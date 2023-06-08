#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, validate_token
from kyzylborda_lib.server import tcp
import os
import searcher
import tempfile
import zipfile


@tcp.listen
async def handle(conn: tcp.Connection):
    await conn.writeall("Введите токен. > ".encode())
    token = (await conn.readline()).decode(errors="ignore").strip()
    if not validate_token(token):
        await conn.writeall("Токен неверен, в доступе отказано. До свидания.\n".encode())
        return

    with tempfile.TemporaryDirectory() as d: 
        with zipfile.ZipFile("archive.zip", "r") as f:
            for fn in f.filelist:
                open(os.path.join(d, fn.filename), "wb").write(f.read(fn).replace(b"+++", get_flag(token).encode()))

        s = searcher.Searcher(conn, token, d)
        await s.iterate_commands()
