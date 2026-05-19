from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D


def _rate_label(rate: float) -> str:
    return f"{int(rate * 100)}%"


def create_plots(detailed: pd.DataFrame, summary: pd.DataFrame, plots_dir: Path) -> None:
    _runtime_comparison_plot(summary, plots_dir / "runtime_comparison.png")
    _pagerank_overlap_plot(summary, plots_dir / "pagerank_overlap.png")
    _structure_tradeoff_plot(summary, plots_dir / "structure_tradeoff.png")


def _runtime_comparison_plot(summary: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False)
    method_order = ["random_node", "random_edge", "random_walk"]
    algorithms = [
        (
            "PageRank runtime",
            "mean_pagerank_runtime_full_sec",
            "mean_pagerank_runtime_sampled_sec",
        ),
        (
            "Connected components runtime",
            "mean_cc_runtime_full_sec",
            "mean_cc_runtime_sampled_sec",
        ),
    ]

    for ax, (title, full_col, sampled_col) in zip(axes, algorithms):
        plot_df = (
            summary.groupby(["sampling_method", "sampling_rate"], as_index=False)
            .agg({full_col: "mean", sampled_col: "mean"})
        )
        plot_df["sampling_method"] = pd.Categorical(plot_df["sampling_method"], categories=method_order, ordered=True)
        plot_df = plot_df.sort_values(["sampling_method", "sampling_rate"])
        plot_df["group"] = plot_df["sampling_method"].astype(str) + " / " + plot_df["sampling_rate"].map(_rate_label)
