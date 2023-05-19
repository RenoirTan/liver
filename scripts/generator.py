import json
from pathlib import Path
from typing import *
import pprint
from .info import *
from .style import Style
from .token_color import TokenColor
from . import utils


T = TypeVar("T")
H = TypeVar("H", bound=Hashable)


def get_palette(name: str) -> Dict[str, str]:
    path = PALETTES_PATH / f"{name}.json"
    return json.load(path.open("r"))


def get_template(name: str) -> Dict[str, str]:
    path = TEMPLATES_PATH / f"{name}.json"
    return json.load(path.open("r"))


def get_theme_base(
    name: str = "",
    type: str = "",
    semantic_highlighting: Optional[bool] = None
) -> Dict[str, Any]:
    theme = {
        "name": name,
        "type": type,
        "colors": {},
        "tokenColors": []
    }
    if semantic_highlighting is not None:
        theme["semanticHighlighting"] = semantic_highlighting
    return theme


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


def theme_has_parents(template: Dict[str, Any]) -> bool:
    parents = template["generator"].get("parents", [])
    return len(parents) > 0


def combine_dicts_with_overwrite(first: Dict, second: Dict) -> Dict:
    for k, v in second.items():
        first[k] = v
    return first


def combine_sets(first: Set, second: Set) -> Set:
    for item in second:
        first.add(item)


def list_find_hash(array: List[H], target: H) -> List[int]:
    indices: List[int] = []
    for index, element in enumerate(array):
        if hash(element) == hash(target):
            indices.append(index)
    return indices


def list_set_add(array: List[H], element: H) -> List[H]:
    indices = list_find_hash(array, element)
    if len(indices) > 0:
        for offset, index in enumerate(indices):
            array.pop(index - offset)
    array.append(element)
    return array


def theme_inherit_from_parents(template: Dict[str, Any]) -> Dict[str, Any]:
    """
    TODO: COMPLETE THIS FUNCTION

    Inherit properties from parents if not already defined in the theme
    itself. This checks to see if the parent template has already been
    filled in by searching for {parent name}.i.json under templates/.
    """
    parents = template["generator"].get("parents", [])
    if len(parents) == 0:
        return template
    generator_colors: Dict[str, str] = {}
    colors: Dict[str, str] = {}
    token_colors: List[TokenColor] = []

    def _add_template(_template: Dict[str, Any]):
        nonlocal generator_colors, colors, token_colors
        combine_dicts_with_overwrite(
            generator_colors, _template["generator"].get("colors", {})
        )
        combine_dicts_with_overwrite(colors, _template["colors"])
        for group in _template["tokenColors"]:
            token_color = TokenColor(group)
            list_set_add(token_colors, token_color)

    for parent_name in parents:
        parent = get_template(parent_name)
        parent = theme_inherit_from_parents(parent) # Recursion
        _add_template(parent)
    _add_template(template)
    template["generator"]["colors"] = generator_colors
    template["colors"] = colors
    for index, token_color in enumerate(token_colors):
        token_colors[index] = token_color.to_dict()
    template["tokenColors"] = token_colors
    return template


def generate_theme(template: Dict[str, Any]) -> Dict[str, Any]:
    template = theme_inherit_from_parents(template)
    output = get_theme_base(
        template["name"],
        template["type"],
        template.get("semanticHighlighting")
    )
    palette = get_palette(template["generator"]["palette"])
    colors = resolve_colors(template["generator"]["colors"], palette)
    for scope, value in template["colors"].items():
        color = Style(value).get_color(colors)
        if color == None:
            raise ValueError(f"Unknown color: {color}")
        output["colors"][scope] = color
    for group in template["tokenColors"]:
        group = group.copy()
        styling = Style(group["settings"])
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
