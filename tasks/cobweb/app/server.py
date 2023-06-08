#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, validate_token


import aiohttp.web
import aiohttp_jinja2 as jinja2
from jinja2 import FileSystemLoader
import PIL.Image
import multiprocessing
import os
import logging
import shutil

from ani_file import ani_file
from itertools import cycle
from PIL import ImageFont, ImageDraw, Image
from colour import Color
from io import BytesIO
import struct

import sys


BASE_DIR = os.path.dirname(__file__)


def draw_letter(image, letter):
    im = image.copy()
    draw = ImageDraw.Draw(im)
    font = ImageFont.load(os.path.join(BASE_DIR, "font", "tom-thumb.pil"))
    draw.text((26, 26), letter, font=font, fill="#000")
    return im

def draw_msg(image, msg):
    seq = zip(cycle([image]), msg)
    return [draw_letter(image, ch) for image, ch in seq]

def space_text(text, n):
    return (" " * n).join(list(text)) + (" " * n)

def replace_color(image: PIL.Image.Image, color):
    imc = image.copy()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if image.getpixel((x, y)) == (0, 0, 0, 255):
                imc.putpixel((x, y), color)
    return imc

def paint_gradient(images, color_a, color_b):
    conv_color  = lambda color: (*[int(x * 255) for x in color.get_rgb()], 255)
    gradient = Color(color_a).range_to(Color(color_b), len(images))
    colors   = map(conv_color, gradient)
    return [replace_color(image, color) for image, color in zip(images, colors)]

def ico(image):
    buf = BytesIO()
    image.save(buf, format="ico", bitmap_format="bmp", sizes=[(32, 32)])
    buf.seek(0)
    return buf

def msg_img_seq(msg, image, color_a="#FF00FF", color_b="#FF0000", spacing=4):
    seq = paint_gradient(
        draw_msg(
            image, 
            space_text(msg, spacing)
        ), color_a, color_b)
    icos = map(ico, seq)
    return list(icos)

class my_ani_write(ani_file.ani_write):
    def _pack_anih(self):
        self._datawritten += 44 #Size of 11I of anih chunk
        return struct.pack("<4s10I",b"anih",36,36,self._nFrames,self._nSteps,self._iWidth,self._iHeight,self._iBitCount,self._nPlanes,self._iDispRate,self._bfAttributes)

    def _pack_info(self):
        if hasattr(self,"_inam") or hasattr(self,"_iart"):
            inamChunk,iartChunk = b"",b""
            # IMPORTANT: _inam and _iart need to be padded to even length for Chunk to work
            if hasattr(self,"_inam"):
                inamChunk = struct.pack(f'<4sI{len(self._inam)}s{"x"*(len(self._inam)%2)}' ,b"INAM",len(self._inam),self._inam)
            if hasattr(self,"_iart"):
                iartChunk = struct.pack(f'<4sI{len(self._iart)}s{"x"*(len(self._iart)%2)}',b"IART",len(self._iart),self._iart)
            
            self._datawritten += 12 + len(iartChunk) + len(inamChunk)
            return struct.pack("<4sI4s", b"LIST",4+len(inamChunk)+len(iartChunk),b"INFO") + inamChunk + iartChunk

    def _pack_frames(self):
        print(self.__dict__)
        iconSize = 0
        iconChunks = b""
        for icon in self._framespath:
            data = icon.read()
            iconChunks += struct.pack("<4sI", b"icon", len(data)) + data
            iconSize += 8 + len(data)
        self._datawritten += 12 + iconSize
        return struct.pack("<4sI4s", b"LIST", 4+iconSize, b"fram") + iconChunks

    def close(self):
        try:
            if hasattr(self, "_file") and self._file:
                self._write_data()
                self._file.flush()
        finally:
            self._file = None
            file = self._i_opened_the_file
            if file:
                self._i_opened_the_file = None
                file.close()


def generate(state_dir, token):
    flag = get_flag(token)

    data_path = os.path.join(state_dir, token)
    data_temp_path = os.path.join(state_dir, "_" + token)

    try:
        os.mkdir(data_path)
        cur = Image.open(os.path.join(BASE_DIR, 'cursor.png'))
        seq = msg_img_seq(flag, cur)
        seq_idx = list(range(len(seq)))
        rate = [2 for _ in seq_idx]

        test = my_ani_write(os.path.join(data_path, "cursor.ani"))
        test.setframespath(seq)
        test.setseq(tuple(seq_idx))
        test.setrate(rate)
        test.setauthor("voronbay@uniiu.su")
        test.setname("Pautinka 001 (06.05.1997)")
        test.close()
    except:
        logging.exception("Very bad things happened with token %s", token)
        raise
    finally:
        shutil.rmtree(data_temp_path)


pool = multiprocessing.Pool(4)


def make_app(state_dir):
    app = aiohttp.web.Application()
    routes = aiohttp.web.RouteTableDef()
    routes.static("/static", os.path.join(BASE_DIR, "static"))


    @routes.get("/{token}")
    async def slashless(request):
        return aiohttp.web.HTTPMovedPermanently(f"/{request.match_info['token']}/")


    @routes.get("/{token}/")
    async def main(request):
        if not validate_token(request.match_info["token"]):
            raise aiohttp.web.HTTPForbidden

        return jinja2.render_template("main.html", request, {})


    @routes.get("/{token}/cursor.ani")
    async def pics(request):
        token = request.match_info["token"]
        if not validate_token(token):
            raise aiohttp.web.HTTPForbidden

        if not os.path.exists(pic_path := os.path.join(state_dir, token)):
            if not os.path.exists(tmp_path := os.path.join(state_dir, "_" + token)):
                os.mkdir(tmp_path)
                pool.apply_async(generate, (state_dir, token, ))
            raise aiohttp.web.HTTPCreated

        return aiohttp.web.Response(
            body=open(os.path.join(pic_path, "cursor.ani"), "rb").read(),
            content_type="application/x-navi-animation"
        )

    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])

    if os.environ.get("DEBUG") == "F":
        aiohttp.web.run_app(app, host="0.0.0.0", port=31337)
    else:
        aiohttp.web.run_app(app, path=os.path.join(sys.argv[1], "cobweb.sock"))
