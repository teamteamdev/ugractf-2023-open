# Коллекция ошибок: Write-up

## Lawful way

В легенде задания говорится что-то про помехоустойчивость, один бит, и потери информации. Открыв изображение, приложенное к таску, можно увидеть что там QR-код. Попытки сосканировать его не работают (хотя с достаточной степенью **хаотичности** могут и сработать), кажется, с ним что-то не так. Если перечитать легенду еще раз, можно зацепиться за фразу про один бит для потери информации. Может быть, в QR-коде как-то потерялся один бит? Попробуем восстановить его.

Написав незамысловатый скрипт на Python который просто поочерёдно инвертирует каждый пиксель в картинке и пытается ее распознать, можно получить флаг.

```python
from PIL import Image
import sys
from zbarlight import scan_codes
import numpy as np

# open the image
img = Image.open("recovered_code.png")

# for each pixel, try inverting it and check if the qr code is readable
for x in range(img.width):
    for y in range(img.height):
        # invert the pixel
        img.putpixel((x, y), 255 - img.getpixel((x, y)))
        # check if the qr code is readable
        data = scan_codes('qrcode', img)
        if data != None:
            print(data)
            img.save("flag.png")
            img.show()
            exit()
        # invert the pixel back
        img.putpixel((x, y), 255 - img.getpixel((x, y)))
```

Оказывается, в QR-коде было побито ровно на 1 больше чем позволяет его корректирующая способность.

## Chaotic way

Откройте код. Отсканируйте код. Получите флаг.
Поздравляем, ваш курсор оказался ровно на том месте, где был бит ошибки в QR-коде!
Пример данного решения можно найти в файле `chaotic.mp4`.

Флаг: **ugra_noooo_my_pixels_collection_jv6en1wtcgvi52u1**
