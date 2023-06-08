from collections import defaultdict
import os
import subprocess
import signal
import sys
import time

from kyzylborda_lib.secrets import get_secret


THROUGHPUT_TIMEOUT = 60


state_dir = sys.argv[1]
host = sys.argv[2]

last_check_by_token = defaultdict(int)
failures_by_token = defaultdict(int)


while True:
    updated_tokens = []
    for file_name in os.listdir(state_dir):
        if file_name.endswith(".event"):
            token = file_name[:-6]
            mtime = os.stat(os.path.join(state_dir, file_name)).st_mtime
            if mtime > last_check_by_token[token] + THROUGHPUT_TIMEOUT:
                updated_tokens.append(token)

    updated_tokens.sort(key=lambda token: last_check_by_token[token])
    for token in updated_tokens:
        with open(os.path.join(state_dir, f"{token}.event")) as f:
            url = f.read()
        password = get_secret("editor_password", token)
        start_time = time.time()
        print(f"Opening {url}", file=sys.stderr, flush=True)

        proc = subprocess.Popen([sys.executable, "openpage.py", url, host, "login=editor", f"password={password}"])

        try:
            try:
                exit_code = proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                # Always reap children
                proc.wait()
                raise
            if exit_code != 0:
                raise Exception(f"Exit code {exit_code}")
        except Exception as e:
            print(token, "Failure", str(e), file=sys.stderr, flush=True)
            failures_by_token[token] += 1
            if failures_by_token[token] >= 3:
                last_check_by_token[token] = start_time
        else:
            print(token, "OK", file=sys.stderr, flush=True)
            last_check_by_token[token] = start_time
            failures_by_token[token] = 0

    time.sleep(3)
