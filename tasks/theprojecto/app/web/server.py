#!/usr/bin/env python3

import aiohttp.web
import aiohttp_jinja2 as jinja2
from jinja2 import FileSystemLoader
import logging
import os
import sys
import time

import jwt
import sqlite3


BASE_DIR = os.path.dirname(__file__)


def make_app(debug: bool = False):
    con = sqlite3.connect("/tmp/app.db", isolation_level=None)
    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE IF NOT EXISTS users (login TEXT UNIQUE, password TEXT);")
        cur.execute("INSERT INTO users VALUES ('admin', '');")
    except sqlite3.Error:
        pass

    with open("/etc/key", "rb") as f:
        key = f.read(32)

    app = aiohttp.web.Application(debug=debug)
    routes = aiohttp.web.RouteTableDef()


    @routes.get("/{token}")
    async def slashless(request):
        return aiohttp.web.HTTPMovedPermanently(f"/{request.match_info['token']}/")


    @routes.get("/{token}/")
    async def main(request: aiohttp.web.Request) -> aiohttp.web.Response:
        token = request.cookies.get("token")
        if token is None:
            return jinja2.render_template("welcome.html", request, {})

        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError:
            return jinja2.render_template("error.html", request, {"error": "Ваш токен некорректен. Получите новый."}, status=403)
        
        if header["alg"] != "HS256":
            return jinja2.render_template("error.html", request, {"error": "Ваш токен некорректен. Получите новый."}, status=403)

        kid = header.get("kid")
        if kid is None or not os.path.exists(kid) or os.path.isdir(kid):
            return jinja2.render_template("error.html", request, {"error": "Ваш токен некорректен. Получите новый."}, status=403)

        try:
            with open(kid, "rb") as f:
                key = f.read(32)

            assert len(key) == 32
        except (OSError, AssertionError):
            return jinja2.render_template("error.html", request, {"error": "Ваш токен некорректен. Получите новый."}, status=403)

        try:
            token_data = jwt.decode(token, key, algorithms=["HS256"])
        except jwt.PyJWTError:
            response = jinja2.render_template("welcome.html", request, {})
            response.del_cookie("token")
            return response

        if token_data.get("login") == "admin":
            try:
                with open("/flag.txt") as f:
                    flag = f.read().strip()
            except OSError:
                flag = "***flag***"
        else:
            flag = None

        return jinja2.render_template("main.html", request, {"flag": flag, "user": token_data.get("login")})

    @routes.get("/{token}/logout")
    async def logout(request: aiohttp.web.Request) -> aiohttp.web.Response:
        response = aiohttp.web.HTTPFound(f"/{request.match_info['token']}/")
        response.del_cookie("token")
        return response


    @routes.post("/{token}/login")
    async def login(request: aiohttp.web.Request) -> aiohttp.web.Response:
        data = await request.post()
        login = data.get("login")
        password = data.get("password")
        
        if not login or not password or not isinstance(login, str) or not isinstance(password, str) or len(password) > 20 or len(login) > 20:
            return jinja2.render_template("error.html", request, {"error": "Поля не заполнены"}, status=400)

        cur.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
        
        user = cur.fetchone()
        if user is None:
            return jinja2.render_template("error.html", request, {"error": "Пользователь не найден"}, status=403)

        token = jwt.encode({"login": login}, key, algorithm="HS256", headers={"kid": "/etc/key", "iat": time.time()})
        response = aiohttp.web.HTTPFound(f"/{request.match_info['token']}/")
        response.set_cookie("token", token, httponly=True, samesite="Strict")
        return response

    @routes.get("/{token}/register")
    async def register(request: aiohttp.web.Request) -> aiohttp.web.Response:
        return jinja2.render_template("register.html", request, {})

    @routes.post("/{token}/register")
    async def process_register(request: aiohttp.web.Request) -> aiohttp.web.Response:
        data = await request.post()
        login = data.get("login")
        password = data.get("password")
        
        if not login or not password or not isinstance(login, str) or not isinstance(password, str) or len(password) > 20 or len(login) > 20:
            return jinja2.render_template("error.html", request, {"error": "Поля не заполнены"}, status=400)

        try:
            cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
        except sqlite3.IntegrityError:
            return jinja2.render_template("error.html", request, {"error": "Пользователь уже существует"}, status=409)

        return aiohttp.web.HTTPFound(f"/{request.match_info['token']}/")

    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    return app


if __name__ == "__main__":
    if os.environ.get("DEBUG") == "F":
        aiohttp.web.run_app(make_app(True), host="0.0.0.0", port=31337)
    else:
        aiohttp.web.run_app(make_app(), path=sys.argv[1])
