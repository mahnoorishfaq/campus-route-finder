import heapq

from src.graph import Graph
from src.result import SearchResult


def dijkstra_shortest_path(graph: Graph, start: str, end: str) -> SearchResult:
    distances = {node: float("inf") for node in graph.nodes()}
    distances[start] = 0.0
    previous = {}
    visited = set()
    pq = [(0.0, start)]
    expansion_order = []

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)

        if current == end:
            break

        for neighbor, weight in graph.neighbors(current):
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    if distances[end] == float("inf"):
        return SearchResult(None, float("inf"), len(expansion_order), expansion_order)

    path = [end]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return SearchResult(path, distances[end], len(expansion_order), expansion_order)
