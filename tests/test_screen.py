import unittest

from algotape.frames import Frame
from algotape.render import render_frame
from algotape.screen import draw_frame


class FakeWindow:
    """Stand-in for a curses window that records calls instead of drawing."""

    def __init__(self, height=24, width=80):
        self._height = height
        self._width = width
        self.erased = False
        self.refreshed = False
        self.written = {}

    def erase(self):
        self.erased = True

    def getmaxyx(self):
        return self._height, self._width

    def addstr(self, row, col, text):
        self.written[(row, col)] = text

    def refresh(self):
        self.refreshed = True


class DrawFrameTest(unittest.TestCase):
    def test_draws_every_rendered_line_at_its_row(self):
        frame = Frame(algorithm="quicksort", step=0, event="init", state={"array": [3, 1, 2]})
        window = FakeWindow()

        draw_frame(window, frame)

        expected_lines = render_frame(frame)
        for row, line in enumerate(expected_lines):
            self.assertEqual(window.written[(row, 0)], line)

    def test_erases_and_refreshes_the_window(self):
        frame = Frame(algorithm="bfs", step=0, event="init", state={"queue": ["A"], "visited": ["A"]})
        window = FakeWindow()

        draw_frame(window, frame)

        self.assertTrue(window.erased)
        self.assertTrue(window.refreshed)

    def test_truncates_lines_wider_than_the_window(self):
        frame = Frame(
            algorithm="dijkstra",
            step=0,
            event="init",
            state={"dist": {"very-long-node-name": 0}},
        )
        window = FakeWindow(height=24, width=10)

        draw_frame(window, frame)

        for text in window.written.values():
            self.assertLessEqual(len(text), 9)

    def test_does_not_write_past_the_bottom_of_the_window(self):
        frame = Frame(algorithm="quicksort", step=0, event="init", state={"array": [1, 2, 3]})
        window = FakeWindow(height=2, width=80)

        draw_frame(window, frame)

        self.assertTrue(all(row < 2 for row, _ in window.written))


if __name__ == "__main__":
    unittest.main()
