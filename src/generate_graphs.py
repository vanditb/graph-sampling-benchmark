from __future__ import annotations

from dataclasses import dataclass

import networkx as nx


@dataclass(frozen=True)
class GraphSpec:
    graph_type: str
    n: int
    seed: int
