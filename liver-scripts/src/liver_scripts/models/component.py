import copy
from dataclasses import dataclass, field
from liver_scripts.models.base import BaseModel, BaseDependent
from liver_scripts.models.palette import Palette
from liver_scripts.models.style import PartialStyle, ResolvedStyle


@dataclass
class ResolvedComponent(BaseModel):
    """
    Component styles after inheriting from parents
    and resolving partial styles.
    """

    name: str
    kind: str
    styles: dict[str, ResolvedStyle]


@dataclass
class Component(BaseModel, BaseDependent):
    name: str
    kind: str = "default"
    parents: list[str] = field(default_factory=list)
    styles: dict[str, PartialStyle] = field(default_factory=dict)
    _RESOLVED_CLASS: type[ResolvedComponent] = field(
        init=False, default=ResolvedComponent
    )

    def inherit_mutably(self, parents: list["Component"]) -> "Component":
        for parent in parents:
            for name, new_style in parent.styles.items():
                old_style = self.styles.get(name)
                if old_style is None:
                    self.styles[name] = new_style
                else:
                    self.styles[name] = old_style.inherit_mutably(new_style)
        return self

    def inherit(self, parents: list["Component"]) -> "Component":
        return copy.copy(self).inherit_mutably(parents)

    def resolve_styles(
        self,
        palette: Palette | None = None,
    ) -> dict[str, ResolvedStyle]:
        palette = palette or Palette.blank()
        resolved_styles: dict[str, ResolvedStyle] = {
            name: value.to_full().resolve(palette)
            for name, value in self.styles.items()
        }
        return resolved_styles

    def resolve(self, palette: Palette | None = None) -> ResolvedComponent:
        resolved_styles = self.resolve_styles(palette)
        return self._RESOLVED_CLASS(
            name=self.name,
            kind=self.kind,
            styles=resolved_styles,
        )
