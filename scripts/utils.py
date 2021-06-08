import re
from typing import *


STRING_EMPTY = re.compile("^\s*$")
HEX6 = re.compile("^#[0-9a-f]{6}$")
HEX8 = re.compile("^#[0-9a-f]{8}$")
HEX3 = re.compile("^#[0-9a-f]{3}$")
HEX4 = re.compile("^#[0-9a-f]{4}$")


def is_string_blank(string: str) -> bool:
    return STRING_EMPTY.match(string) is not None


def option_string(string: str) -> Optional[str]:
    return None if is_string_blank(string) else string


def check_hex_color(string: str) -> int:
    if HEX6.match(string):
        return 1
    elif HEX8.match(string):
        return 2
    elif HEX3.match(string):
        return 3
    elif HEX4.match(string):
        return 4
    else:
        return 0


def list_get(array: List[Any], index: int, default: Any = None) -> Any:
    try:
        return array[index]
    except IndexError as e:
        return default
