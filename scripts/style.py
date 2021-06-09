from __future__ import annotations
from typing import *
from . import utils

class Style(object):
    """
    An object representing the color, opacity and font style of an element
    or text in VSCode.

    This object can be generated from a string in the follow format:

        {color}/{opacity}/{font style}
    
    where
    - color can be a valid hex string or name of a color,
    - opacity is the hexadecimal value of the alpha channel
    (between 0 and 0xff)
    - style can be /[ibu]*/.
        - i: Italic
        - b: Bold
        - u: Underline
    """

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
        self.style: Optional[str] = utils.option_string(
            utils.list_get(components, 2)
        )

    def inherit(self, parent: Style) -> Style:
        """
        Fill in the blanks using the style from a parent.
        """
        if self.color is None:
            self.color = parent.color
        if self.opacity is None:
            self.opacity = parent.opacity
        if self.style is None:
            self.style = parent.style

    def get_color(
        self, palette: Dict[str, str], generator_colors: Dict[str, str]
    ) -> Optional[str]:
        """
        Get the hex color value of this style.
        """
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
        """
        Get the font style.
        """
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
