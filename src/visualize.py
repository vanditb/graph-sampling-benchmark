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
        groups = plot_df["group"].tolist()
        x = range(len(groups))
        width = 0.38
        ax.bar([i - width / 2 for i in x], plot_df[full_col], width=width, label="Full graph")
        ax.bar([i + width / 2 for i in x], plot_df[sampled_col], width=width, label="Sampled graph")
        ax.set_title(title)
        ax.set_xticks(list(x))
        ax.set_xticklabels(groups, rotation=45, ha="right")
        ax.set_ylabel("Seconds")
        ax.legend(frameon=False)

    fig.suptitle("Runtime comparison by sampling method and rate")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def _pagerank_overlap_plot(summary: pd.DataFrame, output_path: Path) -> None:
    methods = ["random_node", "random_edge", "random_walk"]
    rates = [0.25, 0.50, 0.75]

    heat = (
        summary.groupby(["sampling_method", "sampling_rate"], as_index=False)["mean_pagerank_top10_overlap_pct"]
        .mean()
        .pivot(index="sampling_method", columns="sampling_rate", values="mean_pagerank_top10_overlap_pct")
        .reindex(methods)
    )

    heat = heat[rates]

    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(heat.values, cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(rates)))
    ax.set_xticklabels([_rate_label(r) for r in rates])
    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(["Random node", "Random edge", "Random walk"])
    ax.set_xlabel("Sampling rate")
    ax.set_ylabel("Sampling method")
    ax.set_title("Top-10 PageRank overlap")

    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            value = heat.values[i, j]
            ax.text(j, i, f"{value:.1f}%", ha="center", va="center", color="black")

    fig.colorbar(im, ax=ax, label="Overlap %")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def _structure_tradeoff_plot(summary: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    colors = {"random_node": "#4C78A8", "random_edge": "#F58518", "random_walk": "#54A24B"}
    markers = {0.25: "o", 0.50: "s", 0.75: "^"}
    method_labels = {"random_node": "Random node", "random_edge": "Random edge", "random_walk": "Random walk"}

    plots = [
        ("mean_pagerank_top10_overlap_pct", "PageRank overlap %"),
        ("mean_edge_retention_pct", "Edge retention %"),
    ]

    scatter_df = (
        summary.groupby(["sampling_method", "sampling_rate"], as_index=False)
        .agg(
            mean_pagerank_runtime_saved_pct=("mean_pagerank_runtime_saved_pct", "mean"),
            mean_pagerank_top10_overlap_pct=("mean_pagerank_top10_overlap_pct", "mean"),
            mean_edge_retention_pct=("mean_edge_retention_pct", "mean"),
        )
    )
    scatter_df["sampling_method"] = pd.Categorical(
        scatter_df["sampling_method"], categories=["random_node", "random_edge", "random_walk"], ordered=True
    )
    scatter_df = scatter_df.sort_values(["sampling_method", "sampling_rate"])

    for ax, (metric_col, y_label) in zip(axes, plots):
        for _, row in scatter_df.iterrows():
            ax.scatter(
                row["mean_pagerank_runtime_saved_pct"],
                row[metric_col],
                color=colors[row["sampling_method"]],
                marker=markers[row["sampling_rate"]],
                s=70,
                alpha=0.85,
            )
        ax.set_xlabel("Average runtime saved %")
        ax.set_ylabel(y_label)
        ax.grid(True, alpha=0.2)

    handles = []
    for method, color in colors.items():
        handles.append(
            Line2D([0], [0], marker="o", color="w", label=method_labels[method], markerfacecolor=color, markersize=9)
        )
    rate_handles = []
    for rate, marker in markers.items():
