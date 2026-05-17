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
