# Обучающие материалы: Write-up

Подключаемся к порту и видим красивую ХаКеРсКуЮ систему, в которой можно запускать какие-то команды, например `help` (подразумевалось, что наличие этой команды участники проверят сразу):

![intro](writeup/intro.png)

```
Welcome to Deepend, a training simulator for professional hackers!  You're
gifted a bank account with a starting balance of $1000.  We don't really care
about what you do, but we expect you to get $200000 before your house gets
raided by three-letter agencies.  Have fun while you still can!

localhost❯ help
  help                      Show this help
  ssh <ip>                  Connect to a server by IP
  hosts                     Show known hosts
  ls                        List stored files
  funds                     Show bank account information
  exit                      Disconnect
```

Сразу проверим все, что нам известно:

```
localhost❯ hosts
🏠 10.0.0.13       Deepend Bulletin Board

localhost❯ ls
0 file(s) stored

localhost❯ funds
Your balance: $1000.
```

Негусто. Попробуем подключиться к BBS:

```
localhost❯ ssh 10.0.0.13
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                           DEEPEND  BULLETIN  BOARD                           │
│                            ░░░░░░░░░░░░░░░░░░░░░░░░                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Welcome to the first (and only) bulletin board for professional hackers!  Here,
you can buy software, get jobs, and measure your progress.

Choose option:
- software             List available software
- buy-software <name>  Install software
- jobs                 List jobs
- apply-job <number>   Apply at jobs
- current-job          Show information about currently taken job
- abandon-job          Abandon currently taken job
- submit-job           Report job completeness
- exit                 Disconnect from server
```

Раз нас просят заработать деньги, видимо, придется работать.

```
10.0.0.13❯ jobs
Short descriptions of available jobs follow.  More information will be
available once you apply.
[#01 | $  300] Purge information from an internal system
[#02 | $  500] Purge information from an internal system
[#03 | $  300] Purge information from an internal system
[#04 | $  300] Steal files from a secure server
[#05 | $  500] Purge information from an internal system
[#06 | $  500] Purge information from an internal system
[#07 | $  500] Purge information from an internal system
[#08 | $  300] Purge information from an internal system
[#09 | $  500] Purge information from an internal system
[#10 | $  500] Purge information from an internal system
[#11 | $  500] Steal files from a secure server
[#12 | $  300] Purge information from an internal system
[#13 | $  500] Steal files from a secure server
[#14 | $  300] Purge information from an internal system
[#15 | $  400] Steal files from a secure server
[#16 | $  500] Steal files from a secure server
[#17 | $  300] Steal files from a secure server
[#18 | $  500] Steal files from a secure server
[#19 | $  300] Steal files from a secure server
[#20 | $  300] Steal files from a secure server
````

Тут все примерно одинаково, поэтому возьмем какую-нибудь дорогую задачу:

```
10.0.0.13❯ apply-job 11
Your current job is:
| Hack into the admin account at 90.160.232.97.
| Download file named KRA-7eff25-357288 and submit it via Deepend Bulletin Board.
| Reward: $500
```

Попробуем подключиться к этому IP:

```
10.0.0.13❯ exit

localhost❯ ssh 90.160.232.97
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                                                              @
@ Kraftify Internal Services System                                            @
@                                                                              @
@ UNAUTHORIZED ACCESS FORBIDDEN                                                @
@                                                                              @
@ LOGIN NOW                                                                    @
@                                                                              @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


90.160.232.97❯ help
  help                      Show this help
  login <login> <password>  Authorize
  exit                      Disconnect
```

Попробуем подобрать пароль к `admin`:

```
90.160.232.97❯ login admin admin
Wrong password.

90.160.232.97❯ login admin password
Wrong password.

90.160.232.97❯ login admin 123
Wrong password.

90.160.232.97❯ login admin 12345678
Wrong password.

90.160.232.97❯ login admin 1234
Wrong password.

90.160.232.97❯ login admin qwerty
Wrong password.
```

Видимо, так просто не получится подобрать. Можно пытаться подбирать по словарю, но, на самом деле, это тоже ничего не даст. Вернемся обратно в BBS и посмотрим другие разделы:

```
90.160.232.97❯ exit

localhost❯ ssh 10.0.0.13
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                           DEEPEND  BULLETIN  BOARD                           │
│                            ░░░░░░░░░░░░░░░░░░░░░░░░                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Welcome to the first (and only) bulletin board for professional hackers!  Here,
you can buy software, get jobs, and measure your progress.

10.0.0.13❯ software
- brute-password
  Crack the password of an account using brute force
  Cost: $200
