from __future__ import annotations

import networkx as nx


def time_saved_pct(full_seconds: float, sampled_seconds: float) -> float:
    if full_seconds <= 0:
        return 0.0
    return (full_seconds - sampled_seconds) / full_seconds * 100


def top_k_pagerank_nodes(scores: dict, k: int = 10) -> list:
    return [node for node, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:k]]


def top_k_overlap(full_scores: dict, sampled_scores: dict, k: int = 10) -> tuple[int, float]:
    full_top = set(top_k_pagerank_nodes(full_scores, k))
    sampled_top = set(top_k_pagerank_nodes(sampled_scores, k))
    overlap = len(full_top & sampled_top)
    return overlap, overlap / k * 100


def edge_retention_pct(full_graph: nx.Graph, sampled_graph: nx.Graph) -> float:
    full_edges = max(full_graph.number_of_edges(), 1)
    return sampled_graph.number_of_edges() / full_edges * 100


def density_change_pct(full_graph: nx.Graph, sampled_graph: nx.Graph) -> float:
    full_density = nx.density(full_graph)
    if full_density == 0:
