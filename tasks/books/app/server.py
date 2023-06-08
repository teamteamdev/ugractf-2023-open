from flask import Flask, render_template, request, send_file
import os
import shutil
import subprocess


def make_app():
    app = Flask(__name__)

    @app.route("/<token>/", methods=["GET"])
    def index(token):
        return render_template("index.html")


    session_id = 0

    @app.route("/<token>/convert", methods=["POST"])
    def convert(token):
        nonlocal session_id
        session_id += 1

        os.mkdir(f"/tmp/epub-{session_id}")

        try:
            with open(f"/tmp/epub-{session_id}/book.epub", "wb") as f:
                request.files["source"].save(f)

            proc = subprocess.run(
                [os.path.join(os.path.dirname(os.path.abspath(__file__)), "convert.py")],
                cwd=f"/tmp/epub-{session_id}",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            log = proc.stdout.decode(errors="ignore")

            dl_link = ""
            if proc.returncode == 0:
                try:
                    with open(f"/tmp/epub-{session_id}/out-path.txt") as f:
                        out_path = f.read()
                except FileNotFoundError:
                    return "ERROR: out-path.txt does not exist"
                dl_link = "download/" + out_path.removeprefix("/tmp/converted/")
        finally:
            shutil.rmtree(f"/tmp/epub-{session_id}")

        return render_template(
            "result.html",
            dl_link=dl_link,
            log=log
        )


    @app.route("/<token>/download/<path>")
    def download(token, path):
        return send_file("/tmp/converted" + os.path.normpath("/" + path))

    return app