- cover-tracks
  Confuse forensics systems, enabling safe uninterruptable connection
  Cost: $1400
- inject-code
  Upload a program to server and execute it
  Cost: $2000
- generate-malware
  Generate brand new malware
  Cost: $2000
- brute-tcp
  Use the botnet to send tons of requests to target server
  Cost: $1000
```

Первое нам как раз нужно, и мы можем его себе позволить.

```
10.0.0.13❯ buy-software brute-password
Thank you for buying this software!  You can now use it at any server by using
brute-password as a command name.

10.0.0.13❯ exit
```

Так, как этим пользоваться?

```
localhost❯ help
  help                      Show this help
  ssh <ip>                  Connect to a server by IP
  hosts                     Show known hosts
  ls                        List stored files
  funds                     Show bank account information
  exit                      Disconnect
⚒ brute-password <login>    Crack the password of an account using brute force
```

На этом месте многие участники запустили `brute-password admin` и получили следующее:

```
localhost❯ brute-password admin
Cracking...
The password is el1t3_h4xx0r.
```

Это была пасхалка — пароль от `localhost`, но кто-то решил, что это пароль от сервера, и обломался. Правильно утилитой пользоваться так:

```
localhost❯ ssh 90.160.232.97
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                                                              @
@ Kraftify Internal Services System                                            @
@                                                                              @
@ UNAUTHORIZED ACCESS FORBIDDEN                                                @
@                                                                              @
@ LOGIN NOW                                                                    @
@                                                                              @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


90.160.232.97❯ brute-password admin
Cracking...
The password is 602996ff.

90.160.232.97❯ login admin 602996ff
You are now authorized as admin.
```

Теперь можно и разобраться с файлом:

```
90.160.232.97❯ help
  help                      Show this help
  ls                        List available files
  rm <file>                 Delete file
  download <file>           Download file to local PC
  exit                      Logout
⚒ brute-password <login>    Crack the password of an account using brute force

90.160.232.97❯ ls
20 file(s) stored
- KRA-0fed5b-733393
- KRA-2a1a1f-954779
- KRA-319187-730759
- KRA-382f85-740828
- KRA-3e4c0d-726308
- KRA-45b462-155479
- KRA-4fa403-153977
- KRA-5d5e6c-869706
- KRA-6b0461-851049
- KRA-76efd7-588271
- KRA-7eff25-357288
- KRA-97d3af-434432
- KRA-9a0af5-389952
- KRA-9b0dce-968215
- KRA-9fe3bc-535248
- KRA-a4faa1-326216
- KRA-b6e874-001651
- KRA-b8b003-494112
- KRA-bc1166-447431
- KRA-f2bf39-713999

90.160.232.97❯ download KRA-7eff25-357288
File KRA-7eff25-357288 downloaded successfully.
```

Отправим файл:

```
90.160.232.97❯ exit

90.160.232.97❯ exit

localhost❯ ssh 10.0.0.13
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                           DEEPEND  BULLETIN  BOARD                           │
│                            ░░░░░░░░░░░░░░░░░░░░░░░░                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Welcome to the first (and only) bulletin board for professional hackers!  Here,
you can buy software, get jobs, and measure your progress.

10.0.0.13❯ submit-job
The employer has confirmed you have completed the task.  Payment has been
delivered to your bank account.
```

Можно проверить, что наш баланс правда увеличился:

```
10.0.0.13❯ exit

