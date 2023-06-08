from kyzylborda_lib.secrets import get_flag, validate_token
from kyzylborda_lib.server import http


@http.listen
async def handle(request: http.Request):
    token = request.path[1:].partition("/")[0]
    if not validate_token(token):
        return http.respond(404)
    return http.respond(200, get_flag(token))
