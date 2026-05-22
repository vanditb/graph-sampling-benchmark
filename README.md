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
- density change
- connected component count difference

The graph sizes in this project are 1,000, 3,000, and 5,000 nodes. I kept them small enough to run on a normal laptop. The project is CPU-based and uses NetworkX, not a high-performance graph system.

## Results
These are the main patterns I saw in my run:

- Lower sampling rates usually saved more time, but they also lost more structure.
- Random walk sampling was the best balance overall in this run. On average it saved about 59% of PageRank runtime and about 56% of connected components runtime, while keeping about 44% top-10 PageRank overlap.
- Random node sampling also saved a lot of time, but it usually had lower PageRank overlap than random walk.
- Random edge sampling kept more edges by design, but it did not always give the best runtime savings.
- Barabási-Albert graphs had higher PageRank top-10 overlap than the other graph types in this run, which makes sense because hub nodes matter a lot in scale-free graphs.

I would not treat these numbers as universal. They are just one small benchmark run on synthetic graphs.

## Limitations
