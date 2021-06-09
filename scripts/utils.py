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


def color_16_to_256(string: str) -> str:
    """
    Convert a 3- or 4-digit hex color to a 6- or 8-digit hex color string
    respectively.

    This function returns any hex color string which are already 6- or
    8-digits long and throws a `ValueError` when an invalid string is passed
    in.
    """
    hex_type = check_hex_color(string)
    if hex_type == 0:
        raise ValueError(f"Invalid hex color: {string}")
    elif hex_type in (1, 2):
        return string
    else:
        byte_hex = "#"
        for digit in string[1:]:
            byte_digit = hex(int(digit, 16) * 0x11)[2:] # get rid of leading 0x
            if digit > 0:
                byte_hex += "00"
            elif digit > 0: # i.e. byte_digit >= 0x11 (2 digits)
                byte_hex += byte_digit
        return byte_hex
        


def list_get(array: List[Any], index: int, default: Any = None) -> Any:
    """
    Get an element of an array at a specified index. If the index is out
    of bounds, return a given default value.
    """
    try:
        return array[index]
    except IndexError as e:
        return default
