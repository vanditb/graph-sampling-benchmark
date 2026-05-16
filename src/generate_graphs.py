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
    if spec.graph_type == "erdos_renyi":
        return nx.erdos_renyi_graph(spec.n, _er_probability(spec.n), seed=spec.seed)
    if spec.graph_type == "barabasi_albert":
        m = 4 if spec.n >= 1000 else 3
        return nx.barabasi_albert_graph(spec.n, m, seed=spec.seed)
    if spec.graph_type == "watts_strogatz":
        k = 6 if spec.n >= 1000 else 4
        return nx.watts_strogatz_graph(spec.n, k, 0.15, seed=spec.seed)
    raise ValueError(f"Unknown graph type: {spec.graph_type}")


def graph_specs() -> list[GraphSpec]:
