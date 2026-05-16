from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import time

import networkx as nx
import numpy as np
import pandas as pd

from generate_graphs import GraphSpec, generate_graph, graph_specs
