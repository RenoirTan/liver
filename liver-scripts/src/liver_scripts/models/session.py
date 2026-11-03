from liver_scripts.models.base import BaseModel
import copy
from liver_scripts.models.component import (
    Component,
    inherit_components,
)
from liver_scripts.models.palette import Palette, ResolvedPalette, inherit_palettes
from liver_scripts.models.template import ResolvedTemplate, TemplateRecipe, Template
from dataclasses import dataclass, field


@dataclass
class ResolvedSession(BaseModel):
    templates: dict[str, ResolvedTemplate]
    palettes: dict[str, ResolvedPalette]


@dataclass
class Session(BaseModel):
    templates: dict[str, TemplateRecipe]
    palettes: dict[str, Palette]
    components: dict[str, Component]

    def inherit_mutably(self) -> "Session":
        self.palettes = inherit_palettes(self.palettes)
        self.components = inherit_components(self.components)
        return self

    def inherit(self) -> "Session":
        return Session(
            templates=copy.deepcopy(self.templates),
            palettes=inherit_palettes(self.palettes),
            components=inherit_components(self.components),
        )

    def _resolve_palettes(self) -> dict[str, ResolvedPalette]:
        return {n: p.resolve() for n, p in self.palettes.items()}

    def resolve(self) -> ResolvedSession:
        resolved_palettes = self._resolve_palettes()
        templates = {
            n: t.resolve(resolved_palettes, self.components)
            for n, t in self.templates.items()
        }
        return ResolvedSession(templates, resolved_palettes)


@dataclass
class SessionBuilder(BaseModel):
    templates: dict[str, Template]
    palettes: dict[str, Palette] = field(default_factory=dict)

    def collect_data_mutably(self) -> "SessionBuilder":
        return self

    def collect_data(self) -> "SessionBuilder":
        return copy.deepcopy(self).collect_data_mutably()

    def _template_recipes(self) -> dict[str, TemplateRecipe]:
        return {t.name: t.to_recipe() for t in self.templates.values()}

    def _template_palettes(self) -> dict[str, Palette]:
        return {p.name: p for p in (t.palette for t in self.templates.values())}

    def _template_components(self) -> dict[str, Component]:
        components = {}
        for template in self.templates.values():
            components |= template.components
        return components

    def build(self) -> Session:
        templates = self._template_recipes()
        palettes = self.palettes | self._template_palettes()
        components = self._template_components()
        return Session(templates, palettes, components)
