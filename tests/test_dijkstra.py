import unittest

from algotape.algorithms.dijkstra import dijkstra_frames
from algotape.recorder import record

from .helpers import load_fixture

GRAPH = {
    "A": [("B", 1), ("C", 4)],
    "B": [("C", 2), ("D", 5)],
    "C": [("D", 1)],
    "D": [],
}


class DijkstraFramesTest(unittest.TestCase):
    def test_matches_fixture_exactly(self):
        frames = record(dijkstra_frames(GRAPH, "A"))
        self.assertEqual(frames, load_fixture("dijkstra_small.json"))

    def test_is_deterministic_across_runs(self):
        first = record(dijkstra_frames(GRAPH, "A"))
        second = record(dijkstra_frames(GRAPH, "A"))
        self.assertEqual(first, second)

    def test_final_distances_are_shortest_paths(self):
        frames = record(dijkstra_frames(GRAPH, "A"))
        final_dist = frames[-1]["state"]["dist"]
        self.assertEqual(final_dist, {"A": 0, "B": 1, "C": 3, "D": 4})

    def test_starts_with_init_and_ends_with_done(self):
        frames = record(dijkstra_frames(GRAPH, "A"))
        self.assertEqual(frames[0]["event"], "init")
        self.assertEqual(frames[-1]["event"], "done")

    def test_every_node_is_eventually_visited(self):
        frames = record(dijkstra_frames(GRAPH, "A"))
        visited_nodes = {f["state"]["node"] for f in frames if f["event"] == "visit"}
        self.assertEqual(visited_nodes, {"A", "B", "C", "D"})


if __name__ == "__main__":
    unittest.main()
