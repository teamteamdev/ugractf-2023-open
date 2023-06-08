#!/usr/bin/env python3

import sys
import json
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def byte_xor(ba1, ba2):
    return bytes((a ^ b for a, b in zip(ba1, ba2)))

def pairs_hook(pairs):
    ret = dict(pairs)
    if len(ret) < len(pairs):
        return pairs
    else:
        return ret

def get_from_pairs(pairs, key):
    if isinstance(pairs, dict):
        return [pairs[key]]
    else:
        return [p[1] for p in pairs if p[0] == key]

with open(sys.argv[1]) as f:
    pkts = json.load(f, object_pairs_hook=pairs_hook)

REGEX = re.compile(r"sequence is ([0-9a-f]+)")

out = ""
key = b"\0" * 32

key_node = None
key_count = 0

for pkt in pkts:
    try:
        msg = pkt["_source"]["layers"]["erldp"]["Message"]["SMALL_TUPLE_EXT"]
        arity = int(get_from_pairs(msg, "erldp.arity")[0])
    except (KeyError, TypeError, IndexError):
        continue

    def get_nth_binary(i):
        raw_binary = get_from_pairs(msg, "BINARY_EXT")[i]["erldp.binary_ext"]
        return bytes.fromhex(raw_binary.replace(":", ""))

    if arity == 2:
        try:
            new_key = get_nth_binary(0)
        except (KeyError, TypeError, IndexError):
            continue
        if len(key) != 32:
            continue
        ip_hosts = get_from_pairs(pkt["_source"]["layers"]["ip"], "ip.host")
        if key_node is None:
            key_node = ip_hosts[0]
        elif key_node != ip_hosts[1]:
            continue
        key = byte_xor(key, new_key)
        key_count += 1
        print("XORed key")
    elif arity == 4 and key_count >= 11:
        try:
           iv = get_nth_binary(0)
           encrypted = get_nth_binary(1)
        except (KeyError, TypeError, IndexError):
            continue
        decryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()
        msg = decryptor.update(encrypted) + decryptor.finalize()
        print(msg)
        try:
            text = msg.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if match := REGEX.search(text):
            seq = match[1]
        else:
            continue
        part = bytes.fromhex(seq).decode("utf-8")
        out += part
    else:
        continue

print(out)
