from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import time

import networkx as nx
import numpy as np
import pandas as pd

from generate_graphs import GraphSpec, generate_graph, graph_specs
from metrics import (
    component_count_diff,
    density_change_pct,
    edge_retention_pct,
    time_saved_pct,
    top_k_overlap,
    top_k_pagerank_nodes,
)
from sampling_methods import sample_random_edges, sample_random_nodes, sample_random_walk
from visualize import create_plots


SAMPLE_RATES = [0.25, 0.50, 0.75]
SAMPLERS = {
    "random_node": sample_random_nodes,
    "random_edge": sample_random_edges,
    "random_walk": sample_random_walk,
}


def _pagerank(graph: nx.Graph) -> tuple[dict, float]:
    start = time.perf_counter()
    scores = nx.pagerank(graph, alpha=0.85, tol=1e-6, max_iter=100)
    elapsed = time.perf_counter() - start
    return scores, elapsed


def _connected_components(graph: nx.Graph) -> tuple[int, float]:
    start = time.perf_counter()
    count = nx.number_connected_components(graph)
    elapsed = time.perf_counter() - start
    return count, elapsed


def _seed_for(spec: GraphSpec, method: str, rate: float) -> int:
    rate_key = int(rate * 100)
    method_offset = {"random_node": 11, "random_edge": 22, "random_walk": 33}[method]
    return spec.seed * 1000 + rate_key + method_offset


def _base_graph_info(graph: nx.Graph) -> dict:
    return {
        "original_node_count": graph.number_of_nodes(),
        "original_edge_count": graph.number_of_edges(),
        "original_density": nx.density(graph),
    }


def _run_for_graph(spec: GraphSpec) -> list[dict]:
    graph = generate_graph(spec)
    full_pagerank_scores, full_pagerank_time = _pagerank(graph)
    full_component_count, full_cc_time = _connected_components(graph)
    full_top10 = top_k_pagerank_nodes(full_pagerank_scores, 10)
    base_info = _base_graph_info(graph)

    rows = []
    for method_name, sampler in SAMPLERS.items():
        for rate in SAMPLE_RATES:
            sampled_graph = sampler(graph, rate, _seed_for(spec, method_name, rate))
            sampled_pagerank_scores, sampled_pagerank_time = _pagerank(sampled_graph)
            sampled_component_count, sampled_cc_time = _connected_components(sampled_graph)
            overlap_count, overlap_pct = top_k_overlap(full_pagerank_scores, sampled_pagerank_scores, 10)

            row = {
                **asdict(spec),
                **base_info,
                "sampling_method": method_name,
                "sampling_rate": rate,
                "sampled_node_count": sampled_graph.number_of_nodes(),
                "sampled_edge_count": sampled_graph.number_of_edges(),
                "pagerank_runtime_full_sec": full_pagerank_time,
                "pagerank_runtime_sampled_sec": sampled_pagerank_time,
                "connected_components_runtime_full_sec": full_cc_time,
                "connected_components_runtime_sampled_sec": sampled_cc_time,
                "pagerank_top10_overlap_count": overlap_count,
                "pagerank_top10_overlap_pct": overlap_pct,
                "edge_retention_pct": edge_retention_pct(graph, sampled_graph),
                "density_change_pct": density_change_pct(graph, sampled_graph),
                "connected_component_count_diff": sampled_component_count - full_component_count,
                "pagerank_runtime_saved_pct": time_saved_pct(full_pagerank_time, sampled_pagerank_time),
                "cc_runtime_saved_pct": time_saved_pct(full_cc_time, sampled_cc_time),
                "full_connected_component_count": full_component_count,
                "sampled_connected_component_count": sampled_component_count,
            }
            rows.append(row)
    return rows


def _summary_table(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["graph_type", "sampling_method", "sampling_rate"], as_index=False)
        .agg(
            mean_original_nodes=("original_node_count", "mean"),
            mean_original_edges=("original_edge_count", "mean"),
            mean_sampled_nodes=("sampled_node_count", "mean"),
            mean_sampled_edges=("sampled_edge_count", "mean"),
