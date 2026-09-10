from typing import NamedTuple


class SearchResult(NamedTuple):
    path: list[str] | None
    cost: float
    nodes_expanded: int
    # The order nodes came off the frontier. The Streamlit app replays this to
    # show A* heading for the goal while Dijkstra spreads out in all directions.
    expansion_order: list[str]
