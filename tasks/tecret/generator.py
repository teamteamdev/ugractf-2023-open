#!/usr/bin/env python3

import hmac
import json
import sys
import requests
import string

PREFIX = "ugra_test1ng_in_pr0duc7ion_"
FLAG_SECRET = b"WJxDMZ6VzHS_6Dpu82TEH76cadrU"
SUFFIX_SIZE = 12
TOKEN_SECRET = b"Qi23J0TsnZ56OsQKmIaAg21uGXLh"
PASSWORD_SECRET = b"YsLSlxeUP6-UFZcQHKFQqBXhJjTV"
TOKEN_SIZE = 16
PASSWORD_ALPHABET = list(string.ascii_letters + string.digits)


def generate_password(token):
    n = int(
        hmac.new(
            PASSWORD_SECRET,
            token.encode(),
            "sha256",
        ).hexdigest(),
        16,
    )
    ret = []
    while n > 0 and len(ret) < 20:
        n, d = divmod(n, len(PASSWORD_ALPHABET))
        ret.append(PASSWORD_ALPHABET[d])
    return ''.join(ret)


def user_exists(sess, username):
    resp = sess.get(f'{sess.gurl}/api/v4/users', params={'username': username})
    resp.raise_for_status()
    data = resp.json()
    return bool(data)


def create_user(sess, username, password):
    resp = sess.post(
        f'{sess.gurl}/api/v4/users',
        data={
            'admin': False,
            'email': f'{username}@ugractf.ru',
            'username': username,
            'name': username,
            'password': password,
            'private_profile': True,
            'projects_limit': 2,
            'skip_confirmation': True,
        },
    )
    resp.raise_for_status()
    return password


def fork_project(sess, username):
    resp = sess.post(
        f'{sess.gurl}/api/v4/projects/root%2F{sess.template_path}/fork',
        headers={'Sudo': username},
        data={'visibility': 'private'},
    )
    resp.raise_for_status()

def update_variables(sess, username, password):
    resp = sess.post(
        f'{sess.gurl}/api/v4/projects/{username}%2F{sess.template_path}/variables',
        headers={'Sudo': username},
        data={'key': 'SHRON_PASSWORD', 'value': password, 'masked': True},
    )
    resp.raise_for_status()


def init_user(sess, token):
    password = generate_password(token)
    if user_exists(sess, token):
        return token, password
    password = create_user(sess, token, password)
    fork_project(sess, token)
    update_variables(sess, token, password)

    return token, password


def get_user_tokens(user_id):
    token = hmac.new(
        TOKEN_SECRET,
        str(user_id).encode(),
        "sha256",
    ).hexdigest()[:TOKEN_SIZE]
    flag = PREFIX + hmac.new(
        FLAG_SECRET,
        token.encode(),
        "sha256",
    ).hexdigest()[:SUFFIX_SIZE]

    return token, flag


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py secret_file user_id", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        secs = json.load(f)

    sess = requests.Session()
    sess.gurl = secs["url"]
    sess.template_path = secs["template_path"]
    sess.headers["PRIVATE-TOKEN"] = secs["private_token"]
    user_id = sys.argv[2]
    token, flag = get_user_tokens(user_id)

    username, pwd = init_user(sess, token)

    json.dump(
        {
            "flags": [flag],
            "urls": [secs["url"]],
            "bullets": [
                f'Username: {username}, password: {pwd}',
                'SSH port: 2022',
            ]
        },
        sys.stdout,
    )


if __name__ == "__main__":
    generate()
