#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag

import random
import io
import string
import re
import os

import PIL.Image, PIL.ImageDraw, PIL.ImageFont

FRUITS_LETTERS = "storm"
NON_FRUITS_LETTERS = "abcdefghijklnpquvwxyz"


def generate():
    flag = get_flag()
    random.seed(flag)

    font = PIL.ImageFont.truetype("roboto.ttf", 14)

    fruits_letters = list(FRUITS_LETTERS)

    non_fruits_letters = list(NON_FRUITS_LETTERS)
    random.shuffle(non_fruits_letters)

    fruits_pics = os.listdir("fruits")
    non_fruits_pics = os.listdir("nonfruits")

    for i, letter, pic in zip(range(5), fruits_letters, fruits_pics):
        img = PIL.Image.open(os.path.join("fruits", pic)).convert("RGBA")
        draw = PIL.ImageDraw.Draw(img)
        draw.text((0, 0), letter, fill=(255, 255, 255, 254), font=font)
        filename = f"{flag[i*4:i*4+4]}.png"
        img.save(os.path.join(get_attachments_dir(), filename), format="PNG")
    
    for letter, pic in zip(non_fruits_letters, non_fruits_pics):
        img = PIL.Image.open(os.path.join("nonfruits", pic)).convert("RGBA")
        draw = PIL.ImageDraw.Draw(img)
        draw.text((0, 0), letter, fill=(255, 255, 255, 254), font=font)
        filename = f"{''.join(random.choice(string.ascii_lowercase + string.digits + '_________________') for _ in range(4))}.png"
        img.save(os.path.join(get_attachments_dir(), filename), format="PNG")


if __name__ == "__main__":
    generate()
