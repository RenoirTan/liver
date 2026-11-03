from dataclasses import dataclass, KW_ONLY
from liver_scripts.models.base import BaseModel


@dataclass
class TextStyle(BaseModel):
    _: KW_ONLY
    bold: bool = False
    italic: bool = False
    underline: bool = False

    @classmethod
    def parse(cls, literal: str) -> "TextStyle":
        text_style = TextStyle()
        if "b" in literal:
            text_style.bold = True
        if "i" in literal:
            text_style.italic = True
        if "u" in literal:
            text_style.underline = True
        return text_style
