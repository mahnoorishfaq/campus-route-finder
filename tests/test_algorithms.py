from src.graph import Graph
from src.algorithms.brute_force import brute_force_shortest_path
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.algorithms.astar import astar_shortest_path


def build_sample_graph():
    g = Graph()
    g.add_node("A", "A", 0, 0)
    g.add_node("B", "B", 1, 0)
    g.add_node("C", "C", 2, 0)
    g.add_node("D", "D", 1, 1)
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 1)
    g.add_edge("A", "D", 5)
    g.add_edge("D", "C", 2)
    return g


def assert_heuristic_is_admissible(graph: Graph):
    """A* is only guaranteed to find the optimal path if its heuristic never
    overestimates the remaining cost. Since the heuristic is straight-line
    distance, that holds exactly when no edge is shorter than the straight line
    between its endpoints, which is physically impossible for a real walking path.
    """
    for a, b, weight in graph.edges():
        straight_line = graph.euclidean(a, b)
        assert weight >= straight_line, (
            f"edge {a} -> {b} has weight {weight:.2f} but the straight-line "
            f"distance is {straight_line:.2f}, which makes the A* heuristic inadmissible"
        )


def test_campus_map_heuristic_is_admissible():
    assert_heuristic_is_admissible(Graph.from_json())


def test_random_benchmark_graph_heuristic_is_admissible():
    assert_heuristic_is_admissible(Graph.random_graph(30, edge_probability=0.2, seed=1))


def test_sample_graph_heuristic_is_admissible():
    assert_heuristic_is_admissible(build_sample_graph())


def test_all_three_algorithms_agree_on_optimal_cost():
    g = build_sample_graph()
    assert brute_force_shortest_path(g, "A", "C").cost == 2
    assert dijkstra_shortest_path(g, "A", "C").cost == 2
    assert astar_shortest_path(g, "A", "C").cost == 2


def test_all_three_agree_on_every_pair_of_campus_locations():
    g = Graph.from_json()
    for start in g.nodes():
        for end in g.nodes():
            brute = brute_force_shortest_path(g, start, end).cost
            dijkstra = dijkstra_shortest_path(g, start, end).cost
            astar = astar_shortest_path(g, start, end).cost
            assert round(brute, 6) == round(dijkstra, 6) == round(astar, 6), (
                f"{start} -> {end}: brute={brute}, dijkstra={dijkstra}, astar={astar}"
            )


def test_dijkstra_finds_correct_path():
    g = build_sample_graph()
    result = dijkstra_shortest_path(g, "A", "C")
    assert result.path == ["A", "B", "C"]
    assert result.cost == 2


def test_astar_expands_fewer_or_equal_nodes_than_dijkstra_on_campus_map():
    g = Graph.from_json()
    dijkstra = dijkstra_shortest_path(g, "gate", "hostel")
    astar = astar_shortest_path(g, "gate", "hostel")
    assert astar.nodes_expanded <= dijkstra.nodes_expanded


def test_expansion_order_matches_reported_count():
    g = Graph.from_json()
    result = astar_shortest_path(g, "gate", "hostel")
    assert len(result.expansion_order) == result.nodes_expanded
    assert result.expansion_order[0] == "gate"


def test_unreachable_node_returns_no_path():
    g = Graph()
    g.add_node("A", "A", 0, 0)
    g.add_node("B", "B", 10, 10)
    result = dijkstra_shortest_path(g, "A", "B")
    assert result.path is None
    assert result.cost == float("inf")