localhost❯ funds
Your balance: $1300.
```

Осталось этот процесс автоматизировать: подключаемся к BBS, берем самую дорогую задачу, подключаемся к серверу, ломаем пароль, скачиваем или удаляем файл, сдаем задачу. Сделать это можно, например, с помощью библиотеки [pwntools](https://docs.pwntools.com/en/stable/) на Python. Пожалуй, единственная сложность с автоматизацией на этом этапе — цвета и форматирование, которые сделаны с помощью [ANSI-последовательностей](https://ru.wikipedia.org/wiki/%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D1%8F%D1%8E%D1%89%D0%B8%D0%B5_%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D0%B8_ANSI). От них можно избавиться для удобства парсинга, например, вырезав текст по регулярному выражению `/\x1b[.*?m/`.

Все бы хорошо, но в какой-то момент счастье заканчивается:

```
localhost❯ ssh 35.91.244.128
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                                                              @
@ GoBright Internal Services System                                            @
@                                                                              @
@ UNAUTHORIZED ACCESS FORBIDDEN                                                @
@                                                                              @
@ LOGIN NOW                                                                    @
@                                                                              @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


35.91.244.128❯ brute-password admin
This server has forensics systems that confuse brute force.  Install
cover-tracks to circumvent them.
```

Ну хоть написано, как решать проблему.

```
35.91.244.128❯ exit

localhost❯ ssh 10.0.0.13
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                           DEEPEND  BULLETIN  BOARD                           │
│                            ░░░░░░░░░░░░░░░░░░░░░░░░                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Welcome to the first (and only) bulletin board for professional hackers!  Here,
you can buy software, get jobs, and measure your progress.

10.0.0.13❯ buy-software cover-tracks
Thank you for buying this software!  You can now use it at any server by using
cover-tracks as a command name.
```

Теперь можно продолжать ломать машины дальше. Здесь проблем со скачиванием и удалением файлов быть больше не должно, если только не окажется, что нужно скачать файл, который был удален во время предыдущего задания. Это происходит редко, поэтому эту ситуацию можно проигнорировать, либо скачивать каждый файл перед удалением, либо делать в этом случае `abandon-job`.

Уровень сложности потихоньку повышается, и работодатели все больше доверяют вам непростые задачи. Вам же лучше: более сложные задачи — больше денег. Можно пытаться какое-то время игнорировать задания, которые решать вы пока не умеете, но в какой-то момент простые закончатся, а денег хватить не будет, поэтому решать их придется.

Следующая по сложности задача выглядит так:

```
[#20 | $ 1300] Infect our rival's server with malware

10.0.0.13❯ apply-job 20
Your current job is:
| Hack into the admin account at 185.76.58.136.
| Install a backdoor and provide credentials to us via Deepend Bulletin Board.
| Reward: $1300
```

Решать ее надо так:

```
10.0.0.13❯ buy-software inject-code
Thank you for buying this software!  You can now use it at any server by using
inject-code as a command name.

10.0.0.13❯ buy-software generate-malware
Thank you for buying this software!  You can now use it at any server by using
generate-malware as a command name.

localhost❯ generate-malware
Generating...
Backdoor backdoor-76181b.exe generated.

localhost❯ ssh 185.76.58.136
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                                                              @
@ Fleck Internal Services System                                               @
@                                                                              @
@ UNAUTHORIZED ACCESS FORBIDDEN                                                @
@                                                                              @
@ LOGIN NOW                                                                    @
@                                                                              @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


185.76.58.136❯ brute-password admin
Cracking...
The password is b5c5b5b5.

185.76.58.136❯ login admin b5c5b5b5
You are now authorized as admin.

185.76.58.136❯ inject-code backdoor-76181b.exe
Code injected.

185.76.58.136❯ exit

185.76.58.136❯ exit

localhost❯ ssh 10.0.0.13
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                           DEEPEND  BULLETIN  BOARD                           │
│                            ░░░░░░░░░░░░░░░░░░░░░░░░                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Welcome to the first (and only) bulletin board for professional hackers!  Here,
you can buy software, get jobs, and measure your progress.

10.0.0.13❯ submit-job
The employer has confirmed you have completed the task.  Payment has been
delivered to your bank account.
```

И, наконец, последняя по сложности задача:

```
[#20 | $ 1800] Crash our competitor's performance

10.0.0.13❯ apply-job 20
Your current job is:
| Infect any machines of your choice with backdoors and use this botnet to DoS
| our competitor at 62.139.102.98.  Once its performance falls to 10 rps,
| ping us at Deepend Bulletin Board.
| Reward: $1800
```

Здесь нужно сделать ровно то, что написано, но учесть, что эффективность DDoS прямо пропорциональна числу зараженных хостов, поэтому стоит залить как можно больше бэкдоров. Задача была реализована так, что 19 машин должно хватить. Список машин для заражения можно достать, например, через `hosts`, либо просто запоминать все доступные IP.

```
localhost❯ brute-tcp 62.139.102.98
DoSing the server...
The estimated throughput of the server is 68 rps
The estimated throughput of the server is 41 rps
The estimated throughput of the server is 29 rps
The estimated throughput of the server is 23 rps
The estimated throughput of the server is 19 rps
The estimated throughput of the server is 16 rps
The estimated throughput of the server is 13 rps
The estimated throughput of the server is 12 rps
The estimated throughput of the server is 11 rps
The estimated throughput of the server is 10 rps
```

На этом различные задания заканчиваются, и остается только это все автоматизировать и дождаться заветного флага:

```
10.0.0.13❯ submit-job
The employer has confirmed you have completed the task.  Payment has been
delivered to your bank account.

YOUR FLAG: ugra_i_am_in_erxqd41jzsdz
```

Полный код автоматического решателя доступен в [solve.py](solve.py).

Флаг: **ugra_i_am_in_erxqd41jzsdz**
