import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, send_from_directory, render_template, redirect, make_response
import os

from kyzylborda_lib.secrets import get_flag, get_secret, validate_token


class TokenError(ValueError):
    pass


class Weblog:
    def __init__(self, state_dir):
        self.state_dir = state_dir
        self.cursors = {}


    def get_cursor(self, token):
        if not validate_token(token):
            raise TokenError("Invalid token")
        if token not in self.cursors:
            con = sqlite3.connect(f"{self.state_dir}/dbs/{token}.db", isolation_level=None)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, content TEXT, authorized_only BOOLEAN)")
            self.cursors[token] = cur
            if self.get_blog(token, 1) is None:
                self.add_blog(token, "A flag for my fellow subscribers", "admin", get_flag(token), True)
        return self.cursors[token]


    def get_blogs(self, token):
        cur = self.get_cursor(token)
        return [
            {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "content": row[3],
                "authorized_only": row[4]
            }
            for row in cur.execute("SELECT id, title, author, content, authorized_only FROM articles ORDER BY id DESC").fetchall()
        ]


    def get_blog(self, token, blog_id):
        cur = self.get_cursor(token)
        row = cur.execute("SELECT id, title, author, content, authorized_only FROM articles WHERE id = ?", (blog_id,)).fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "content": row[3],
            "authorized_only": row[4]
        }


    def add_blog(self, token, title, author, content, authorized_only):
        cur = self.get_cursor(token)
        cur.execute("INSERT INTO articles (title, author, content, authorized_only) VALUES (?, ?, ?, ?)", (title, author, content, authorized_only))


    def report_blog(self, token, blog_id):
        if blog_id != 1:
            cur = self.get_cursor(token)
            cur.execute("UPDATE articles SET content = ?, authorized_only = ? WHERE id = ?", ("<i>This post has been hidden due to spam reports.</i>", False, blog_id))


    def reset_db(self, token):
        if not validate_token(token):
            raise TokenError("Invalid token")
        try:
            os.unlink(f"{self.state_dir}/dbs/{token}.db")
        except FileNotFoundError:
            pass
        if token in self.cursors:
            del self.cursors[token]


def make_app(state_dir):
    weblog = Weblog(state_dir)

    app = Flask(__name__)
    # Required for server to correctly redirect.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    @app.errorhandler(404)
    def page_not_found(e):
        return f"Don't forget your token: {request.path}"

    @app.route("/<token>/publish", methods=["POST"])
    def publish(token):
        try:
            form = request.form
            weblog.add_blog(token, form["title"], form["author"], form["content"], "authorized_only" in form)
            return redirect(f"/{token}/", code=302)
        except TokenError:
            return "Invalid token"

    @app.route("/<token>/login", methods=["POST"])
    def login(token):
        # Fake login form: the administrator logs on via a token
        return "Wrong login or password"


    @app.route("/<token>/")
    def blogs(token):
        try:
            if request.cookies.get("session") == get_secret("admin", token):
                authorized_login = "admin"
            else:
                authorized_login = None
            resp = make_response(render_template("index.html", blogs=weblog.get_blogs(token), authorized_login=authorized_login))
            resp.headers["Content-Security-Policy"] = "default-src 'none'; frame-src *; img-src *; media-src *; style-src 'self'"
            return resp
        except TokenError:
            return "Invalid token"


    @app.route("/<token>/embed/<post_id>")
    def embed(token, post_id):
        if len(post_id) > 10:
            blog = None
        else:
            try:
                post_id = int(post_id)
            except ValueError:
                blog = None
            else:
                blog = weblog.get_blog(token, int(post_id))

        try:
            if request.cookies.get("session") == get_secret("admin", token):
                authorized_login = "admin"
            else:
                authorized_login = None
        except TokenError:
            return "Invalid token"

        return render_template("embed.html", blog=blog, authorized_login=authorized_login)


    @app.route("/<token>/report/<post_id>")
    def report(token, post_id):
        if len(post_id) < 10:
            try:
                post_id = int(post_id)
            except ValueError:
                pass
            else:
                try:
                    weblog.report_blog(token, post_id)
                except TokenError:
                    return "Invalid token"
        return redirect(f"/{token}/", code=302)


    @app.route("/<token>/__reset_db__", methods=["POST"])
    def reset_db(token):
        try:
            weblog.reset_db(token)
            return redirect(f"/{token}/", code=302)
        except TokenError:
            return "Invalid token"



    return app
