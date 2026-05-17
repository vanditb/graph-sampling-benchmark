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
