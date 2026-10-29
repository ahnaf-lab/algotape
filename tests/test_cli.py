import contextlib
import io
import json
import os
import tempfile
import unittest

from algotape import cli


class CliTest(unittest.TestCase):
    def test_bfs_demo_prints_one_json_frame_per_line(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            exit_code = cli.main(["record", "bfs"])
        self.assertEqual(exit_code, 0)
        lines = out.getvalue().strip().splitlines()
        self.assertGreater(len(lines), 0)
        first_frame = json.loads(lines[0])
        self.assertEqual(first_frame["algorithm"], "bfs")
        self.assertEqual(first_frame["event"], "init")

    def test_rejects_unknown_algorithm(self):
        with self.assertRaises(SystemExit):
            cli.main(["record", "not-a-real-algorithm"])

    def test_record_output_then_play_round_trips_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "quicksort.cassette.json")

            record_out = io.StringIO()
            with contextlib.redirect_stdout(record_out):
                record_exit = cli.main(["record", "quicksort", "--output", path])
            self.assertEqual(record_exit, 0)
            self.assertTrue(os.path.exists(path))

            play_out = io.StringIO()
            with contextlib.redirect_stdout(play_out):
                play_exit = cli.main(["play", path])
            self.assertEqual(play_exit, 0)

            self.assertEqual(record_out.getvalue(), play_out.getvalue())

    def test_play_reports_missing_file_without_traceback(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            exit_code = cli.main(["play", "/nonexistent/path/to.cassette.json"])
        self.assertEqual(exit_code, 1)
        self.assertIn("algotape:", err.getvalue())

    def test_samples_lists_the_bundled_demo_names(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            exit_code = cli.main(["samples"])
        self.assertEqual(exit_code, 0)
        listing = out.getvalue()
        for name in ("maze", "graph", "array"):
            self.assertIn(name, listing)

    def test_play_with_sample_flag_needs_no_file_on_disk(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            exit_code = cli.main(["play", "--sample", "maze"])
        self.assertEqual(exit_code, 0)
        lines = out.getvalue().strip().splitlines()
        self.assertGreater(len(lines), 0)
        first_frame = json.loads(lines[0])
        self.assertEqual(first_frame["algorithm"], "bfs")
        self.assertEqual(first_frame["event"], "init")

    def test_play_rejects_unknown_sample_name(self):
        with self.assertRaises(SystemExit):
            cli.main(["play", "--sample", "not-a-real-sample"])

    def test_play_without_path_or_sample_is_an_error(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            exit_code = cli.main(["play"])
        self.assertEqual(exit_code, 1)
        self.assertIn("PATH or --sample", err.getvalue())

    def test_play_rejects_both_path_and_sample_together(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            exit_code = cli.main(["play", "some/path.json", "--sample", "array"])
        self.assertEqual(exit_code, 1)
        self.assertIn("not both", err.getvalue())

    def test_view_reports_out_of_range_step_without_opening_a_screen(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "quicksort.cassette.json")
            record_out = io.StringIO()
            with contextlib.redirect_stdout(record_out):
                cli.main(["record", "quicksort", "--output", path])

            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                exit_code = cli.main(["view", path, "--step", "9999"])

        self.assertEqual(exit_code, 1)
        self.assertIn("out of range", err.getvalue())


if __name__ == "__main__":
    unittest.main()
