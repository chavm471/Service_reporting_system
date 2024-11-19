import sys
if sys.version_info < (3, 8):
    raise RuntimeError("This program requires Python 3.8 or higher")
import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from dataclasses import dataclass, field # Class helpers, py 3.8+ features that make classes much shorter to write
from typing import *    # Type hinting

def main():

    print("select what mode you want")
    print("1.Operator mode")
    print("2. Provider Mode")
    mode = input()

    #operator mode
    if mode == 1:
        member_num = input("enter you membership number")
    #provider mode
    if mode == 2:
        provider_num = input("enter you provider number")

    return 0

if __name__ == "__main__":
    sys.exit(main())