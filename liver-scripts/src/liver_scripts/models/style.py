import copy
from dataclasses import dataclass, field
from liver_scripts.models.base import BaseModel
from liver_scripts.models.color import validate_hex_color
from liver_scripts.models.palette import Palette, BasePalette
from liver_scripts.models.text_style import TextStyle


@dataclass
class BaseStyle(BaseModel):
    def to_partial(self) -> "PartialStyle":
        raise NotImplementedError()


@dataclass
class Style(BaseStyle):
    """
    A combination of color, opacity and text_style that
    an element/text can have.
    """

    color: str
    opacity: int = 0xFF
    text_style: TextStyle = field(default_factory=TextStyle)

    def __post_init__(self):
        pass

    def to_partial(self) -> "PartialStyle":
        return PartialStyle(
            color=self.color,
            opacity=self.opacity,
            text_style=self.text_style,
        )

    def resolve_color(self, palette: BasePalette) -> str | None:
        if validate_hex_color(self.color, throw=False):
            return self.color
        else:
            return palette.colors.get(self.color)

    def resolve(self, palette: BasePalette | None = None) -> "ResolvedStyle":
        palette = palette or Palette.blank()
        resolved_color = self.resolve_color(palette)
        if resolved_color is None:
            raise ValueError(f"Could not find {self.color} in palette {palette.name}")
        return ResolvedStyle(
            color=resolved_color,
            opacity=self.opacity,
            text_style=copy.copy(self.text_style),
        )


@dataclass
class ResolvedStyle(Style):
    def __post_init__(self):
        super().__post_init__()
        validate_hex_color(self.color)


@dataclass
class PartialStyle(BaseStyle):
    color: str | None = None
    opacity: int | None = None
    text_style: TextStyle | None = None

    def __post_init__(self):
        if self.opacity is not None:
            assert 0 <= self.opacity <= 255

    @classmethod
    def parse(cls, input: str) -> "PartialStyle":
        components = input.split("/")
        n_components = len(components)
        color = components[0].strip() or None
        raw_opacity = (components[1].strip() or None) if n_components >= 2 else None
        opacity = int(raw_opacity, 16) if raw_opacity is not None else None
        raw_text_style = (components[2].strip() or None) if n_components >= 3 else None
        text_style = (
            TextStyle.parse(raw_text_style) if raw_text_style is not None else None
        )
        return PartialStyle(color=color, opacity=opacity, text_style=text_style)

    def to_partial(self) -> "PartialStyle":
        return copy.deepcopy(self)

    def to_full(self) -> Style:
        if self.color is None:
            raise ValueError("self.color is None")
        opacity = 0xFF if self.opacity is None else self.opacity
        text_style = TextStyle() if self.text_style is None else self.text_style
        return Style(self.color, opacity, text_style)

    def inherit_mutably(self, parent: "PartialStyle") -> "PartialStyle":
        self.color = self.color or parent.color
        self.opacity = self.opacity if self.opacity is not None else parent.opacity
        self.text_style = (
            self.text_style if self.text_style is not None else parent.text_style
        )
        return self

    def inherit(self, parent: "PartialStyle") -> "PartialStyle":
        return copy.deepcopy(self).inherit_mutably(parent)
