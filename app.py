"""Streamlit front end for the campus route finder.

Run locally with:  streamlit run app.py
"""
import statistics
import time

import matplotlib.pyplot as plt
import streamlit as st

from src.algorithms.astar import astar_shortest_path
from src.algorithms.brute_force import brute_force_shortest_path
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.graph import Graph
from src.plotting import draw_map

ALGORITHMS = {
    "A*": astar_shortest_path,
    "Dijkstra": dijkstra_shortest_path,
    "Brute-force (naive)": brute_force_shortest_path,
}

st.set_page_config(page_title="Campus Route Finder", page_icon="🗺️", layout="wide")


@st.cache_data
def load_graph() -> Graph:
    return Graph.from_json()


def time_algorithm(fn, graph, start, end, repeats=5):
    """Average wall-clock time in milliseconds over a few runs."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(graph, start, end)
        times.append(time.perf_counter() - t0)
    return statistics.mean(times) * 1000


def route_as_text(graph, path):
    if not path:
        return "No route found"
    return "  ➜  ".join(graph.name_of(n) for n in path)


def show_figure(fig):
    st.pyplot(fig)
    plt.close(fig)


graph = load_graph()
names_to_ids = {graph.name_of(n): n for n in graph.nodes()}
location_names = sorted(names_to_ids)

st.title("🗺️ Campus Route Finder")
st.caption(
    "Finds the shortest walking route between two campus locations, and compares "
    "three shortest-path algorithms solving the exact same problem."
)

with st.sidebar:
    st.header("Plan a route")
    start_name = st.selectbox("Start", location_names, index=location_names.index("Main Gate"))
    end_name = st.selectbox("Destination", location_names, index=location_names.index("Hostel Block"))
    show_weights = st.checkbox("Show path distances on the map", value=True)
    st.divider()
    st.markdown(
        "**How to read the map**\n\n"
        "- 🟢 start\n"
        "- 🔴 destination\n"
        "- 🔵 chosen route\n"
        "- 🟡 nodes the search looked at"
    )

start, end = names_to_ids[start_name], names_to_ids[end_name]

if start == end:
    st.info("Pick two different locations to see a route.")
    show_figure(draw_map(graph, start=start, end=end, show_weights=show_weights, title="Campus map"))
    st.stop()

results = {label: fn(graph, start, end) for label, fn in ALGORITHMS.items()}
best = results["A*"]

if best.path is None:
    st.error(f"There is no walking path between {start_name} and {end_name} on this map.")
    st.stop()

map_tab, compare_tab, search_tab = st.tabs(["Route map", "Algorithm comparison", "Watch the search"])

with map_tab:
    left, right = st.columns([3, 1])
    with left:
        show_figure(
            draw_map(
                graph,
                route=best.path,
                start=start,
                end=end,
                show_weights=show_weights,
                title=f"{start_name} to {end_name}",
            )
        )
    with right:
        st.metric("Total distance", f"{best.cost:.1f} m")
        st.metric("Stops along the way", len(best.path))
        st.markdown("**Route**")
        for i, node_id in enumerate(best.path, start=1):
            st.write(f"{i}. {graph.name_of(node_id)}")

with compare_tab:
    st.subheader("Same problem, three algorithms")
    st.write(
        "All three return the same optimal distance. What separates them is how much "
        "work they do to get there."
    )

    rows = []
    for label, fn in ALGORITHMS.items():
        result = results[label]
        rows.append(
            {
                "Algorithm": label,
                "Distance": f"{result.cost:.1f} m",
                "Nodes expanded": result.nodes_expanded,
                "Time": f"{time_algorithm(fn, graph, start, end):.3f} ms",
                "Route": route_as_text(graph, result.path),
            }
        )

    st.dataframe(rows, hide_index=True)

    astar_expanded = results["A*"].nodes_expanded
    brute_expanded = results["Brute-force (naive)"].nodes_expanded
    st.success(
        f"On this route, A* reached the destination after expanding {astar_expanded} nodes. "
        f"Brute-force expanded {brute_expanded} to find the same answer."
    )
    st.caption(
        "Read the **nodes expanded** column, not the time column. This map has only 10 "
        "locations, so every algorithm finishes in well under a millisecond and the timings "
        "are mostly measurement noise. A* can even look slower than Dijkstra here, because "
        "computing the heuristic costs something and there is barely any search to save. "
        "Nodes expanded is the honest comparison, and the benchmark in the README shows what "
        "happens to each algorithm as the graph grows."
    )

with search_tab:
    st.subheader("Step through the search")
    st.write(
        "A* uses straight-line distance to the destination as a hint, so it heads toward "
        "the goal. Dijkstra has no such hint and spreads outward evenly. Drag the slider "
        "to replay each one node by node."
    )

    choice = st.radio("Algorithm", list(ALGORITHMS), horizontal=True)
    order = results[choice].expansion_order
    step = st.slider("Nodes expanded so far", 1, len(order), len(order))
    seen = order[:step]

    show_figure(
        draw_map(
            graph,
            route=best.path if step == len(order) else None,
            expanded=seen,
            start=start,
            end=end,
            show_weights=False,
            title=f"{choice}: {step} of {len(order)} expansions",
        )
    )
    st.write("**Expansion order:** " + " → ".join(graph.name_of(n) for n in seen))
