from __future__ import annotations
from typing import *
from . import utils

class Style(object):
    def __init__(self, literal: str) -> None:
        components = literal.split("/")
        self.color: Optional[str] = utils.option_string(
            utils.list_get(components, 0)
        )
        opacity = utils.list_get(components, 1)
        self.opacity: Optional[int] = None if opacity is None else int(opacity)
        if not (0 <= self.opacity <= 0xFF):
            raise ValueError(
                f"opacity must be between 0 and 255: {self.opacity}"
            )
        self.style: Optional[str] = utils.option_string(utils.list_get(components, 2))

    def inherit(self, parent: Style) -> Style:
        if self.color is None:
            self.color = parent.color
        if self.opacity is None:
            self.opacity = parent.opacity
        if self.style is None:
            self.style = parent.style

    def get_color(
        self, palette: Dict[str, str], generator_colors: Dict[str, str]
    ) -> Optional[str]:
        if self.color is None:
            return None
        color = self.color
        while utils.check_hex_color(color) == 0:
            tentative = generator_colors.get(color, None)
            if tentative is None:
                tentative = palette.get(color, None)
                if tentative is None:
                    raise ValueError(f"Could not find color: {color}")
            color = tentative
        if self.opacity is not None:
            color += hex(self.opacity)[2:]
        return color
    
    def get_style(self) -> Optional[str]:
        if self.style is None:
            return None
        style = []
        if "i" in self.style:
            style.append("italic")
        if "b" in self.style:
            self.append("bold")
        if "u" in self.style:
            self.append("underline")
        return " ".join(style)
