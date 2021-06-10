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
        self.opacity: Optional[int] = None if utils.is_string_blank(
            opacity
        ) else int(opacity, 16)
        if self.opacity is not None and not (0 <= self.opacity <= 0xFF):
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
        self, palette: Dict[str, str]
    ) -> Optional[str]:
        """
        Get the hex color value of this style.
        """
        if self.color is None:
            return None
        color = palette.get(self.color, None)
        if color is None:
            raise ValueError(f"Could not find color named '{self.color}'")
        # Convert 3/4 digit to 6/8 digit
        color = utils.color_16_to_256(color)
        if self.opacity is not None:
            color = utils.set_opacity(color, self.opacity)
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
            style.append("bold")
        if "u" in self.style:
            style.append("underline")
        return " ".join(style)
