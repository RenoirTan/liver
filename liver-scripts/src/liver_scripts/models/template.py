import copy
from dataclasses import dataclass, field
import networkx as nx
from liver_scripts.models.base import BaseModel, BaseDependent
from liver_scripts.models.component import Component, ResolvedComponent, BaseComponent
from liver_scripts.models.palette import Palette, ResolvedPalette, BasePalette
from liver_scripts.utils.graph import build_dependency_graph, get_dependency_list


@dataclass
class BaseTemplate(BaseModel):
    """
    A combination of color palette and component styles
    """

    name: str
    palettes: dict[str, ResolvedPalette] = field(default_factory=dict)
    components: dict[str, ResolvedComponent] = field(default_factory=dict)
    palette_roles: dict[str, str] = field(default_factory=dict)
    component_roles: dict[str, str] = field(default_factory=dict)


@dataclass
class ResolvedTemplate(BaseTemplate):
    """
    A combination of color palette and component styles
    """

    name: str
    palettes: dict[str, ResolvedPalette] = field(default_factory=dict)
    components: dict[str, ResolvedComponent] = field(default_factory=dict)
    palette_roles: dict[str, str] = field(default_factory=dict)
    component_roles: dict[str, str] = field(default_factory=dict)


@dataclass
class Template(BaseTemplate, BaseDependent):
    name: str
    parents: list[str] = field(default_factory=list)
    """
    List of parent template names to copy from
    """
    palettes: dict[str, Palette] = field(default_factory=dict)
    """
    Map of palettes to draw from.
    This mapping grows when this template inherits from parent templates.
    After inheritance, the resolution step will resolve all palettes
    and select only those in palette_roles.
    """
    components: dict[str, Component] = field(default_factory=dict)
    """
    Like in palettes but with components
    """
    palette_roles: dict[str, str] = field(default_factory=dict)
    """
    Mapping of final palette names (required by backend)
    to internal palette names (stored in datastruct)
    """
    component_roles: dict[str, str] = field(default_factory=dict)
    """
    Like in palette_roles but with components
    """

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
            parent_palettes.extend(parent.palettes.values())
            parent_components.extend(parent.components.values())
        self._inherit_palettes_mutably(parent_palettes)
        self._inherit_components_mutably(parent_components)
        return self

    def inherit(self, parents: list["Template"]) -> "Template":
        return copy.deepcopy(self).inherit_mutably(parents)

    def _resolve_palettes(self) -> dict[str, ResolvedPalette]:
        G = build_dependency_graph(list(self.palettes.values()))
        cycles = nx.simple_cycles(G)
        for _ in cycles:
            raise ValueError(f"Dependency cycle detected in palettes: {cycles}")
        sorted_palettes = get_dependency_list(G)
        palettes = dict[str, Palette]()
        for name in sorted_palettes:
            palette = self.palettes[name]
            parents: dict[str, BasePalette] = {
                p: self.palettes[p] for p in palette.parents
            }
            palettes[name] = palette.inherit(parents)
        return {n: p.resolve() for n, p in palettes.items()}

    def _resolve_components(self):
        G = build_dependency_graph(list(self.components.values()))
        cycles = nx.simple_cycles(G)
        for _ in cycles:
            raise ValueError(f"Dependency cycle detected in components: {cycles}")
        sorted_components = get_dependency_list(G)
        components = dict[str, Component]()
        for name in sorted_components:
            component = self.components[name]
            parents: dict[str, BaseComponent] = {
                p: self.components[p] for p in component.parents
            }
            components[name] = component.inherit(parents)
        return {n: c.resolve() for n, c in components.items()}

    def resolve(self) -> ResolvedTemplate:
        return ResolvedTemplate(
            name=self.name,
            palettes=self._resolve_palettes(),
            components=self._resolve_components(),
            palette_roles=copy.deepcopy(self.palette_roles),
            component_roles=copy.deepcopy(self.component_roles),
        )
