import json
from pathlib import Path
from typing import *
from pprint import pprint
from . import generator


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
        output = generator.generate(template)
        json.dump(
            output,
            Path(generator.THEMES_PATH / (name + ".json")).open("w")
        )
        print(" ✓")
    return 0
