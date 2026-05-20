# Graph Sampling Benchmark

Runtime vs Structure Preservation in Graph Analysis

## Why I Built This
I built this after reaching out to Professor Hang Liu at Rutgers HPDA Lab. His lab works on graph analytics and high-performance data systems, and he suggested I build something concrete so he could evaluate my fit for research. I wanted to make a small project that connects to graph analytics while still matching my current Python and data analysis background.

## Project Question
"When we sample a graph to make analysis faster, how much useful graph structure do we lose?"

## What This Project Does
- generates three kinds of graphs
- samples them with three simple sampling methods
- runs PageRank and connected components on the full graph and the sampled graph
- compares runtime and basic structure-preservation metrics
- saves CSV tables and plots in `results/`

## Methods
### Graph types
- Erdős-Rényi random graph
- Barabási-Albert scale-free graph
- Watts-Strogatz small-world graph

### Sampling methods
- Random node sampling
- Random edge sampling
- Random walk sampling

### Algorithms
- PageRank
- Connected components

### Metrics
- original and sampled node/edge counts
- PageRank runtime on the full graph and sampled graph
- connected components runtime on the full graph and sampled graph
- top-10 PageRank overlap
- edge retention percentage
