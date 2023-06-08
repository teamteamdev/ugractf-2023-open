#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_token

import os

def generate():
    with open(os.path.join(get_attachments_dir(), "sdc.img"), "wb") as f:
        f.write(open(os.path.join("private", "alpine-ready.img"), "rb").read()
                .replace(b"XXXXXXXXXXXXXXXX", get_token().encode()))


if __name__ == "__main__":
    generate()
