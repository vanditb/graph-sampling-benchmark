from __future__ import annotations

from dataclasses import dataclass

import networkx as nx


@dataclass(frozen=True)
class GraphSpec:
    graph_type: str
    n: int
    seed: int


def _er_probability(n: int) -> float:
    # Keep the graph sparse enough to run on a normal laptop.
    return min(0.01, max(0.0015, 8 / max(n - 1, 1)))


def generate_graph(spec: GraphSpec) -> nx.Graph:
