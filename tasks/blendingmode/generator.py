#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


import PIL.Image, PIL.ImageFont, PIL.ImageDraw
import os
import random
import re


def generate():
    flag = get_flag()
    random.seed(flag.encode())

    stencil_mask = PIL.Image.new("1", (400, 500))
    font = PIL.ImageFont.truetype(os.path.join("private", "SairaStencilOne-Regular.ttf"), 66)
    draw = PIL.ImageDraw.Draw(stencil_mask)

    draw.text((0, 0), re.compile("(.{7,}?_)").sub("\\1\n", flag)[:-8] + "\n" + flag[-8:], fill=1, font=font)

    # offsets = [(random.randint(0, 200), random.randint(0, 200)) for _ in range(4)]
    offsets = [(100, 100) for _ in range(4)]

    stencil = stencil_mask.convert("RGBA")
    distributions = [[0] * 256] * 4
    population = list(range(256))
    for x in range(stencil.width):
        for y in range(stencil.height):
            if stencil.getpixel((x, y)) == (255, 255, 255, 255):
                while True:
                    try:
                        rands = [random.random() * 0.3 + 0.7 for _ in range(4)]
                        prod = rands[0] * rands[1] * rands[2] * rands[3]
                        rands = [int((i / (prod ** 0.25)) * (0.5 ** 0.25) * 256) for i in rands]
                        if all(i <= 255 for i in rands):
                            break
                    except OverflowError:
                        continue
                for n, i in enumerate(rands):
                    distributions[n][i] += 1
                stencil.putpixel((x, y), tuple(rands))

    stencils = [PIL.Image.new("L", (600, 700)) for _ in offsets]

    choices = [iter(random.choices(population, weights=distributions[n], k=st.width * st.height)) for st in stencils]

    for n, st in enumerate(stencils):
        for x in range(st.width):
            for y in range(st.height):
                if (0 <= (x_ := x - offsets[n][0]) < stencil.width and 
                        0 <= (y_ := y - offsets[n][1]) < stencil.height and
                        stencil_mask.getpixel((x_, y_))):
                    st.putpixel((x, y), stencil.getpixel((x_, y_))[n])
                else:
                    st.putpixel((x, y), next(choices[n]))

    for n, s in enumerate(stencils):
        ss = s.convert("RGBA")
        for x in range(ss.width):
            for y in range(ss.height):
                ss.putpixel((x, y), (0, 0, 0, 255 - s.getpixel((x, y))))
        ss.save(os.path.join(get_attachments_dir(), f"{n}.png"))


if __name__ == "__main__":
    generate()
