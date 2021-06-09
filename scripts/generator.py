import json
from pathlib import Path
from typing import *
from . import utils


ROOT_PATH = Path(__file__).parents[1].resolve()
PALETTES_PATH = ROOT_PATH / "palettes"
TEMPLATES_PATH = ROOT_PATH / "templates"


def get_palette(name: str) -> Dict[str, str]:
    path = PALETTES_PATH / f"{name}.json"
    return json.load(path.open("r"))


def get_template(name: str) -> Dict[str, str]:
    path = TEMPLATES_PATH / f"{name}.json"
    return json.load(path.open("r"))


def resolve_colors(
    generator_colors: Dict[str, str],
    palette: Dict[str, str],
    max_depth: int = 5
) -> Dict[str, str]:
    """
    Resolve linked-list colors to a name-to-hex dictionary.
    """
    def _valid_filter(kv):
        return utils.check_hex_color(kv[1]) != 0
    united: Dict[str, str] = {
        k: v for k, v in generator_colors.items() | palette.items()
    }
    valid: Set[str] = set(
        map(lambda h: h[0], filter(_valid_filter, united.items()))
    )
    for name, value in united.items():
        depth: int = 0
        if name in valid:
            continue
        elif type(value) != str:
            continue
        color_name = value
        while utils.check_hex_color(united[color_name]) == 0:
            if depth > max_depth and max_depth >= 0:
                raise ValueError(
                    f"Could not find valid hex color value for name: {name}"
                )
            color_name = united[color_name]
            depth += 1
        united[name] = united[color_name]
    return united
