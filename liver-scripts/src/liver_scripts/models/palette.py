import copy
from dataclasses import dataclass, field
from liver_scripts.models.base import BaseModel, BaseDependent
from liver_scripts.models.color import validate_hex_color


@dataclass
class Palette(BaseModel, BaseDependent):
    """
    Represents a color palette.
    Keys of `colors` are the name of each color
    while values are the hex value of the color or the name of another color.
    """

    name: str
    parents: list[str] = field(default_factory=list)
    colors: dict[str, str] = field(default_factory=dict)

    @classmethod
    def blank(cls):
        return cls(name="", parents=[], colors={})

    def inherit_mutably(self, parents: list["Palette"]) -> "Palette":
        for parent in parents:
            for name, new_color in parent.colors.items():
                self.colors[name] = self.colors.get(name) or new_color
        return self

    def inherit(self, parents: list["Palette"]) -> "Palette":
        return copy.deepcopy(self).inherit_mutably(parents)

    def resolve_mutably(self) -> "Palette":
        unresolved = set[str]()
        unresolved_iterator = filter(
            lambda kv: not validate_hex_color(kv[1], throw=False), self.colors.items()
        )
        for name, color in unresolved_iterator:
            unresolved.add(name)
            if color not in self.colors:
                raise ValueError(f"{color} could not be resolved to a color")
        loop_counter = 0
        while len(unresolved) >= 1:
            if loop_counter > 100:
                raise ValueError("Too many loops!")
            for name in set(unresolved):
                color = self.colors[name]
                new_color = self.colors[color]
                if validate_hex_color(new_color, throw=False):
                    unresolved.remove(name)
                self.colors[name] = new_color
            loop_counter += 1
        return self

    def resolve(self) -> "Palette":
        return copy.deepcopy(self).resolve_mutably()
