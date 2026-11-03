from test_liver_scripts.models.test_palette import create_resolved_palette_1
from liver_scripts.models.component import (
    Component,
    ResolvedComponent,
    inherit_components,
)
from liver_scripts.models.palette import ResolvedPalette
from liver_scripts.models.style import PartialStyle, ResolvedStyle


def create_simple_component() -> Component:
    return Component(
        name="simple", styles={"windowAccent": PartialStyle(color="#123456")}
    )


def create_simple_resolved_component() -> ResolvedComponent:
    return ResolvedComponent(
        name="simple",
        kind="default",
        styles={"windowAccent": ResolvedStyle.parse("#123456")},
    )


def create_shallow_components() -> list[Component]:
    a = Component(
        name="a",
        styles={
            "windowAccent": PartialStyle.parse("red//biu"),
            "text": PartialStyle.parse("#ffffff//b"),
        },
    )
    b = Component(
        name="b",
        parents=["a"],
        styles={
            "windowAccent": PartialStyle.parse("red/7f"),
            "highlightedLine": PartialStyle.parse("#ffff00/33"),
        },
    )
    return [a, b]


def create_shallow_resolved_components(
    palette: ResolvedPalette,
) -> list[ResolvedComponent]:
    a = ResolvedComponent(
        name="a",
        kind="default",
        styles={
            "windowAccent": PartialStyle.parse("red//biu").to_full().resolve(palette),
            "text": PartialStyle.parse("#ffffff//b").to_full().resolve(palette),
        },
    )
    b = ResolvedComponent(
        name="b",
        kind="default",
        styles={
            "windowAccent": PartialStyle.parse("red/7f/biu").to_full().resolve(palette),
            "highlightedLine": PartialStyle.parse("#ffff00/33")
            .to_full()
            .resolve(palette),
            "text": PartialStyle.parse("#ffffff//b").to_full().resolve(palette),
        },
    )
    return [a, b]


def test_simple_component():
    assert create_simple_component().resolve() == create_simple_resolved_component()


def test_shallow_component():
    palette = create_resolved_palette_1()
    inherited = inherit_components({c.name: c for c in create_shallow_components()})
    components = {n: c.resolve(palette) for n, c in inherited.items()}
    resolved = {c.name: c for c in create_shallow_resolved_components(palette)}
    assert components == resolved
