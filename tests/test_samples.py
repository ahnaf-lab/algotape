import unittest

from algotape import samples

EXPECTED_ALGORITHMS = {
    "maze": "bfs",
    "graph": "dijkstra",
    "array": "quicksort",
}


class SamplesTest(unittest.TestCase):
    def test_sample_names_match_the_three_bundled_demos(self):
        self.assertEqual(set(samples.sample_names()), set(EXPECTED_ALGORITHMS))

    def test_each_sample_loads_as_a_well_formed_cassette(self):
        for name, algorithm in EXPECTED_ALGORITHMS.items():
            tape = samples.load_sample(name)
            self.assertEqual(tape.algorithm, algorithm)
            self.assertGreater(len(tape.frames), 1)
            self.assertEqual(tape.frames[0].event, "init")
            self.assertEqual(tape.frames[-1].event, "done")

    def test_bundled_cassette_matches_freshly_regenerated_frames(self):
        """The shipped JSON must match what the source definitions produce now."""
        for name in EXPECTED_ALGORITHMS:
            shipped = [frame.to_dict() for frame in samples.load_sample(name).frames]
            fresh = [frame.to_dict() for frame in samples.sample_frames(name)]
            self.assertEqual(shipped, fresh)

    def test_unknown_sample_name_is_rejected(self):
        with self.assertRaises(samples.SampleNotFoundError):
            samples.load_sample("not-a-real-sample")
        with self.assertRaises(samples.SampleNotFoundError):
            samples.sample_description("not-a-real-sample")
        with self.assertRaises(samples.SampleNotFoundError):
            list(samples.sample_frames("not-a-real-sample"))

    def test_sample_description_is_a_nonempty_string(self):
        for name in samples.sample_names():
            description = samples.sample_description(name)
            self.assertIsInstance(description, str)
            self.assertGreater(len(description), 0)


if __name__ == "__main__":
    unittest.main()
