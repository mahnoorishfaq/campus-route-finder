import heapq

from src.graph import Graph
from src.result import SearchResult


def astar_shortest_path(graph: Graph, start: str, end: str) -> SearchResult:
    g_score = {node: float("inf") for node in graph.nodes()}
    g_score[start] = 0.0
    previous = {}
    visited = set()
    pq = [(graph.euclidean(start, end), start)]
    expansion_order = []

    while pq:
        _, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)

        if current == end:
            break

        for neighbor, weight in graph.neighbors(current):
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                previous[neighbor] = current
                f_score = tentative_g + graph.euclidean(neighbor, end)
                heapq.heappush(pq, (f_score, neighbor))

    if g_score[end] == float("inf"):
        return SearchResult(None, float("inf"), len(expansion_order), expansion_order)

    path = [end]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return SearchResult(path, g_score[end], len(expansion_order), expansion_order)
