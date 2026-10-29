"""Thin curses wrapper that draws a single Frame onto a window.

``draw_frame`` only calls ``erase``/``addstr``/``refresh`` on whatever
window-like object it is given, so it can be exercised in tests against
a plain stand-in object instead of a real terminal. All of the actual
text layout lives in ``render.py``.
"""

import curses

from .frames import Frame
from .render import render_frame


def draw_frame(window, frame: Frame) -> None:
    """Clear ``window`` and draw ``frame``'s rendered lines onto it."""
    window.erase()
    max_y, max_x = window.getmaxyx()
    for row, line in enumerate(render_frame(frame)):
        if row >= max_y:
            break
        window.addstr(row, 0, line[: max(max_x - 1, 0)])
    window.refresh()


def view_frame(frame: Frame) -> None:
    """Open a curses screen, draw ``frame``, and wait for a keypress."""

    def _run(window) -> None:
        draw_frame(window, frame)
        window.getch()

    curses.wrapper(_run)
