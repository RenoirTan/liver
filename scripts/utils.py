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


def hex_byte_str(value: int) -> str:
    """
    Convert a "char" to a hexadecimal number.
    """
    if not (0 <= value <= 0xFF):
        raise ValueError(f"value must be between 0 and 255: {value}")
    hex_value = hex(value)[2:]
    if value < 0x10:
        hex_value = "0" + hex_value
    return hex_value


def check_hex_color(string: str) -> int:
    """
    Check whether a string represents a valid hex colour.
    """
    if type(string) != str:
        return 0
    elif HEX6.match(string):
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


def set_opacity(string: str, opacity: int) -> str:
    """
    Set the opacity of a hex color string.

    This function raises ValueError if the hex color string only has 3 or
    4 digits because it can't tell whether to multiply opacity by 0x11.
    """
    hex_type = check_hex_color(string)
    if hex_type not in (1, 2):
        raise ValueError(f"Incompatible hex string: {string}")
    hex_opacity = hex_byte_str(opacity)
    if hex_type == 1:
        return string + hex_opacity
    else:
        return string[:-2] + hex_opacity


def list_get(array: List[Any], index: int, default: Any = None) -> Any:
    """
    Get an element of an array at a specified index. If the index is out
    of bounds, return a given default value.
    """
    try:
        return array[index]
    except IndexError as e:
        return default
