#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, validate_token


import aiohttp.web
import aiohttp_jinja2 as jinja2
from jinja2 import FileSystemLoader
import io
import os
import pickle
import sys


BASE_DIR = os.path.dirname(__file__)


def get_attempts(state_dir, token):
    attempts_file = os.path.join(state_dir, token) 
    attempts = 10
    try:
        with open(attempts_file, "r") as f:
            attempts -= f.read().count("\n")
    except FileNotFoundError:
        pass
    return attempts


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

        attempts = get_attempts(state_dir, token)
        return jinja2.render_template("main.html", request, {"attempts": attempts})


    @routes.post("/{token}/")
    async def main_post(request):
        token = request.match_info["token"]
        if not validate_token(token):
            raise aiohttp.web.HTTPForbidden

        flag = get_flag(token)
        attempts = get_attempts(state_dir, token)

        form = await request.post()
        try:
            lat, lon = float(form["lat"]), float(form["lon"])
        except:
            return jinja2.render_template("main.html", request, {"attempts": attempts, "error": "presentation"})

        if attempts == 0:
            return jinja2.render_template("main.html", request, {"attempts": attempts, "error": "attempts"})

        with open(os.path.join(state_dir, token), "a") as f:
            f.write(f"{lat} {lon}\n")  # race conditions? who cares!
            attempts -= 1

        if abs(lat - 59.970105) <= 0.000135 and abs(lon - 30.385707) <= 0.00027:
            return jinja2.render_template("main.html", request, {"attempts": attempts, "flag": flag})
        else:
            return jinja2.render_template("main.html", request, {"attempts": attempts, "error": "wrong-point"})


    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])

    if os.environ.get("DEBUG") == "F":
        aiohttp.web.run_app(app, host="0.0.0.0", port=31337)
    else:
        aiohttp.web.run_app(app, path=os.path.join(sys.argv[1], "bigcityroads.sock"))
