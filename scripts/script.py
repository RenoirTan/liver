import json
from pathlib import Path
from typing import *
from pprint import pprint
from . import generator
from . import registrar


def show_resolved_colors(name: str) -> Dict[str, str]:
    template = generator.get_template(name)
    palette = generator.get_palette(template["generator"]["palette"])
    template_colors = template["generator"]["colors"]
    resolved = generator.resolve_colors(template_colors, palette)
    pprint(resolved)
    return resolved


def generate(*names: str) -> int:
    for name in names:
        print(f"Generating: {name}...", end="")
        template = generator.get_template(name)
        output = generator.generate_theme(template)
        json.dump(
            output,
            Path(generator.THEMES_PATH / (name + ".json")).open("w"),
            indent=4
        )
        print(" ✓")
    return 0


def register(*names: str) -> int:
    for name in names:
        print(f"Registering {name} to package.json...", end="")
        registrar.register(name)
        print(" ✓")
    return 0


def remove(*names: str) -> int:
    for name in names:
        print(f"Removing {name} from package.json...", end="")
        registrar.remove(name)
        print(" ✓")
    return 0
