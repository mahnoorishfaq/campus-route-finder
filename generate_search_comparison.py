"""Saves docs/search_comparison.png, showing how much of the map each algorithm
had to look at to find the same route."""
from pathlib import Path

import matplotlib  # pyright: ignore[reportMissingImports]
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.algorithms.astar import astar_shortest_path
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.graph import Graph
from src.plotting import draw_map

START, END = "gate", "hostel"

graph = Graph.from_json()
fig, axes = plt.subplots(1, 2, figsize=(17, 7))

for ax, (label, fn) in zip(axes, [("Dijkstra", dijkstra_shortest_path), ("A*", astar_shortest_path)]):
    result = fn(graph, START, END)
    draw_map(
        graph,
        route=result.path,
        expanded=result.expansion_order,
        start=START,
        end=END,
        show_weights=False,
        title=f"{label}: {result.nodes_expanded} nodes expanded, distance {result.cost:.1f}",
        ax=ax,
    )

fig.tight_layout()
Path("docs").mkdir(exist_ok=True)
fig.savefig("docs/search_comparison.png", dpi=140, bbox_inches="tight")
print("Saved docs/search_comparison.png")
