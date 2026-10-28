import unittest

from algotape.algorithms.quicksort import quicksort_frames
from algotape.recorder import record

from .helpers import load_fixture

VALUES = [5, 3, 8, 1, 9, 2]


class QuicksortFramesTest(unittest.TestCase):
    def test_matches_fixture_exactly(self):
        frames = record(quicksort_frames(VALUES))
        self.assertEqual(frames, load_fixture("quicksort_small.json"))

    def test_is_deterministic_across_runs(self):
        first = record(quicksort_frames(VALUES))
        second = record(quicksort_frames(VALUES))
        self.assertEqual(first, second)

    def test_final_array_is_sorted(self):
        frames = record(quicksort_frames(VALUES))
        self.assertEqual(frames[-1]["state"]["array"], sorted(VALUES))

    def test_does_not_mutate_input_list(self):
        original = list(VALUES)
        record(quicksort_frames(VALUES))
        self.assertEqual(VALUES, original)

    def test_starts_with_init_and_ends_with_done(self):
        frames = record(quicksort_frames(VALUES))
        self.assertEqual(frames[0]["event"], "init")
        self.assertEqual(frames[-1]["event"], "done")

    def test_handles_already_sorted_and_empty_input(self):
        self.assertEqual(
            record(quicksort_frames([1, 2, 3]))[-1]["state"]["array"], [1, 2, 3]
        )
        self.assertEqual(record(quicksort_frames([]))[-1]["state"]["array"], [])


if __name__ == "__main__":
    unittest.main()
