import unittest

from algotape.algorithms.bfs import bfs_frames
from algotape.recorder import record

from .helpers import load_fixture

GRAPH = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": [],
}


class BfsFramesTest(unittest.TestCase):
    def test_matches_fixture_exactly(self):
        frames = record(bfs_frames(GRAPH, "A"))
        self.assertEqual(frames, load_fixture("bfs_small.json"))

    def test_is_deterministic_across_runs(self):
        first = record(bfs_frames(GRAPH, "A"))
        second = record(bfs_frames(GRAPH, "A"))
        self.assertEqual(first, second)

    def test_starts_with_init_and_ends_with_done(self):
        frames = record(bfs_frames(GRAPH, "A"))
        self.assertEqual(frames[0]["event"], "init")
        self.assertEqual(frames[-1]["event"], "done")

    def test_visits_every_reachable_node_exactly_once(self):
        frames = record(bfs_frames(GRAPH, "A"))
        visit_neighbors = [
            f["state"]["neighbor"] for f in frames if f["event"] == "visit"
        ]
        self.assertEqual(sorted(visit_neighbors), ["B", "C", "D"])
        self.assertEqual(frames[-1]["state"]["visited"], ["A", "B", "C", "D"])

    def test_steps_are_sequential(self):
        frames = record(bfs_frames(GRAPH, "A"))
        self.assertEqual([f["step"] for f in frames], list(range(len(frames))))


if __name__ == "__main__":
    unittest.main()
