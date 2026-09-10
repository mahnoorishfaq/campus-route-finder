"""Draws the campus map with matplotlib so the Streamlit app can show a route
instead of printing a list of location names."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.graph import Graph

EDGE_COLOR = "#cbd5e1"
NODE_COLOR = "#94a3b8"
EXPANDED_COLOR = "#fbbf24"
ROUTE_COLOR = "#2563eb"
START_COLOR = "#16a34a"
END_COLOR = "#dc2626"


def draw_map(
    graph: Graph,
    route: list[str] | None = None,
    expanded: list[str] | None = None,
    start: str | None = None,
    end: str | None = None,
    show_weights: bool = True,
    title: str = "",
    ax=None,
):
    expanded = set(expanded or [])
    route = route or []
    route_edges = {frozenset(pair) for pair in zip(route, route[1:])}

    # Pass an existing axes to draw several maps side by side in one figure.
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 7))
    else:
        fig = ax.get_figure()

    for a, b, weight in graph.edges():
        na, nb = graph.node(a), graph.node(b)
        on_route = frozenset((a, b)) in route_edges
        ax.plot(
            [na.x, nb.x],
            [na.y, nb.y],
            color=ROUTE_COLOR if on_route else EDGE_COLOR,
            linewidth=4 if on_route else 1.5,
            zorder=2 if on_route else 1,
            solid_capstyle="round",
        )
        if show_weights and not on_route:
            ax.text(
                (na.x + nb.x) / 2,
                (na.y + nb.y) / 2,
                f"{weight:g}",
                fontsize=7,
                color="#94a3b8",
                ha="center",
                va="center",
                zorder=3,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
            )

    for node_id in graph.nodes():
        node = graph.node(node_id)
        if node_id == start:
            color, size = START_COLOR, 260
        elif node_id == end:
            color, size = END_COLOR, 260
        elif node_id in route:
            color, size = ROUTE_COLOR, 180
        elif node_id in expanded:
            color, size = EXPANDED_COLOR, 180
        else:
            color, size = NODE_COLOR, 110

        ax.scatter(node.x, node.y, s=size, color=color, zorder=4, edgecolors="white", linewidths=1.5)
        ax.annotate(
            node.name,
            (node.x, node.y),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=8.5,
            color="#0f172a",
            zorder=5,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.8),
        )

    if title:
        ax.set_title(title, fontsize=12, color="#0f172a", pad=14)

    ax.set_xlabel("x coordinate (metres)", fontsize=9, color="#64748b")
    ax.set_ylabel("y coordinate (metres)", fontsize=9, color="#64748b")
    ax.margins(0.15)
    ax.grid(True, alpha=0.2)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors="#94a3b8", labelsize=8)
    fig.tight_layout()
    return fig
