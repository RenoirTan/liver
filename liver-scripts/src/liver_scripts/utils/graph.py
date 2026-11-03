import networkx as nx
from typing import TypeVar
from liver_scripts.models.base import BaseDependent


N_co = TypeVar("N_co", bound=BaseDependent, covariant=True)


def build_dependency_graph(nodes: list[N_co]) -> nx.Graph:
    node_names = {n.name for n in nodes}
    assert len(node_names) == len(nodes)
    for node in nodes:
        for parent in node.parents:
            assert parent in node_names
    G = nx.DiGraph({n.name: n.parents for n in nodes})
    return G


def get_dependency_list(G: nx.Graph) -> list[BaseDependent]:
    return list(reversed(list(nx.topological_sort(G))))
