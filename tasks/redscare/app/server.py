from flask import Flask, redirect, render_template, request
from kyzylborda_lib.secrets import get_flag, validate_token
import random
import re
import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix


questions = {}

with open("questions.txt") as f:
    lines = [line.strip() for line in f.read().splitlines()]
    lines = [line for line in lines if line.startswith("| Q: ") or line.startswith("| A: ")]
    for i in range(0, len(lines), 2):
        q, a = lines[i].strip(), lines[i + 1].strip()
        assert q.startswith("| Q: ") and a.startswith("| A: ")
        q, a = q[5:], a[5:]
        questions[q] = a

MIN_QUESTIONS_TO_ANSWER = 200


def clean_string(s: str) -> str:
    return re.sub(r"\W", "", s).strip("_").lower()


def do_answers_match(answer: str, expected_answer: str) -> bool:
    return clean_string(answer).startswith(clean_string(expected_answer))


def make_app(state_dir: str):
    con = sqlite3.connect(f"{state_dir}/answers.db", isolation_level=None)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS answers (token TEXT, question TEXT, UNIQUE (token, question))")
    cur.execute("CREATE INDEX IF NOT EXISTS answers_token ON answers (token)")

    app = Flask(__name__)
    # Required for server to correctly redirect.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    @app.errorhandler(404)
    def page_not_found(e):
        return "Don't forget your token"

    @app.route("/<token>/reply", methods=["POST"])
    def api(token: str):
        if not validate_token(token):
            return "Wrong token"
        question = request.form.get("question", "")
        answer = request.form.get("answer", "")
        if question not in questions:
            return redirect(f"/{token}/?error=Неправильный вопрос", code=302)
        expected_answer = questions[question]
        if not do_answers_match(answer, expected_answer):
            return redirect(f"/{token}/?error=Неправильный ответ", code=302)
        cur.execute("INSERT OR IGNORE INTO answers (token, question) VALUES (?, ?)", (token, question))
        return redirect(f"/{token}/", code=302)

    @app.route("/<token>/")
    def index(token: str):
        if not validate_token(token):
            return "Wrong token"
        error = request.args.get("error", "")
        answered_questions = [row[0] for row in cur.execute("SELECT question FROM answers WHERE token = ?", (token,)).fetchall()]
        percentage = round(len(answered_questions) / MIN_QUESTIONS_TO_ANSWER * 100, 1)
        assert all(q in questions for q in answered_questions)
        questions_left = list(set(questions) - set(answered_questions))
        if questions_left:
            question = random.choice(questions_left)
        else:
            question = "Сожалеем, но вопросы закончились :("
        if len(answered_questions) >= MIN_QUESTIONS_TO_ANSWER and error == "":
            error = f"Поздравляем! Ваш флаг: {get_flag(token)}"
        return render_template("index.html", percentage=percentage, question=question, error=error)

    return app
