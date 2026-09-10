import statistics
import time

from src.graph import Graph
from src.algorithms.brute_force import brute_force_shortest_path
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.algorithms.astar import astar_shortest_path


def time_call(fn, graph, start, end, repeats=25):
    """Median run time in seconds.

    Median rather than mean: these runs are fast enough that a single OS
    scheduling hiccup can be larger than the measurement itself, and one
    outlier would drag a mean well off the real cost.
    """
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(graph, start, end)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmark(sizes_all=range(4, 13), sizes_scaled_only=range(13, 61, 4)):
    results = {"n": [], "brute_force": [], "dijkstra": [], "astar": []}

    for n in sizes_all:
        graph = Graph.random_graph(n, edge_probability=0.4, seed=1)
        start, end = "0", str(n - 1)
        results["n"].append(n)
        # Brute-force gets fewer repeats purely because it is slow enough that
        # more of them would make the benchmark take minutes.
        results["brute_force"].append(time_call(brute_force_shortest_path, graph, start, end, repeats=5))
        results["dijkstra"].append(time_call(dijkstra_shortest_path, graph, start, end))
        results["astar"].append(time_call(astar_shortest_path, graph, start, end))
        print(f"n={n}: brute={results['brute_force'][-1]*1000:.3f}ms  "
              f"dijkstra={results['dijkstra'][-1]*1000:.4f}ms  astar={results['astar'][-1]*1000:.4f}ms")

    scaled = {"n": [], "dijkstra": [], "astar": [], "dijkstra_expanded": [], "astar_expanded": []}
    for n in sizes_scaled_only:
        graph = Graph.random_graph(n, edge_probability=0.15, seed=1)
        start, end = "0", str(n - 1)
        scaled["n"].append(n)
        scaled["dijkstra"].append(time_call(dijkstra_shortest_path, graph, start, end))
        scaled["astar"].append(time_call(astar_shortest_path, graph, start, end))
        scaled["dijkstra_expanded"].append(dijkstra_shortest_path(graph, start, end).nodes_expanded)
        scaled["astar_expanded"].append(astar_shortest_path(graph, start, end).nodes_expanded)
        print(f"n={n}: dijkstra={scaled['dijkstra'][-1]*1000:.4f}ms  astar={scaled['astar'][-1]*1000:.4f}ms  "
              f"expanded {scaled['dijkstra_expanded'][-1]} vs {scaled['astar_expanded'][-1]}  (brute-force skipped)")

    return results, scaled


if __name__ == "__main__":
    run_benchmark()
