"""Demo entry point. Loads the campus map and finds the shortest route between
two locations using all three algorithms, side by side."""
from src.graph import Graph
from src.algorithms.brute_force import brute_force_shortest_path
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.algorithms.astar import astar_shortest_path

ALGORITHMS = [
    ("Brute-force (naive)", brute_force_shortest_path),
    ("Dijkstra", dijkstra_shortest_path),
    ("A*", astar_shortest_path),
]


def describe_path(graph: Graph, path: list | None) -> str:
    if not path:
        return "No path found"
    return " -> ".join(graph.name_of(n) for n in path)


def main():
    graph = Graph.from_json()
    start, end = "gate", "hostel"

    print(f"Finding route: {graph.name_of(start)} -> {graph.name_of(end)}\n")

    for label, fn in ALGORITHMS:
        result = fn(graph, start, end)
        print(f"-- {label} --")
        print(f"Route: {describe_path(graph, result.path)}")
        print(f"Total distance: {result.cost:.2f}")
        print(f"Nodes expanded: {result.nodes_expanded}\n")


if __name__ == "__main__":
    main()
