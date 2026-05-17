from __future__ import annotations

import random

import networkx as nx


def sample_random_nodes(graph: nx.Graph, rate: float, seed: int) -> nx.Graph:
    rng = random.Random(seed)
    target = max(2, int(round(graph.number_of_nodes() * rate)))
    nodes = rng.sample(list(graph.nodes()), min(target, graph.number_of_nodes()))
    return graph.subgraph(nodes).copy()


def sample_random_edges(graph: nx.Graph, rate: float, seed: int) -> nx.Graph:
    rng = random.Random(seed)
    edges = list(graph.edges())
    target = max(1, int(round(len(edges) * rate)))
    chosen = rng.sample(edges, min(target, len(edges)))
    sampled = nx.Graph()
    sampled.add_edges_from(chosen)
    return sampled


def sample_random_walk(graph: nx.Graph, rate: float, seed: int) -> nx.Graph:
    rng = random.Random(seed)
    nodes = list(graph.nodes())
    if not nodes:
        return graph.copy()

    target = max(2, int(round(graph.number_of_nodes() * rate)))
    start = rng.choice(nodes)
    visited = {start}
