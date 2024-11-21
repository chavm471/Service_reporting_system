import sys
if sys.version_info < (3, 8):
    raise RuntimeError("This program requires Python 3.8 or higher")
import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from dataclasses import dataclass, field # Class helpers, py 3.8+ features that make classes much shorter to write
from typing import *    # Type hinting
from menu import *
from database import *

def main():
    menu_inst = MenuController()
    database = DatabaseManager("chocoDB")

    database.create_tables()

    menu_inst.startmenu()

    return 0

if __name__ == "__main__":
    sys.exit(main())