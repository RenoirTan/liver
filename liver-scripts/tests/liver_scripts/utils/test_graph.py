from liver_scripts.models.palette import Palette
from liver_scripts.utils.graph import build_dependency_graph


def test_graph():
    palette_arguments = [
        ("a", ["b", "c"]),
        ("b", ["c"]),
        ("c", []),
    ]
    palettes = [
        Palette(name=name, parents=parents)
        for name, parents in palette_arguments
    ]
    graph = build_dependency_graph(palettes)
    assert list(graph.neighbors("a")) == ["b", "c"]
    assert list(graph.neighbors("b")) == ["c"]
    assert list(graph.neighbors("c")) == []
