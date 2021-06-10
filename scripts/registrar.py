import json
from pathlib import Path
from typing import *
from .info import *


THEME_TYPES: Dict[str, str] = {
    "dark": "vs-dark",
    "light": "vs",
    "contrast": "hc-black"
}


def find_theme(label: str, themes: List[Dict[str, str]]) -> int:
    for index, theme in enumerate(themes):
        if theme["label"] == label:
            return index
    return -1


def register(name: str) -> int:
    path = THEMES_PATH / f"{name}.json"
    theme = json.load(path.open("r"))
    label = theme["name"]
    ui_theme = THEME_TYPES[theme["type"]]
    theme_path = f"./themes/{name}.json"
    package_json = json.load((ROOT_PATH / "package.json").open("r"))
    index = find_theme(label, package_json["contributes"]["themes"])
    if index >= 0:
        package_json["contributes"]["themes"].pop(index)
    package_json["contributes"]["themes"].append({
        "label": label,
        "uiTheme": ui_theme,
        "path": theme_path
    })
    json.dump(package_json, (ROOT_PATH / "package.json").open("w"))
    return 0


def remove(name: str) -> int:
    package_json = json.load((ROOT_PATH / "package.json").open("r"))
    index = find_theme(name, package_json["contributes"]["themes"])
    if index >= 0:
        package_json["contributes"]["themes"].pop(index)
        json.dump(package_json, (ROOT_PATH / "package.json").open("w"))
    return 0
