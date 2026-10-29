"""VCR-style playback controls: a state machine over a cassette's frame index.

``Player`` tracks only two things: which frame index is current, and
whether playback is running. It knows nothing about curses, timing, or
wall-clock delays — a driving loop (the interactive TUI built in a later
milestone) is expected to call ``tick()`` on its own schedule while
playback is running, and call ``step_forward``/``step_backward``/``pause``/
``rewind`` in response to key presses. Keeping it free of real I/O is what
makes it possible to unit-test every transition directly.
"""

from dataclasses import dataclass


class PlayerError(ValueError):
    """Raised when a Player is constructed with an invalid frame count."""


@dataclass(frozen=True)
class PlayerState:
    """A snapshot of playback state: the current index and run/pause flag."""

    index: int
    playing: bool


class Player:
    """Play/pause/step/rewind over a fixed number of frames, by index."""

    def __init__(self, frame_count: int) -> None:
        if frame_count < 1:
            raise PlayerError("frame_count must be at least 1")
        self._frame_count = frame_count
        self._index = 0
        self._playing = False

    @property
    def frame_count(self) -> int:
        return self._frame_count

    @property
    def index(self) -> int:
        return self._index

    @property
    def playing(self) -> bool:
        return self._playing

    @property
    def at_start(self) -> bool:
        return self._index == 0

    @property
    def at_end(self) -> bool:
        return self._index == self._frame_count - 1

    def snapshot(self) -> PlayerState:
        return PlayerState(index=self._index, playing=self._playing)

    def play(self) -> None:
        """Start playback, unless already parked on the last frame."""
        if not self.at_end:
            self._playing = True

    def pause(self) -> None:
        """Stop playback. The current index is left untouched."""
        self._playing = False

    def toggle(self) -> None:
        """Flip between playing and paused."""
        if self._playing:
            self.pause()
        else:
            self.play()

    def tick(self) -> None:
        """Advance one frame if playing; auto-pause on reaching the end."""
        if not self._playing:
            return
        if self.at_end:
            self._playing = False
            return
        self._index += 1
        if self.at_end:
            self._playing = False

    def step_forward(self) -> None:
        """Move one frame forward, clamped to the last frame, and pause."""
        self._playing = False
        self._index = min(self._index + 1, self._frame_count - 1)

    def step_backward(self) -> None:
        """Move one frame backward, clamped to the first frame, and pause."""
        self._playing = False
        self._index = max(self._index - 1, 0)

    def rewind(self) -> None:
        """Jump back to the first frame and pause."""
        self._playing = False
        self._index = 0

    def seek(self, index: int) -> None:
        """Jump directly to ``index``, clamped into range, and pause."""
        self._playing = False
        self._index = max(0, min(index, self._frame_count - 1))
