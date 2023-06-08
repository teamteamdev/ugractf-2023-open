import sys
import json

import hmac

TOKEN_SECRET = b"d2986f83a5fa271ff87fd135bfb302e32fda"
FLAG_SECRET = b"32800d6a5df0b7dc5b51ca6da8db949a94bd"
TOKEN_SIZE = 12
SUFFIX_SIZE = 12
PREFIX = "ugra_cr0zy_sc1nce_run_0ut_"

def gen_flag(user_id):
    token = hmac.new(TOKEN_SECRET, str(user_id).encode(), "sha256").hexdigest()[:TOKEN_SIZE]
    flag = PREFIX + hmac.new(FLAG_SECRET, token.encode(), "sha256").hexdigest()[:SUFFIX_SIZE]
    return token, flag

def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]

    token, flag = gen_flag(user_id)

    json.dump({
        "flags": [flag],
        "urls": [f"https://noteotp.{{hostname}}/{token}/"]
    }, sys.stdout)

if __name__ == "__main__":
    generate()
