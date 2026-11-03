import pytest
from liver_scripts.models.palette import inherit_palettes, Palette, ResolvedPalette


def create_palette_0() -> Palette:
    return Palette(
        name="p0",
        parents=[],
        colors={
            "red": "#f00",
            "green": "#0f0",
            "blue": "#00f",
        },
    )


def create_resolved_palette_0() -> ResolvedPalette:
    return ResolvedPalette(
        name="p0",
        colors={
            "red": "#f00",
            "green": "#0f0",
            "blue": "#00f",
        },
    )


def create_palette_1() -> Palette:
    return Palette(
        name="p1",
        parents=[],
        colors={
            "red": "#ff0000",
            "yellow": "#ffff00",
            "green": "#00ff00",
            "bad": "red",
            "maybe": "yellow",
            "good": "green",
        },
    )


def create_resolved_palette_1() -> ResolvedPalette:
    return ResolvedPalette(
        name="p1",
        colors={
            "red": "#ff0000",
            "yellow": "#ffff00",
            "green": "#00ff00",
            "bad": "#ff0000",
            "maybe": "#ffff00",
            "good": "#00ff00",
        },
    )


def create_palette_2() -> Palette:
    return Palette(
        name="p2",
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
        },
    )


def create_resolved_palette_2() -> ResolvedPalette:
    return ResolvedPalette(
        name="p2",
        colors={
            "red": "#ff0000",
            "yellow": "#ffff00",
            "green": "#00ff00",
            "bad": "#ff0000",
            "maybe": "#ffff00",
            "good": "#00ff00",
            "deleted_file": "#ff0000",
            "modified_file": "#ffff00",
            "new_file": "#00ff00",
        },
    )


def create_bad_palette_0() -> Palette:
    return Palette(
        name="p3",
        parents=[],
        colors={
            "red": "#f00",
            "bad": "oops",
        },
    )


def create_bad_palette_1() -> Palette:
    return Palette(
        name="cyclic",
        parents=[],
        colors={
            "a": "b",
            "b": "a",
        },
    )


def create_inheritance_palettes_0() -> list[Palette]:
    a = Palette(
        name="a",
        parents=[],
        colors={
            "red": "#f00",
            "bad": "red",
        },
    )
    b = Palette(
        name="b",
        parents=[],
        colors={
            "green": "#0f0",
            "good": "green",
        },
    )
    c = Palette(
        name="c",
        parents=["a", "b"],
        colors={
            "tomato": "red",
            "gravy": "good",
        },
    )
    d = Palette(
        name="d",
        parents=["c"],
        colors={
            "gravy": "bad",
        },
    )
    return [a, b, c, d]


def create_inheritance_resolved_palettes_0() -> list[ResolvedPalette]:
    a = ResolvedPalette(
        name="a",
        colors={
            "red": "#f00",
            "bad": "#f00",
        },
    )
    b = ResolvedPalette(
        name="b",
        colors={
            "green": "#0f0",
            "good": "#0f0",
        },
    )
    c = ResolvedPalette(
        name="c",
        colors={
            "red": "#f00",
            "bad": "#f00",
            "green": "#0f0",
            "good": "#0f0",
            "tomato": "#f00",
            "gravy": "#0f0",
        },
    )
    d = ResolvedPalette(
        name="d",
        colors={
            "red": "#f00",
            "bad": "#f00",
            "green": "#0f0",
            "good": "#0f0",
            "tomato": "#f00",
            "gravy": "#f00",
        },
    )
    return [a, b, c, d]


def test_simple_palette():
    assert create_palette_0().resolve() == create_resolved_palette_0()


def test_shallow_palette():
    assert create_palette_1().resolve() == create_resolved_palette_1()


def test_deep_palette():
    assert create_palette_2().resolve() == create_resolved_palette_2()


def test_unresolvable_palette():
    with pytest.raises(ValueError):
        create_bad_palette_0().resolve()


def test_cyclic_palette():
    with pytest.raises(ValueError):
        create_bad_palette_1().resolve()


def test_palette_inheritance():
    resolved = {p.name: p for p in create_inheritance_resolved_palettes_0()}
    inherited_palettes = inherit_palettes(
        {p.name: p for p in create_inheritance_palettes_0()}
    )
    palettes = {n: p.resolve() for n, p in inherited_palettes.items()}
    assert palettes == resolved
