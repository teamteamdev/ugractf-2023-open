import re
import socket


TOKEN = "i6cnsxvi19pqovqz"


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("deepend.o.2023.ugractf.ru", 5917))


buf = b""

def waitfor(s):
    global buf
    s = s.encode()
    while s not in buf:
        part = sock.recv(4096)
        print(part.decode(), end="", flush=True)
        buf += part
    pos = buf.find(s)
    match = buf[:pos + len(s)].decode()
    buf = buf[pos + len(s):]
    return match


def run(s):
    sock.sendall(s.encode() + b"\n")
    print(s)
    return waitfor("❯\x1b[0m ")


sock.recv(4096)
sock.sendall(TOKEN.encode() + b"\n")
waitfor("❯\x1b[0m ")

run("ssh 10.0.0.13")
run("buy-software brute-password")

malware = None
funds = 0
known_hosts = set()
infected_hosts = set()

def brute_auth(login):
    brute = run(f"brute-password {login}")
    if "forensics" in brute:
        run("exit")
        run("ssh 10.0.0.13")
        run("buy-software cover-tracks")
        run("cover-tracks")
        run("exit")
        run(f"ssh {ip}")
        brute = run(f"brute-password {login}")
    password = brute.partition("\x1b[1m")[2].partition("\x1b[0m")[0]
    run(f"login {login} {password}")

while True:
    jobs = run("jobs")
    job_list = []
    for line in jobs.split("\n"):
        if "$" in line:
            num = int(line.partition("\x1b[32m")[2].partition("\x1b[0m")[0])
            reward = int(line.partition("\x1b[34m")[2].partition("\x1b[0m")[0])
            if (
                "Purge" in line
                or "Steal" in line
                or ("Infect" in line and (malware is not None or funds >= 4000))
                or ("Crash" in line and (malware is not None or funds >= 4000) and len(known_hosts) >= 20)
            ):
                job_list.append((reward, num))
    reward, num = max(job_list)

    desc = run(f"apply-job {num}")
    highlights = [part.partition("\x1b[0m")[0] for part in desc.split("\x1b[32m")[1:]]

    if "Delete" in desc or "Download" in desc:
        login, ip, file, *_ = highlights
        known_hosts.add(ip)
        run("exit")
        run(f"ssh {ip}")
        brute_auth(login)
        if "Delete" in desc:
            # In case we need it later
            run(f"download {file}")
            run(f"rm {file}")
        else:
            run(f"download {file}")
        run("exit")
        run("exit")
    elif "Install a backdoor" in desc:
        login, ip, *_ = highlights
        known_hosts.add(ip)
        if malware is None:
            run("buy-software inject-code")
            run("buy-software generate-malware")
            run("exit")
            malware = run("generate-malware").partition("\x1b[32m")[2].partition("\x1b[0m")[0]
        else:
            run("exit")
        run(f"ssh {ip}")
        brute_auth(login)
        run(f"inject-code {malware}")
        infected_hosts.add(ip)
        run("exit")
        run("exit")
    elif "DoS" in desc:
        ip, *_ = highlights
        known_hosts.add(ip)
        run("buy-software brute-tcp")
        run("exit")

        for host in known_hosts:
            if len(infected_hosts) >= 19:
                break
            if host in infected_hosts:
                continue
            run(f"ssh {host}")
            brute_auth("admin")
            run(f"inject-code {malware}")
            infected_hosts.add(host)
            run("exit")
            run("exit")

        run(f"brute-tcp {ip}")
    else:
        raise SystemExit(1)

    funds = int(run("funds").partition("\x1b[34m")[2].partition("\x1b[0m")[0])
    funds += reward

    run("ssh 10.0.0.13")
    run("submit-job")

waitfor("\x00")
