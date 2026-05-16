from __future__ import annotations

import networkx as nx


def time_saved_pct(full_seconds: float, sampled_seconds: float) -> float:
    if full_seconds <= 0:
        return 0.0
    return (full_seconds - sampled_seconds) / full_seconds * 100


