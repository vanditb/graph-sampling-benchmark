from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D


def _rate_label(rate: float) -> str:
    return f"{int(rate * 100)}%"


def create_plots(detailed: pd.DataFrame, summary: pd.DataFrame, plots_dir: Path) -> None:
