import copy
from dataclasses import dataclass, field
import networkx as nx
from liver_scripts.models.base import BaseModel, BaseDependent
from liver_scripts.models.component import Component, ResolvedComponent
from liver_scripts.models.palette import Palette
from liver_scripts.utils.graph import build_dependency_graph, get_dependency_list


@dataclass
class ResolvedTemplate(BaseModel, BaseDependent):
    """
    A combination of color palette and component styles
    """

    name: str
    parents: list[str] = field(default_factory=list)
    palettes: dict[str, Palette] = field(default_factory=dict)
    components: dict[str, ResolvedComponent] = field(default_factory=dict)
    palette_roles: dict[str, str] = field(default_factory=dict)
    component_roles: dict[str, str] = field(default_factory=dict)


@dataclass
class Template(BaseModel, BaseDependent):
    name: str
    parents: list[str] = field(default_factory=list)
    palettes: dict[str, Palette] = field(default_factory=dict)
    components: dict[str, Component] = field(default_factory=dict)
    palette_roles: dict[str, str] = field(default_factory=dict)
    component_roles: dict[str, str] = field(default_factory=dict)

    @property
    def palette_names(self) -> list[str]:
        return list(self.palettes.keys())

    @property
    def component_names(self) -> list[str]:
        return list(self.components.keys())

    def _inherit_palettes_mutably(self, parent_palettes: list[Palette]):
        for parent_palette in parent_palettes:
            if (name := parent_palette.name) not in self.palettes:
                self.palettes[name] = copy.deepcopy(parent_palette)

    def _inherit_components_mutably(self, parent_components: list[Component]):
        for parent_component in parent_components:
            if (name := parent_component.name) not in self.components:
                self.components[name] = copy.deepcopy(parent_component)

    def inherit_mutably(self, parents: list["Template"]) -> "Template":
        parent_palettes = list[Palette]()
        parent_components = list[Component]()
        for parent in parents:
            parent_palettes.extend(parent.palettes)
            parent_components.extend(parent.components)
        self._inherit_palettes_mutably(parent_palettes)
        self._inherit_components_mutably(parent_components)
        return self

    def inherit(self, parents: list["Template"]) -> "Template":
        return copy.deepcopy(self).inherit_mutably(parents)

    def _resolve_palettes_mutably(self):
        G = build_dependency_graph(list(self.palettes.values()))
        cycles = nx.simple_cycles(G)
        if len(cycles) >= 1:
            raise ValueError(f"Dependency cycle detected in palettes: {cycles}")
        sorted_palettes = get_dependency_list(G)
        for name in sorted_palettes:
            palette = self.palettes[name]
            parents = [self.palettes[p] for p in palette.parents]
            palette.inherit_mutably(parents)
        for palette in self.palettes.values():
            palette.resolve_mutably()

    def _resolve_components_mutably(self):
        G = build_dependency_graph(list(self.components.values()))
        cycles = nx.simple_cycles(G)
        if len(cycles) >= 1:
            raise ValueError(f"Dependency cycle detected in components: {cycles}")
        sorted_components = get_dependency_list(G)
        for name in sorted_components:
            component = self.components[name]
            parents = [self.components[p] for p in component.parents]
            component.inherit_mutably(parents)
        for name, component in self.components.items():
            pass

    def resolve_mutably(self) -> "Template":
        self._resolve_palettes_mutably()
        self._resolve_components_mutably()
        return self
