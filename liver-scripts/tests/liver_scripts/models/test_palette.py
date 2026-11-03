import pytest
from liver_scripts.models.palette import Palette


def test_simple_palette():
    palette = Palette(
        name="simple",
        parents=[],
        colors={
            "red": "#f00",
            "green": "#0f0",
            "blue": "#00f",
        },
    ).resolve_mutably()
    assert len(palette.colors) == 3
    assert palette.colors["red"] == "#f00"
    assert palette.colors["green"] == "#0f0"
    assert palette.colors["blue"] == "#00f"


def test_shallow_palette():
    palette = Palette(
        name="shallow",
        parents=[],
        colors={
            "red": "#ff0000",
            "yellow": "#ffff00",
            "green": "#00ff00",
            "bad": "red",
            "maybe": "yellow",
            "good": "green",
        }
    ).resolve_mutably()
    assert len(palette.colors) == 6
    assert palette.colors["red"] == palette.colors["bad"] == "#ff0000"
    assert palette.colors["yellow"] == palette.colors["maybe"] == "#ffff00"
    assert palette.colors["green"] == palette.colors["good"] == "#00ff00"


def test_deep_palette():
    palette = Palette(
        name="deep",
        parents=[],
        colors={
            "red": "#ff0000",
            "yellow": "#ffff00",
            "green": "#00ff00",
            "bad": "red",
            "maybe": "yellow",
            "good": "green",
            "deleted_file": "bad",
            "modified_file": "maybe",
            "new_file": "good",
        }
    ).resolve_mutably()
    assert len(palette.colors) == 9
    assert (
        palette.colors["red"]
        == palette.colors["bad"]
        == palette.colors["deleted_file"]
        == "#ff0000"
    )
    assert (
        palette.colors["yellow"]
        == palette.colors["maybe"]
        == palette.colors["modified_file"]
        == "#ffff00"
    )
    assert (
        palette.colors["green"]
        == palette.colors["good"]
        == palette.colors["new_file"]
        == "#00ff00"
    )


def test_unresolvable_palette():
    palette = Palette(
        name="unresolvable",
        parents=[],
        colors={
            "red": "#f00",
            "bad": "oops",
        },
    )
    with pytest.raises(ValueError):
        palette.resolve_mutably()


def test_cyclic_palette():
    palette = Palette(
        name="cyclic",
        parents=[],
        colors={
            "a": "b",
            "b": "a",
        }
    )
    with pytest.raises(ValueError):
        palette.resolve_mutably()


def test_palette_inheritance():
    a = Palette(
        name="a",
        parents=[],
        colors={
            "red": "#f00",
            "bad": "red",
        }
    )
    b = Palette(
        name="b",
        parents=[],
        colors={
            "green": "#0f0",
            "good": "green",
        }
    )
    c = Palette(
        name="c",
        parents=["a", "b"],
        colors={
            "tomato": "red",
            "gravy": "good",
        }
    )
    d = Palette(
        name="d",
        parents=["c"],
        colors={
            "blood": "bad",
        }
    )
    c.inherit_mutably([a, b])
    d.inherit_mutably([c])
    a.resolve_mutably()
    b.resolve_mutably()
    c.resolve_mutably()
    d.resolve_mutably()
    assert c.colors["tomato"] == d.colors["blood"] == "#f00"
