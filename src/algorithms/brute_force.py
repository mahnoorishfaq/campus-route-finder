from src.graph import Graph
from src.result import SearchResult


def brute_force_shortest_path(graph: Graph, start: str, end: str) -> SearchResult:
    best_path = None
    best_cost = float("inf")
    expansion_order = []

    def dfs(current: str, visited: set, path: list, cost: float):
        nonlocal best_path, best_cost
        expansion_order.append(current)

        if current == end:
            if cost < best_cost:
                best_cost = cost
                best_path = path[:]
            return

        for neighbor, weight in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, visited, path, cost + weight)
                path.pop()
                visited.remove(neighbor)

    dfs(start, {start}, [start], 0.0)
    return SearchResult(best_path, best_cost, len(expansion_order), expansion_order)
