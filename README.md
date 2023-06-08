# Ugra CTF Open 2023

4–6 июня 2023 | [Сайт](https://2023.ugractf.ru/)

## Таски

### Lawful

[Режим доступа](tasks/accessthelink/) (purplesyringa, misc 100)  
[Главная дорога](tasks/bigcityroads/) (nsychev, recon 150)  
[Мониторинг](tasks/monitoring/) (baksist, web 50)

[Только не это…](tasks/ohgodno/) (purplesyringa, misc 200)  
[Сам всё сделаю](tasks/tecret/) (gudn, admin 200)  
[Разобрезать](tasks/uncut/) (enhydra, forensics 150)

[Пойман на камеру](tasks/carrier/) (enhydra, recon 300)

### Neutral

[Паутинка](tasks/cobweb/) (ksixty, stegano 100)  
[Величайший ценитель](tasks/connoisseur/) (enhydra, stegano 150)  
[В один проход](tasks/scanline/) (enhydra, stegano 100)  
[Стегопентест](tasks/stegopentest/) (baksist, ctb 100)

[Но не взбалтывать](tasks/blendingmode/) (enhydra, stegano 200)  
[Обучающие материалы](tasks/deepend/) (purplesyringa, ppc 200)  
[Коллекция ошибок](tasks/errorcollection/) (astrra, forensics 150)  
[Просто скажи](tasks/sayinggoes/) (enhydra, crypto 200)  
[Как я провелето](tasks/summerspent/) (enhydra, misc 150)

[Конференция](tasks/conference/) (abbradar, reverse 350)  
[Высота полёта](tasks/flyover/) (enhydra, ppc 350)

### Chaotic

[Landing](tasks/landing/) (purplesyringa, web 50)  
[Схемы и мемы](tasks/schememe/) (baksist, web 100)  
[UcucugaKB](tasks/ucucugakb/) (baksist, web 100)

[Войти и не пострадать](tasks/bururute/) (enhydra, ppc 200)  
[Landing 2](tasks/landing2/) (purplesyringa, web 400)  
[Ничего не забыть](tasks/noteotp/) (gudn, web 200)  
[☭](tasks/redscare/) (purplesyringa, ppc 150)  
[Делай как я](tasks/repeatafterme/) (enhydra, forensics 300)  
[The Project O](tasks/theprojecto/) (nsychev, web 200)  
[Web log](tasks/weblog/) (purplesyringa, web 200)

[Документация](tasks/books/) (purplesyringa, ctb 350)

----

[The End](tasks/fruits/) (ucucuga 0)

## Команда разработки

Олимпиада была подготовлена командой [team Team].

[Никита Сычев](https://github.com/nsychev) — руководитель команды  
[Калан Абе](https://github.com/enhydra) — разработчик тасков  
[Коля Амиантов](https://github.com/abbradar) — инженер по надёжности  
[Астра Андриенко](https://github.com/astrrra) — разработчица тасков  
[Ваня Клименко](https://github.com/ksixty) — разработчик сайта и платформы, арт-директор  
[Даниил Новоселов](https://github.com/gudn) — разработчик тасков  
[Матвей Сердюков](https://github.com/baksist) — разработчик тасков  
[Алиса Сиренева](https://github.com/imachug) — разработчица тасков и платформы

## Организаторы и спонсоры

Организаторы Ugra CTF — Югорский НИИ информационных технологий, Департамент информационных технологий и цифрового развития ХМАО–Югры и команда [team Team].

## Генерация заданий

Некоторые таски создаются динамически — у каждого участника своя, уникальная версия задания. В таких заданиях вам необходимо запустить генератор — обычно он находится в файле `generate.py` в директории задания. Обычно генератор принимает три аргумента — уникальный идентификатор, директорию для сохранения файлов для участника и названия генерируемых тасков (последний, как правило, не используется). Например, генератор можно запустить так:

```bash
./tasks/hello/generate.py 1337 /tmp/hello
```

Уникальный идентификатор используется для инициализации генератора псевдослучайных чисел, если такой используется. Благодаря этому, повторные запуски генератора выдают одну и ту же версию задания.

Генератор выведет на стандартный поток вывода JSON-объект, содержащий флаг к заданию и информацию для участника, а в директории `/tmp/hello` появятся вложения, если они есть.

## Лицензия

Материалы соревнования можно использовать для тренировок, сборов и других личных целей, но запрещено использовать на своих соревнованиях. Подробнее — [в лицензии](LICENSE).
