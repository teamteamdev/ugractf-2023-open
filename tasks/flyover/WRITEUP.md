# Высота полёта: Write-up

Открываем страницу, дожидаемся загрузки, смотрим.

Какое-то время можно на неё просто помедитировать.

Потом следует сохранить картинки для удобного анализа. Видим, что страница делает запрос по пути `pics` и получает список картинок, повторим это:

```python3
import requests
import base64

for n, pic in enumerate(requests.get("https://flyover.o.2023.ugractf.ru/ycmagjq8qjyoex36/pics").json()):
    open(f"{n:03d}.png", "wb").write(base64.b64decode(pic.split(",")[1]))
```

Итак, имеем файлы 000.png — 255.png, в каждом — огромный QR-код. Настолько огромный, что многие считыватели отказываются с ним работать. Среди тех, кто отрабатывает нормально, — [декодер на zxing.org](https://zxing.org/w/decode.jspx). Впрочем, результатом его работы является много-много страшных бинарных данных.

Существуют ещё различные обёртки вокруг библиотеки zxing, в частности, утилиты ZXingReader и ZXingWriter. С ними видно, что zxing, на самом деле, тоже справляется с QR-кодом не сама — а именно, ей нужно указать опцию `-ispure`, говорящую о том, что на картинке есть только один чётко выровненный и обрезанный QR-код, и больше ничего.

```
$ ZXingReader -ispure 000.png
...
Format:   QRCode
Position: 8x8 361x8 361x361 8x361
Rotation: 0 deg
Error:    NoError
EC Level: L
Structured Append: symbol 4 of 16 (parity/id: '28')
```

Structured Append — механизм, позволяющий разделять большой объём данных на несколько QR-кодов; поддерживаются цепочки длиной до 16 QR-кодов на одно сообщение. В каждом таком QR-коде содержится его порядковый номер и общее количество кодов в цепочке.

Просмотрев все файлы, видим, что у нас 16 цепочек по 16 кодов; при этом метаданных, которые давали бы понять, к какой из цепочек следует отнести тот или иной QR-код, у нас нет. В общем случае вариантов их скомпоновать существует $(16!)^{15}$ — это число, состоящее из 200 цифр, поэтому полный перебор — не вариант.

Изучим какой-нибудь из файлов, обозначенный как 1 of 16. В нём встречаются строки `PNG`, `IHDR`, `IDAT`, характерные для PNG-изображений. PNG-файлы состоят из чанков — структур данных, содержащих длину чанка, тип чанка, собственно данные и контрольную сумму. Если чанки `IDAT`, содержащие непосредственно данные, достаточно короткие, то тогда вместо полного перебора можно сделать очень ограниченный частичный, сверяя контрольные суммы. Когда контрольная сумма сойдётся, мы будем точно знать, что цепочка до этого места собрана правильно, и сможем провести следующий перебор; будем продолжать, пока не соберём всю цепочку или не обнаружим чанк типа `IEND`, означающий конец файла.

Для чтения QR-кодов будем использовать библиотеку [zxingcpp](https://pypi.org/project/zxing-cpp/). Она не предоставляет доступа к метаданным Structured Append, поэтому для начала получим эти данные через ZXingReader:

```bash
for i in *.png; do
    mv $i s$(ZXingReader -ispure $i | tail -n1 | grep -o '[0-9]\?[0-9] of' | sed 's/ of//')-$i
done
```

Осуществим перебор. В некоторых местах нам достаточно будет перебрать по одному QR-коду, а в некоторых — несколько (например, в третьих QR-кодах нет конца чанка, поэтому перебирать придётся все комбинации третьих и четвёртых).

```python
import glob
import zxingcpp
import PIL.Image
import itertools
import png
import io

files = glob.glob("*.png")
codes = {}
for fn in files:
    s_number = int(fn.split("-")[0][1:])
    if s_number not in codes:
        codes[s_number] = []
    codes[s_number].append(zxingcpp.read_barcode(PIL.Image.open(fn), is_pure=True).bytes)

chains = []
for code in codes[1]:
    chain = code
    brute_pos = [2]
    chunks_ok = 1  # first IHDR chunk

    while brute_pos:
        for cur_codes in itertools.product(*[codes[p] for p in brute_pos]):
            cur_chain = chain + b"".join(cur_codes)
            bio = io.BytesIO()
            bio.write(cur_chain)
            bio.seek(0)

            try:
                cur_chunks_ok = 0
                for _ in png.Reader(file=bio).chunks():
                    cur_chunks_ok += 1

                brute_pos = []  # no exception thrown, all chunks are OK
                chain = cur_chain
                break
            except png.ChunkError as e:
                if cur_chunks_ok > chunks_ok:  # found new chunk
                    chain = cur_chain
                    chunks_ok = cur_chunks_ok

                    print(brute_pos, f"New chunk found - total {chunks_ok}")
                    brute_pos = [brute_pos[-1] + 1]
                    break
                else:
                    print(brute_pos, e.args[0])
        else:
            brute_pos += [brute_pos[-1] + 1]
    chains.append(chain)

for n, c in enumerate(chains):
    open(f"result/{n}.png", "wb").write(c)
```

![Кусочки](writeup/pieces.png)

Осталось из этих кусочков собрать, как мозаику, уже один большой код — границы картинок разрезают пиксели, поэтому это можно сделать однозначно без труда.

![Результат](writeup/final.png)

Флаг: **ugra_embrace_your_intuition_discover_the_sequences_6f2bkkasij5y33z2**
