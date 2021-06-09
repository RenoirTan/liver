import re
from typing import *


STRING_EMPTY = re.compile("^\s*$")
HEX6 = re.compile("^#[0-9a-f]{6}$", flags=re.IGNORECASE)
HEX8 = re.compile("^#[0-9a-f]{8}$", flags=re.IGNORECASE)
HEX3 = re.compile("^#[0-9a-f]{3}$", flags=re.IGNORECASE)
HEX4 = re.compile("^#[0-9a-f]{4}$", flags=re.IGNORECASE)


def is_string_blank(string: str) -> bool:
    """
    Check to see if a string is empty or only has whitespace.
    """
    return STRING_EMPTY.match(string) is not None


def option_string(string: str) -> Optional[str]:
    """
    Convert an string to None if it's blank (i.e. only whitespace),
    otherwise return the original string.
    """
    return None if is_string_blank(string) else string


def check_hex_color(string: str) -> int:
    """
    Check whether a string represents a valid hex colour.
    """
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
    """
    Get an element of an array at a specified index. If the index is out
    of bounds, return a given default value.
    """
    try:
        return array[index]
    except IndexError as e:
        return default
