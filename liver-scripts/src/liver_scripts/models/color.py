import re
from liver_scripts.utils import index_first


HEX6 = re.compile("^#[0-9a-f]{6}$", flags=re.IGNORECASE)
HEX8 = re.compile("^#[0-9a-f]{8}$", flags=re.IGNORECASE)
HEX3 = re.compile("^#[0-9a-f]{3}$", flags=re.IGNORECASE)
HEX4 = re.compile("^#[0-9a-f]{4}$", flags=re.IGNORECASE)
HEXES = [HEX6, HEX8, HEX3, HEX4]


def validate_hex_color(input: str, *, throw: bool = True) -> bool:
    index = index_first(HEXES, lambda r: r.match(input) is not None)
    result = index != -1
    if not result and throw:
        raise ValueError(f"{input} is not a valid color hex")
    return result
