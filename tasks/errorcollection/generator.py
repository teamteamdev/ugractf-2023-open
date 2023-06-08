#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag

from PIL import Image
import qrcode
import sys
from zbarlight import scan_codes
import numpy as np
import random
import os

def generate():
    flag = get_flag()
    img = qrcode.make(flag, box_size=1, error_correction=qrcode.constants.ERROR_CORRECT_L, border=3)
    img.save("/tmp/qrcode.png")

    # flip random bits until the qr code is not readable
    img = Image.open("/tmp/qrcode.png")
    data = scan_codes('qrcode', img)
    # print(data)
    if data == "":
        exit(1)
    while data != None:
        # flip a random bit, it should be at least 10 pixels away from the borders
        x = random.randint(12, img.width - 12)
        y = random.randint(12, img.height - 12)
        img.putpixel((x, y), 255)
        # check if the qr code is readable
        data = scan_codes('qrcode', img)
        # print(data)

    # save the qr code using Image.save to get_attachments_dir()+"recovered_code.png"
    img.save(os.path.join(get_attachments_dir(), "recovered_code.png"))

if __name__ == "__main__":
    generate()
