#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, get_secret, validate_token


import aiohttp.web
import aiohttp_jinja2 as jinja2
from jinja2 import FileSystemLoader
import io
import lru
import os
import pickle
import sys


BASE_DIR = os.path.dirname(__file__)


attempts = {}  # lost on every restart but not that we cared


def get_ip(request):
    return request.headers.get("X-Forwarded-For", request.remote)


def make_app(state_dir):
    app = aiohttp.web.Application()
    routes = aiohttp.web.RouteTableDef()
    if os.path.exists(static_dir := os.path.join(BASE_DIR, "static")):
        routes.static("/static", static_dir)


    @routes.get("/{token}")
    async def slashless(request):
        return aiohttp.web.HTTPMovedPermanently(f"/{request.match_info['token']}/")


    @routes.get("/{token}/")
    async def main(request):
        token = request.match_info["token"]
        if not validate_token(token):
            raise aiohttp.web.HTTPForbidden

        ip = get_ip(request)
        blocked = attempts.get(token, {}).get(ip) == 0

        return jinja2.render_template("main.html", request, {"ip": ip, "blocked": blocked, "format_ok": True, "otp_ok": True})


    @routes.post("/{token}/")
    async def main_post(request):
        token = request.match_info["token"]
        if not validate_token(token):
            raise aiohttp.web.HTTPForbidden

        correct_otp = get_secret("otp", token)
        flag = get_flag(token)

        ip = get_ip(request)
        form = await request.post()
        otp = form["otp"]

        if token not in attempts:
            attempts[token] = lru.LRU(4000)
        if ip not in attempts[token]:
            attempts[token][ip] = 25
        if attempts[token][ip] == 0:
            blocked = True
            otp_ok = False
        else:
            blocked = False
            attempts[token][ip] -= 1
            otp_ok = otp == correct_otp
        format_ok = len(otp) == 5 and all(i in "0123456789" for i in otp)

        return jinja2.render_template("main.html", request, {"ip": ip, "blocked": blocked, "flag": flag if otp_ok else None,
                                                             "format_ok": format_ok, "otp_ok": otp_ok})


    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])

    if os.environ.get("DEBUG") == "F":
        aiohttp.web.run_app(app, host="0.0.0.0", port=31337)
    else:
        aiohttp.web.run_app(app, path=os.path.join(sys.argv[1], "bururute.sock"))
