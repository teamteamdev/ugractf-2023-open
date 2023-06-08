#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, validate_token


import aiohttp.web
import aiohttp_jinja2 as jinja2
import base64
from jinja2 import FileSystemLoader
import PIL.Image
import io
import multiprocessing
import os
import png
import random
import segno
import sys


BASE_DIR = os.path.dirname(__file__)


def generate(state_dir, token):
    flag = get_flag(token)
    random.seed(flag.encode())

    data_path = os.path.join(state_dir, token)
    data_temp_path = os.path.join(state_dir, "_" + token)

    try: 
        flag_qr = segno.make_qr(f"Please have the thing as herein described at your disposal.\n\n{flag}\n\n"
                                f"Nonce={random.randint(0, 10**2233)}",
                                mode="byte", version=40, error="L", boost_error=False, mask=0)
        
        bio = io.BytesIO()
        flag_qr.save(bio, kind="png", scale=4)

        bio.seek(0)
        flag_qr_img = PIL.Image.open(bio).convert("RGBA")

        for error_factor in range(27, 0, -1):
            try:
                for x in range(flag_qr_img.width):
                    for y in range(flag_qr_img.height):
                        if random.random() < error_factor / 100.0:
                            br = flag_qr_img.getpixel((x, y))[0] & 128
                            flag_qr_img.putpixel((x, y), tuple([br + random.randint(0, 127) for _ in range(3)] + [255]))

                pieces = [flag_qr_img.copy() for _ in range(16)]
                for i in range(len(pieces)):
                    x = 185 * (i % 4)
                    y = 185 * (i // 4)
                    pieces[i] = pieces[i].crop((x, y, x + 185, y + 185))

                qrs = []
                for i in range(len(pieces)):
                    bio = io.BytesIO()
                    pieces[i].save(bio, format="PNG")
                    bio.seek(0)

                    chunks = list(png.Reader(file=bio).chunks())
                    rbio = io.BytesIO()
                    r_chunks = []
                    for t, c in chunks:
                        if t == b"IDAT":
                            CHUNK_SIZE = 5600
                            for o in range(0, len(c), CHUNK_SIZE):
                                r_chunks.append((t, c[o : o + CHUNK_SIZE]))
                        else:
                            r_chunks.append((t, c))
                    png.write_chunks(rbio, r_chunks)
                    
                    piece_data = rbio.getvalue()
                    piece_data = piece_data + random.randbytes(2950 * 16 - len(piece_data))

                    qr_seq = segno.make_sequence(piece_data, mode="byte", version=40, error="L", boost_error=False, mask=0)
                    qrs += qr_seq

                break  # successful generation without exceptions
            except ValueError:  # bad luck with compression
                continue

        assert error_factor > 0

        random.shuffle(qrs)
        for n, qr in enumerate(qrs):
            qr.save(os.path.join(data_temp_path, f"{n:03d}.png"), scale=2)

        os.rename(data_temp_path, data_path)
    except:
        shutil.rmtree(data_temp_path)
        raise


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


    @routes.get("/{token}/pics")
    async def pics(request):
        token = request.match_info["token"]
        if not validate_token(token):
            raise aiohttp.web.HTTPForbidden

        if not os.path.exists(pic_path := os.path.join(state_dir, token)):
            if not os.path.exists(tmp_path := os.path.join(state_dir, "_" + token)):
                os.mkdir(tmp_path)
                pool.apply_async(generate, (state_dir, token, ))
            raise aiohttp.web.HTTPCreated

        return aiohttp.web.json_response([("data:image/png;base64," +
                                               base64.b64encode(open(os.path.join(pic_path, f), "rb").read()).decode())
                                          for f in os.listdir(pic_path) if f.endswith(".png")])


    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])

    if os.environ.get("DEBUG") == "F":
        aiohttp.web.run_app(app, host="0.0.0.0", port=31337)
    else:
        aiohttp.web.run_app(app, path=os.path.join(sys.argv[1], "flyover.sock"))
