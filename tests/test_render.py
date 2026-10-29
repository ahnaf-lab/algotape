import os
import unittest

from algotape.frames import Frame
from algotape.render import render_frame
from .helpers import load_fixture

GOLDEN_DIR = os.path.join(os.path.dirname(__file__), "golden")


def load_golden(name):
    with open(os.path.join(GOLDEN_DIR, f"{name}.txt")) as f:
        return f.read().splitlines()


def frame_from_fixture(fixture_name, index):
    data = load_fixture(fixture_name)[index]
    return Frame(
        algorithm=data["algorithm"],
        step=data["step"],
        event=data["event"],
        state=data["state"],
    )


class RenderFrameGoldenTest(unittest.TestCase):
    def test_quicksort_pivot_frame_marks_low_and_high(self):
        frame = frame_from_fixture("quicksort_small.json", 1)
        self.assertEqual(render_frame(frame), load_golden("quicksort_step1_pivot"))

    def test_quicksort_swap_frame_marks_i_and_j(self):
        frame = frame_from_fixture("quicksort_small.json", 2)
        self.assertEqual(render_frame(frame), load_golden("quicksort_step2_swap"))

    def test_bfs_init_frame_has_no_current_node_yet(self):
        frame = frame_from_fixture("bfs_small.json", 0)
        self.assertEqual(render_frame(frame), load_golden("bfs_step0_init"))

    def test_bfs_visit_frame_shows_current_node_and_neighbor(self):
        frame = frame_from_fixture("bfs_small.json", 2)
        self.assertEqual(render_frame(frame), load_golden("bfs_step2_visit"))

    def test_dijkstra_visit_frame_shows_scalar_distance(self):
        frame = frame_from_fixture("dijkstra_small.json", 1)
        self.assertEqual(render_frame(frame), load_golden("dijkstra_step1_visit"))

    def test_dijkstra_relax_frame_shows_distance_table(self):
        frame = frame_from_fixture("dijkstra_small.json", 2)
        self.assertEqual(render_frame(frame), load_golden("dijkstra_step2_relax"))


class RenderFrameBehaviorTest(unittest.TestCase):
    def test_header_always_names_algorithm_step_and_event(self):
        frame = Frame(algorithm="quicksort", step=7, event="swap", state={"array": [1, 2]})
        lines = render_frame(frame)
        self.assertEqual(lines[0], "quicksort | step 7 | swap")

    def test_array_row_and_marker_row_are_the_same_length(self):
        frame = Frame(
            algorithm="quicksort",
            step=0,
            event="pivot",
            state={"low": 0, "high": 2, "array": [10, 20, 30]},
        )
        lines = render_frame(frame)
        array_row, marker_row = lines[2], lines[3]
        self.assertEqual(len(array_row), len(marker_row))

    def test_unknown_algorithm_falls_back_to_generic_state_dump(self):
        frame = Frame(algorithm="mystery", step=0, event="init", state={"x": 1})
        lines = render_frame(frame)
        self.assertIn("state: {'x': 1}", lines)


if __name__ == "__main__":
    unittest.main()
