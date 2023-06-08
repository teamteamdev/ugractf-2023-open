#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, validate_token
import os

os.environ["TASK_NAME"] = "repeatafterme"

try:
    token = os.environ["AUTH"]
    if validate_token(token):
        print("You may take note of the following information:\n" + get_flag(token))
    else:
        print("The provided authentication token is incorrect.")
except:
    print("Not enough information provided for authentication.")
