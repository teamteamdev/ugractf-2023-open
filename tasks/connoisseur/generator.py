#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


import os
import random
import re
import shutil
import subprocess
import tempfile


class Inserter():
    def __init__(self, text):
        self.bits = "".join(f"{b:08b}" for b in text.encode())
        self.pos = -1 

    def add_class(self, m):
        self.pos += 1
        if self.pos >= len(self.bits):
            return "h"
        return "a" if self.bits[self.pos] == "1" else "h"

def wrap_letters(m):
    def _wrap_letter(m):
        return f"<tspan class=\"~~~\">{m.group(0)}</tspan>"

    return re.compile("&[#]?[a-zA-Z0-9]+;|[^ ]").sub(_wrap_letter, m.group(1))


def generate():
    flag = get_flag()

    text = open(os.path.join("private", "source.svg")).read()
    text = re.compile("\\*([^<]*)").sub(wrap_letters, text)

    inserter = Inserter(flag)
    text = re.compile("~~~").sub(inserter.add_class, text)

    with tempfile.TemporaryDirectory() as temp_dir:
        open(os.path.join(temp_dir, "f.svg"), "w").write(text)

        display = random.randint(100000, 999999)
        with subprocess.Popen(f"Xvfb :{display}", shell=True) as p:
            try:
                # add path-combine after object-to-path for more task complexity
                env = {**os.environ, "FONTCONFIG_FILE": os.path.abspath(os.path.join("private", "fonts.conf"))}
                subprocess.check_call(f"DISPLAY=:{display} inkscape --with-gui --batch-process "
                                       "--actions='select-all;object-to-path' --export-overwrite f.svg",
                                       shell=True, cwd=temp_dir, env=env)
                subprocess.check_call("inkscape --export-filename=f.pdf f.svg",
                                      shell=True, cwd=temp_dir, env=env)
            finally:
                p.terminate()

        shutil.copy(os.path.join(temp_dir, "f.pdf"),
                    os.path.join(get_attachments_dir(), "FOR IMMEDIATE RELEASE.pdf"))


if __name__ == "__main__":
    generate()
