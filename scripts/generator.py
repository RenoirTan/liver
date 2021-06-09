import json
from pathlib import Path
from typing import *
import pprint
from . import style
from . import utils


ROOT_PATH = Path(__file__).parents[1].resolve()
PALETTES_PATH = ROOT_PATH / "palettes"
TEMPLATES_PATH = ROOT_PATH / "templates"
THEMES_PATH = ROOT_PATH / "themes"


def get_palette(name: str) -> Dict[str, str]:
    path = PALETTES_PATH / f"{name}.json"
    return json.load(path.open("r"))


def get_template(name: str) -> Dict[str, str]:
    path = TEMPLATES_PATH / f"{name}.json"
    return json.load(path.open("r"))


def get_theme_base(name: str = "", type: str = "") -> Dict[str, Any]:
    return {
        "name": name,
        "type": type,
        "colors": {},
        "tokenColors": []
    }


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
        k: v for k, v in palette.items() | generator_colors.items()
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


def has_parents(template: Dict[str, Any]) -> bool:
    parents = template["generator"].get("parents", [])
    return len(parents) > 0


def inherit_from_parents(template: Dict[str, Any]) -> Dict[str, Any]:
    """
    TODO: COMPLETE THIS FUNCTION

    Inherit properties from parents if not already defined in the theme
    itself. This checks to see if the parent template has already been
    filled in by searching for {parent name}.i.json under templates/.
    """
    return template
    parents = template["generator"].get("parents", [])
    if len(parents) == 0:
        return template
    for parent_name in parents:
        parent = get_template(parent_name)


def generate(template: Dict[str, Any]) -> Dict[str, Any]:
    template = inherit_from_parents(template)
    output = get_theme_base(template["name"], template["type"])
    palette = get_palette(template["generator"]["palette"])
    colors = resolve_colors(template["generator"]["colors"], palette)
    for scope, value in template["colors"].items():
        color = style.Style(value).get_color(colors)
        if color == None:
            raise ValueError(f"Unknown color: {color}")
        output["colors"][scope] = color
    for group in template["tokenColors"]:
        group = group.copy()
        pprint.pprint(group)
        styling = style.Style(group["settings"])
        color = styling.get_color(colors)
        font_style = styling.get_style()
        settings = {}
        if color is not None:
            settings["foreground"] = color
        if font_style is not None:
            settings["fontStyle"] = font_style
        group["settings"] = settings
        output["tokenColors"].append(group)
    return output
