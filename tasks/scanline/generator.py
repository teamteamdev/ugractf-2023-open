#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


import PIL.Image
import barcode
import io
import os

def generate():
    flag = get_flag()
    flag_enc = flag.upper().replace("_", " ")

    bio = io.BytesIO()
    options = {"module_width": 0.0846666666, "module_height": 0.0846666666, "quiet_zone": 3, "font_size": 0}
    barcode.Code39(flag_enc, writer=barcode.writer.ImageWriter()).write(bio, options)

    bio.seek(0)
    barcode_img = PIL.Image.open(bio)

    scanner_img = PIL.Image.open(os.path.join("private", "scanners.png"))
    scanner_img.putpalette(scanner_img.getpalette() * 2)
    scanner_img.info["transparency"] = b"\xff" * 128 + bytes([(i % 15 + 240) for i in range(128)])

    for x in range(barcode_img.width):
        for y in range(barcode_img.height):
            if barcode_img.getpixel((x, y))[0] != 255:
                scanner_img.putpixel((x, y + 50), scanner_img.getpixel((x, y + 50)) + 128)

    scanner_img.save(os.path.join(get_attachments_dir(), "scanline.png"))


if __name__ == "__main__":
    generate()
