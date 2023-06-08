import hashlib

from kyzylborda_lib.sandbox import Box, start_box
from kyzylborda_lib.secrets import validate_token, get_flag
from kyzylborda_lib.server import http


def init(box: Box) -> None:
    with box.open("/etc/key", "wb") as f:
        f.write(hashlib.sha512(f"{box.token}-ucucuga-ragu-ug-secret".encode()).digest())

    with box.open("/flag.txt", "w") as f:
        f.write(get_flag(box.token))


@http.listen
async def handle(request: http.Request):
    token = request.path[1:].partition("/")[0]
    if not validate_token(token):
        return http.respond(404)
    if "X-Forwarded-Host" in request.headers:
        del request.headers["Host"]
        request.headers["Host"] = request.headers["X-Forwarded-Host"]
    return await start_box(token, init=init, pass_secrets=["flag"])
