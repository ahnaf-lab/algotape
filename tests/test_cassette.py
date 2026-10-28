import os
import tempfile
import unittest

from algotape import cassette
from algotape.algorithms.bfs import bfs_frames
from algotape.algorithms.dijkstra import dijkstra_frames
from algotape.algorithms.quicksort import quicksort_frames
from algotape.frames import Frame


class CassetteRoundTripTest(unittest.TestCase):
    def test_save_then_load_round_trips_bfs_frames(self):
        graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        original = list(bfs_frames(graph, "A"))

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "tape.json")
            cassette.save(original, path)
            tape = cassette.load(path)

        self.assertEqual(tape.algorithm, "bfs")
        self.assertEqual(tape.frames, original)

    def test_save_then_load_round_trips_dijkstra_frames(self):
        graph = {"A": [("B", 1), ("C", 4)], "B": [("C", 2)], "C": []}
        original = list(dijkstra_frames(graph, "A"))

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "tape.json")
            cassette.save(original, path)
            tape = cassette.load(path)

        self.assertEqual(tape.algorithm, "dijkstra")
        self.assertEqual(tape.frames, original)

    def test_save_then_load_round_trips_quicksort_frames(self):
        original = list(quicksort_frames([5, 3, 8, 1, 9, 2]))

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "tape.json")
            cassette.save(original, path)
            tape = cassette.load(path)

        self.assertEqual(tape.algorithm, "quicksort")
        self.assertEqual(tape.frames, original)

    def test_dumps_then_loads_round_trips_without_touching_disk(self):
        frames = [
            Frame(algorithm="quicksort", step=0, event="init", state={"values": [3, 1]}),
            Frame(algorithm="quicksort", step=1, event="done", state={"values": [1, 3]}),
        ]

        text = cassette.dumps(frames)
        tape = cassette.loads(text)

        self.assertEqual(tape.algorithm, "quicksort")
        self.assertEqual(tape.frames, frames)

    def test_frames_preserve_step_order_and_state_after_round_trip(self):
        frames = [
            Frame(algorithm="bfs", step=0, event="init", state={"queue": ["A"]}),
            Frame(algorithm="bfs", step=1, event="dequeue", state={"node": "A"}),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "tape.json")
            cassette.save(frames, path)
            tape = cassette.load(path)

        self.assertEqual([f.step for f in tape.frames], [0, 1])
        self.assertEqual(tape.frames[1].state, {"node": "A"})

    def test_empty_frame_sequence_is_rejected(self):
        with self.assertRaises(cassette.CassetteError):
            cassette.dumps([])

    def test_loading_wrong_format_version_is_rejected(self):
        text = '{"format_version": 999, "algorithm": "bfs", "frames": []}'
        with self.assertRaises(cassette.CassetteError):
            cassette.loads(text)

    def test_loading_malformed_json_is_rejected(self):
        with self.assertRaises(cassette.CassetteError):
            cassette.loads("not json at all")

    def test_loading_cassette_missing_frames_field_is_rejected(self):
        text = '{"format_version": 1, "algorithm": "bfs"}'
        with self.assertRaises(cassette.CassetteError):
            cassette.loads(text)


if __name__ == "__main__":
    unittest.main()
