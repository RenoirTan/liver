from liver_scripts.utils.graph import build_dependency_graph, get_dependency_list
import copy
from dataclasses import dataclass, field
import networkx as nx
from liver_scripts.models.base import BaseModel, BaseDependent
from liver_scripts.models.palette import ResolvedPalette
from liver_scripts.models.style import PartialStyle, ResolvedStyle, BaseStyle


@dataclass
class BaseComponent(BaseModel):
    """
    Component styles after inheriting from parents
    and resolving partial styles.
    """

    name: str
    kind: str
    styles: dict[str, BaseStyle]


@dataclass
class ResolvedComponent(BaseComponent):
    name: str
    kind: str
    styles: dict[str, ResolvedStyle]


@dataclass
class Component(BaseComponent, BaseDependent):
    name: str
    kind: str = "default"
    parents: list[str] = field(default_factory=list)
    styles: dict[str, PartialStyle] = field(default_factory=dict)
    _RESOLVED_CLASS: type[ResolvedComponent] = field(default=ResolvedComponent)

    def inherit_mutably(self, parents: dict[str, BaseComponent]) -> "Component":
        for parent_name in self.parents:
            parent = parents[parent_name]
            for name, new_style in parent.styles.items():
                old_style = self.styles.get(name)
                new_style = new_style.to_partial()
                if old_style is None:
                    self.styles[name] = new_style
                else:
                    self.styles[name] = old_style.inherit_mutably(new_style)
        return self

    def inherit(self, parents: dict[str, BaseComponent]) -> "Component":
        return copy.copy(self).inherit_mutably(parents)

    def resolve_styles(
        self,
        palette: ResolvedPalette | None = None,
    ) -> dict[str, ResolvedStyle]:
        palette = palette or ResolvedPalette.blank()
        resolved_styles: dict[str, ResolvedStyle] = {
            name: value.to_full().resolve(palette)
            for name, value in self.styles.items()
        }
        return resolved_styles

    def resolve(self, palette: ResolvedPalette | None = None) -> ResolvedComponent:
        resolved_styles = self.resolve_styles(palette)
        return self._RESOLVED_CLASS(
            name=self.name,
            kind=self.kind,
            styles=resolved_styles,
        )


def inherit_components(components: dict[str, Component]) -> dict[str, Component]:
    G = build_dependency_graph(list(components.values()))
    cycles = nx.simple_cycles(G)
    for _ in cycles:
        raise ValueError(f"Dependency cycle detected in components: {cycles}")
    sorted_components = get_dependency_list(G)
    updated_components = dict[str, Component]()
    for name in sorted_components:
        component = components[name]
        parents: dict[str, BaseComponent] = {
            p: components[p] for p in component.parents
        }
        updated_components[name] = component.inherit(parents)
    return updated_components
