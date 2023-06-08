#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


import PIL.Image, PIL.ImageDraw, PIL.ImageFont
import io
import re
import os


def generate():
    flag = get_flag()
    font = PIL.ImageFont.truetype(os.path.join("private", "roboto.ttf"), 64)
    
    img = PIL.Image.open(os.path.join("private", "orig.png"))
    draw = PIL.ImageDraw.Draw(img)
    draw.text((42, 1755), re.compile("(.{30,}?_)").sub("\\1\n", flag), fill=(0, 0, 0), font=font)

    bio = io.BytesIO()
    img.save(bio, format="PNG")

    cr_bio = io.BytesIO()
    img.crop((0, 0, 1080, 300)).save(cr_bio, format="PNG")

    data = cr_bio.getvalue() + bio.getvalue()[len(cr_bio.getvalue()):]
    open(os.path.join(get_attachments_dir(), "Снимок экрана_20230603-174642.png"), "wb").write(data)


if __name__ == "__main__":
    generate()
