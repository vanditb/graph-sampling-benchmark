from __future__ import annotations

import random

import networkx as nx


def sample_random_nodes(graph: nx.Graph, rate: float, seed: int) -> nx.Graph:
    rng = random.Random(seed)
    target = max(2, int(round(graph.number_of_nodes() * rate)))
    nodes = rng.sample(list(graph.nodes()), min(target, graph.number_of_nodes()))
