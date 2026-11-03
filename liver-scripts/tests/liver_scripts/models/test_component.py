from liver_scripts.models.component import Component
from liver_scripts.models.palette import Palette
from liver_scripts.models.style import PartialStyle


def test_simple_component():
    component = Component(
        name="simple", styles={"windowAccent": PartialStyle(color="#123456")}
    )
    resolved_component = component.resolve()
    assert resolved_component.styles["windowAccent"].color == "#123456"


def test_shallow_component():
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
    b.inherit_mutably({"a": a})
    b = b.resolve(
        palette=Palette(
            name="palette",
            colors={
                "red": "#ff0000",
            },
        ).resolve()
    )
    assert (
        b.styles["windowAccent"]
        == PartialStyle.parse("#ff0000/7f/biu").to_full().resolve()
    )
    assert (
        b.styles["highlightedLine"]
        == PartialStyle.parse("#ffff00/33").to_full().resolve()
    )
    assert b.styles["text"] == PartialStyle.parse("#ffffff//b").to_full().resolve()
