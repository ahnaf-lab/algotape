import contextlib
import io
import json
import unittest

from algotape import cli


class CliTest(unittest.TestCase):
    def test_bfs_demo_prints_one_json_frame_per_line(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            exit_code = cli.main(["bfs"])
        self.assertEqual(exit_code, 0)
        lines = out.getvalue().strip().splitlines()
        self.assertGreater(len(lines), 0)
        first_frame = json.loads(lines[0])
        self.assertEqual(first_frame["algorithm"], "bfs")
        self.assertEqual(first_frame["event"], "init")

    def test_rejects_unknown_algorithm(self):
        with self.assertRaises(SystemExit):
            cli.main(["not-a-real-algorithm"])


if __name__ == "__main__":
    unittest.main()
