from liver_scripts.utils.graph import build_dependency_graph, get_dependency_list
import copy
from dataclasses import dataclass, field
import networkx as nx
from liver_scripts.models.base import BaseModel, BaseDependent
from liver_scripts.models.color import validate_hex_color


@dataclass
class BasePalette(BaseModel):
    name: str
    colors: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        pass


@dataclass
class ResolvedPalette(BasePalette):
    name: str
    colors: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        for color in self.colors.values():
            validate_hex_color(color)

    @classmethod
    def blank(cls):
        return cls(name="", colors={})


@dataclass
class Palette(BasePalette, BaseDependent):
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

    def inherit_mutably(self, parents: dict[str, BasePalette]) -> "Palette":
        for parent_name in self.parents:
            parent = parents[parent_name]
            for name, new_color in parent.colors.items():
                self.colors[name] = self.colors.get(name) or new_color
        return self

    def inherit(self, parents: dict[str, BasePalette]) -> "Palette":
        return copy.deepcopy(self).inherit_mutably(parents)

    def resolve(self) -> "ResolvedPalette":
        unresolved = set[str]()
        unresolved_iterator = filter(
            lambda kv: not validate_hex_color(kv[1], throw=False), self.colors.items()
        )
        for name, color in unresolved_iterator:
            unresolved.add(name)
            if color not in self.colors:
                raise ValueError(f"{color} could not be resolved to a color")
        colors = copy.deepcopy(self.colors)
        loop_counter = 0
        while len(unresolved) >= 1:
            if loop_counter > 100:
                raise ValueError("Too many loops!")
            for name in set(unresolved):
                color = colors[name]
                new_color = colors[color]
                if validate_hex_color(new_color, throw=False):
                    unresolved.remove(name)
                colors[name] = new_color
            loop_counter += 1
        return ResolvedPalette(self.name, colors)


def inherit_palettes(palettes: dict[str, Palette]) -> dict[str, Palette]:
    G = build_dependency_graph(list(palettes.values()))
    cycles = nx.simple_cycles(G)
    for _ in cycles:
        raise ValueError(f"Dependency cycle detected in palettes: {cycles}")
    sorted_palettes = get_dependency_list(G)
    updated_palettes = dict[str, Palette]()
    for name in sorted_palettes:
        palette = palettes[name]
        parents: dict[str, BasePalette] = {
            p: updated_palettes[p] for p in palette.parents
        }
        updated_palettes[name] = palette.inherit(parents)
    return updated_palettes
