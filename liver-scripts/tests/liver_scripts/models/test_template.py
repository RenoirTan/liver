from liver_scripts.models.style import PartialStyle, ResolvedStyle
from liver_scripts.models.component import Component, ResolvedComponent
from liver_scripts.models.palette import Palette, ResolvedPalette
from liver_scripts.models.template import Template, ResolvedTemplate


def test_simple_template():
    template = Template(
        name="simple",
        palettes={
            "simple_palette": Palette(
                name="simple_palette",
                colors={"red": "#ff0000", "yellow": "#ffff00", "green": "#00ff00"},
            )
        },
        components={
            "simple_component": Component(
                name="simple_component",
                styles={"windowAccent": PartialStyle("#123456")},
            )
        },
        palette_roles={"colors": "simple_palette"},
        component_roles={"window": "simple_component"},
    )
    resolved_template = ResolvedTemplate(
        name="simple",
        palettes={
            "simple_palette": ResolvedPalette(
                name="simple_palette",
                colors={"red": "#ff0000", "yellow": "#ffff00", "green": "#00ff00"},
            )
        },
        components={
            "simple_component": ResolvedComponent(
                name="simple_component",
                kind="default",
                styles={"windowAccent": ResolvedStyle("#123456")},
            )
        },
        palette_roles={"colors": "simple_palette"},
        component_roles={"window": "simple_component"},
    )
    assert template.resolve() == resolved_template


def test_shallow_template():
    template = Template(
        name="simple",
        palettes={
            "p0": Palette(
                name="p0",
                colors={
                    "red": "#ff0000",
                    "yellow": "#ffff00",
                    "green": "#00ff00",
                    "blue": "#0000ff",
                    "good": "green",
                    "maybe": "yellow",
                    "bad": "red",
                },
            ),
            "p1": Palette(
                name="p1",
                parents=["p0"],
                colors={
                    "untracked": "good",
                    "modified": "maybe",
                    "added": "blue",
                    "deleted": "bad",
                },
            ),
        },
        components={
            "c0": Component(
                name="c0",
                styles={
                    "windowAccent": PartialStyle("red//biu"),
                    "text": PartialStyle.parse("#ffffff//b"),
                },
            ),
            "c1": Component(
                name="c1",
                parents=["c0"],
                styles={
                    "windowAccent": PartialStyle.parse("red/7f"),
                    "highlightedLine": PartialStyle.parse("#ffff00/33"),
                },
            ),
        },
        palette_roles={"colors": "p1"},
        component_roles={"window": "c1"},
    )
    resolved_template = ResolvedTemplate(
        name="simple",
        palettes={
            "p0": ResolvedPalette(
                name="p0",
                colors={
                    "red": "#ff0000",
                    "yellow": "#ffff00",
                    "green": "#00ff00",
                    "blue": "#0000ff",
                    "good": "#00ff00",
                    "maybe": "#ffff00",
                    "bad": "#ff0000",
                },
            ),
            "p1": ResolvedPalette(
                name="p1",
                colors={
                    "red": "#ff0000",
                    "yellow": "#ffff00",
                    "green": "#00ff00",
                    "blue": "#0000ff",
                    "good": "#00ff00",
                    "maybe": "#ffff00",
                    "bad": "#ff0000",
                    "untracked": "#00ff00",
                    "modified": "#ffff00",
                    "added": "#0000ff",
                    "deleted": "#ff0000",
                },
            ),
        },
        components={
            "c0": ResolvedComponent(
                name="c0",
                kind="default",
                styles={
                    "windowAccent": ResolvedStyle.parse("#123456"),
                    "text": ResolvedStyle.parse("#ffffff//b"),
                },
            ),
            "c1": ResolvedComponent(
                name="c1",
                kind="default",
                styles={
                    "windowAccent": ResolvedStyle.parse("#ff0000/7f"),
                    "highlightedLine": ResolvedStyle.parse("#ffff00/33"),
                },
            ),
        },
        palette_roles={"colors": "p1"},
        component_roles={"window": "c1"},
    )
    assert template.resolve() == resolved_template
