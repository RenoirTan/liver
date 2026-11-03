import copy
from dataclasses import dataclass, field
from liver_scripts.models.base import BaseModel, BaseDependent
from liver_scripts.models.component import Component, ResolvedComponent
from liver_scripts.models.palette import Palette, ResolvedPalette


@dataclass
class ResolvedTemplate(BaseModel):
    """
    A combination of color palette and component styles
    """

    name: str
    palette: ResolvedPalette = field(default_factory=ResolvedPalette.blank)
    components: dict[str, ResolvedComponent] = field(default_factory=dict)


@dataclass
class TemplateRecipe(BaseModel):
    name: str
    palette: str
    components: dict[str, str]
    """
    Final component name to required internal component
    """

    def resolve(
        self,
        resolved_palettes: dict[str, ResolvedPalette],
        unresolved_components: dict[str, Component],
    ) -> ResolvedTemplate:
        palette = resolved_palettes[self.palette]
        components = dict[str, ResolvedComponent]()
        for internal in self.components.values():
            components[internal] = unresolved_components[internal].resolve(palette)
        resolved_components = {f: components[i] for f, i in self.components.items()}
        return ResolvedTemplate(
            name=self.name,
            palette=palette,
            components=resolved_components,
        )


@dataclass
class Template(BaseModel, BaseDependent):
    name: str
    parents: list[str] = field(default_factory=list)
    """
    List of parent template names to inherit definitions from
    """
    palette: Palette = field(default_factory=Palette.blank)
    components: dict[str, Component] = field(default_factory=dict)
    """
    Map of components to draw from.
    """
    component_roles: dict[str, str] = field(default_factory=dict)
    """
    Mapping of final palette names (required by backend)
    to internal palette names (stored in datastruct)
    """

    @property
    def component_names(self) -> list[str]:
        return list(self.components.keys())

    def to_recipe(self) -> TemplateRecipe:
        return TemplateRecipe(
            name=self.name,
            palette=self.palette.name,
            components=copy.deepcopy(self.component_roles),
        )
