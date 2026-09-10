"""Runs the benchmark and saves docs/benchmark_chart.png."""
from pathlib import Path

import matplotlib  # pyright: ignore[reportMissingImports]
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.benchmark import run_benchmark

BRUTE, DIJKSTRA, ASTAR = "#d62728", "#1f77b4", "#2ca02c"

small, scaled = run_benchmark()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

ax = axes[0]
ax.plot(small["n"], [t * 1000 for t in small["brute_force"]], marker="o", label="Brute-force (naive)", color=BRUTE)
ax.plot(small["n"], [t * 1000 for t in small["dijkstra"]], marker="o", label="Dijkstra", color=DIJKSTRA)
ax.plot(small["n"], [t * 1000 for t in small["astar"]], marker="o", label="A*", color=ASTAR)
ax.set_yscale("log")
ax.set_xlabel("Number of nodes")
ax.set_ylabel("Time (ms, log scale)")
ax.set_title("Brute-force vs Dijkstra vs A*\n(small graphs, where brute-force is still feasible)")
ax.legend()
ax.grid(True, which="both", alpha=0.3)

ax2 = axes[1]
all_n = small["n"] + scaled["n"]
all_dij = [t * 1000 for t in small["dijkstra"]] + [t * 1000 for t in scaled["dijkstra"]]
all_astar = [t * 1000 for t in small["astar"]] + [t * 1000 for t in scaled["astar"]]
ax2.plot(all_n, all_dij, marker="o", markersize=4, label="Dijkstra", color=DIJKSTRA)
ax2.plot(all_n, all_astar, marker="o", markersize=4, label="A*", color=ASTAR)
ax2.set_xlabel("Number of nodes")
ax2.set_ylabel("Time (ms)")
ax2.set_title("Dijkstra vs A*, wall-clock time\n(brute-force omitted, infeasible beyond ~12 nodes)")
ax2.legend()
ax2.grid(True, alpha=0.3)

ax3 = axes[2]
ax3.plot(scaled["n"], scaled["dijkstra_expanded"], marker="o", markersize=4, label="Dijkstra", color=DIJKSTRA)
ax3.plot(scaled["n"], scaled["astar_expanded"], marker="o", markersize=4, label="A*", color=ASTAR)
ax3.set_xlabel("Number of nodes")
ax3.set_ylabel("Nodes expanded")
ax3.set_title("Dijkstra vs A*, nodes expanded\n(the work each algorithm actually does)")
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
Path("docs").mkdir(exist_ok=True)
plt.savefig("docs/benchmark_chart.png", dpi=150)
print("\nSaved docs/benchmark_chart.png")
