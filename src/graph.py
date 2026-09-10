import json
from dataclasses import dataclass
from math import hypot
from pathlib import Path

DEFAULT_MAP_PATH = Path(__file__).resolve().parent.parent / "data" / "campus_map.json"


@dataclass
class Node:
    id: str
    name: str
    x: float
    y: float


class Graph:
    def __init__(self):
        self._nodes: dict[str, Node] = {}
        self._adjacency: dict[str, list[tuple[str, float]]] = {}
        self._edges: list[tuple[str, str, float]] = []

    def add_node(self, node_id: str, name: str, x: float, y: float) -> None:
        self._nodes[node_id] = Node(node_id, name, x, y)
        self._adjacency.setdefault(node_id, [])

    def add_edge(self, a: str, b: str, weight: float, bidirectional: bool = True) -> None:
        self._adjacency[a].append((b, weight))
        if bidirectional:
            self._adjacency[b].append((a, weight))
        self._edges.append((a, b, weight))

    def neighbors(self, node_id: str) -> list[tuple[str, float]]:
        return self._adjacency.get(node_id, [])

    def node(self, node_id: str) -> Node:
        return self._nodes[node_id]

    def nodes(self) -> list[str]:
        return list(self._nodes.keys())

    def edges(self) -> list[tuple[str, str, float]]:
        return list(self._edges)

    def name_of(self, node_id: str) -> str:
        return self._nodes[node_id].name

    def euclidean(self, a: str, b: str) -> float:
        """Straight-line distance between two nodes, used as the A* heuristic."""
        na, nb = self._nodes[a], self._nodes[b]
        return hypot(na.x - nb.x, na.y - nb.y)

    @classmethod
    def from_json(cls, path: str | Path = DEFAULT_MAP_PATH) -> "Graph":
        with open(path) as f:
            data = json.load(f)
        g = cls()
        for n in data["nodes"]:
            g.add_node(n["id"], n["name"], n["x"], n["y"])
        for e in data["edges"]:
            g.add_edge(e["from"], e["to"], e["weight"])
        return g

    @classmethod
    def random_graph(cls, num_nodes: int, edge_probability: float = 0.35, seed: int = 42) -> "Graph":
        """Builds a random connected graph, used for benchmarking at scale."""
        import random
        rng = random.Random(seed)
        g = cls()
        for i in range(num_nodes):
            g.add_node(str(i), f"Node{i}", rng.uniform(0, 100), rng.uniform(0, 100))

        # Ensure connectivity: chain all nodes first
        # Edge weights are the exact straight-line distance, so the A* heuristic
        # stays admissible here too. Rounding them would let a weight fall below
        # the heuristic and break A*'s optimality guarantee.
        ids = [str(i) for i in range(num_nodes)]
        for i in range(num_nodes - 1):
            g.add_edge(ids[i], ids[i + 1], g.euclidean(ids[i], ids[i + 1]))

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if rng.random() < edge_probability:
                    g.add_edge(str(i), str(j), g.euclidean(str(i), str(j)))
        return g
