from flask import Flask, redirect, render_template, request
from kyzylborda_lib.secrets import get_flag, get_secret, validate_token
from pathlib import Path
import random
import re
import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix


def make_app():
    con = sqlite3.connect("/state/data.db", isolation_level=None)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (token TEXT, login TEXT, password TEXT, UNIQUE (token, login))")
    cur.execute("CREATE TABLE IF NOT EXISTS messages (token TEXT, user_from TEXT, user_to TEXT, message TEXT)")
    cur.execute("CREATE INDEX IF NOT EXISTS messages_to ON messages (token, user_to)")


    tokens_initialized = set()

    def init_db(token: str):
        if token in tokens_initialized:
            return
        try:
            cur.execute(
                "INSERT INTO users (token, login, password) VALUES (?, ?, ?)",
                (token, "admin", "password")
            )
        except sqlite3.IntegrityError:
            pass
        else:
            cur.execute(
                "INSERT INTO users (token, login, password) VALUES (?, ?, ?)",
                (token, "editor", get_secret("editor_password", token))
            )
            cur.execute(
                "INSERT INTO users (token, login, password) VALUES (?, ?, ?)",
                (token, "purplesyringa", "🏳️‍🌈")
            )
            cur.execute(
                "INSERT INTO messages (token, user_from, user_to, message) VALUES (?, ?, ?, ?)",
                (token, "purplesyringa", "admin", get_flag(token))
            )
        tokens_initialized.add(token)


    app = Flask(__name__)
    # Required for server to correctly redirect.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)


    @app.errorhandler(404)
    def page_not_found(e):
        return "Don't forget your token"


    def is_authorized(token: str) -> bool:
        login = request.cookies.get("login")
        password = request.cookies.get("password")
        if not login or not password:
            return False
        return cur.execute("SELECT * FROM users WHERE token = ? AND login = ? AND password = ?", (token, login, password)).fetchone() is not None


    def get_messages(token: str) -> list[dict]:
        login = request.cookies.get("login", "")
        messages = []
        for msg in cur.execute("SELECT user_from, message FROM messages WHERE token = ? AND user_to = ?", (token, login)):
            messages.append({
                "user_from": msg[0],
                "message": msg[1]
            })
        return messages


    def get_state(token: str) -> dict:
        return {
            "token": token,
            "is_authorized": is_authorized(token),
            "login": request.cookies.get("login"),
            "messages": get_messages(token)
        }


    @app.route("/<token>/")
    def index(token: str):
        if not validate_token(token):
            return "Invalid token"
        init_db(token)
        return render_template("index.html", **get_state(token))


    @app.route("/<token>/nasha_ucucuga/")
    def nasha_ucucuga(token: str):
        if not validate_token(token):
            return "Invalid token"
        init_db(token)
        return render_template("nasha_ucucuga.html", **get_state(token))


    @app.route("/<token>/register/", methods=["GET", "POST"])
    def register(token: str):
        if not validate_token(token):
            return "Invalid token"
        init_db(token)
        if request.method == "POST":
            login = request.form["name"]
            password = request.form["password"]
            try:
                cur.execute("INSERT INTO users (token, login, password) VALUES (?, ?, ?)", (token, login, password))
            except sqlite3.IntegrityError:
                return "This user already exists"
            else:
                cur.execute(
                    "INSERT INTO messages (token, user_from, user_to, message) VALUES (?, ?, ?, ?)",
                    (token, "admin", login, "Благодарим за регистрацию в системе")
                )
            resp = redirect(f"/{token}/", code=302)
            resp.set_cookie("login", login)
            resp.set_cookie("password", password)
            return resp
        else:
            return render_template("register.html", **get_state(token))


    @app.route("/<token>/login/", methods=["POST"])
    def login(token: str):
        if not validate_token(token):
            return "Invalid token"
        init_db(token)
        login = request.form["login"]
        password = request.form["password"]
        row = cur.execute("SELECT password FROM users WHERE token = ? AND login = ?", (token, login)).fetchone()
        if not row:
            return "Unknown user"
        if row[0] != password:
            return "Wrong password"
        resp = redirect(f"/{token}/", code=302)
        resp.set_cookie("login", login)
        resp.set_cookie("password", password)
        return resp


    @app.route("/<token>/logout/")
    def logout(token: str):
        if not validate_token(token):
            return "Invalid token"
        resp = redirect(f"/{token}/", code=302)
        resp.set_cookie("login", "")
        resp.set_cookie("password", "")
        return resp


    @app.route("/<token>/__reset_db__", methods=["POST"])
    def reset_db(token):
        if not validate_token(token):
            return "Invalid token"
        cur.execute("DELETE FROM users WHERE token = ?", (token,))
        cur.execute("DELETE FROM messages WHERE token = ?", (token,))
        tokens_initialized.discard(token)
        return redirect(f"/{token}/", code=302)


    @app.route("/<token>/ctrl-enter/", methods=["POST"])
    def ctrl_enter(token: str):
        if not validate_token(token):
            return "Invalid token"
        init_db(token)
        text = request.form["text"]
        if is_authorized(token):
            login = request.cookies.get("login")
        else:
            login = "(anonymous)"
        cur.execute(
            "INSERT INTO messages (token, user_from, user_to, message) VALUES (?, ?, ?, ?)",
            (token, login, "editor", text)
        )
        cur.execute(
            "INSERT INTO messages (token, user_from, user_to, message) VALUES (?, ?, ?, ?)",
            (token, "editor", login, f"Вы отправили сообщение об ошибке: {text}. Скоро мы его рассмотрим.")
        )
        match = re.search(r"https?://\S+", text)
        if match:
            with open(f"/state/{token}.event", "w") as f:
                f.write(match.group(0))
        return redirect(f"/{token}/", code=302)


    return app
