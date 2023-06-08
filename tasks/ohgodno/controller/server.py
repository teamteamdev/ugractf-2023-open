from kyzylborda_lib.sandbox import start_box
from kyzylborda_lib.server import udp


@udp.listen
async def handle(conn: udp.Connection):
    return await start_box(conn.peer_address)
