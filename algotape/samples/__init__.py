"""Bundled, pre-recorded cassettes for a zero-setup demo.

Every other way of getting a cassette requires the caller to supply an
input (a graph, an array) to run an algorithm on. These three ship the
already-recorded result of a fixed, interesting input for each
instrumented algorithm, so ``algotape.cli`` can play or view a demo with
nothing but a sample name.
"""

from importlib import resources
from typing import Iterator, List

from .. import cassette
from ..cassette import Cassette
from ..frames import Frame
from . import _definitions

#: sample name -> bundled cassette filename, one-line description, and the
#: frame generator its cassette was recorded from.
_SAMPLES = {
    "maze": (
        "maze.cassette.json",
        "BFS exploring a small walled maze",
        _definitions.maze_frames,
    ),
    "graph": (
        "graph.cassette.json",
        "Dijkstra finding shortest paths over a weighted graph",
        _definitions.graph_frames,
    ),
    "array": (
        "array.cassette.json",
        "quicksort sorting a small array",
        _definitions.array_frames,
    ),
}


class SampleNotFoundError(KeyError):
    """Raised when a sample name doesn't match a bundled cassette."""


def sample_names() -> List[str]:
    """Names of the bundled sample cassettes, in a fixed, stable order."""
    return list(_SAMPLES)


def sample_description(name: str) -> str:
    """One-line description of what the named sample demonstrates."""
    try:
        return _SAMPLES[name][1]
    except KeyError as exc:
        raise SampleNotFoundError(name) from exc


def sample_frames(name: str) -> Iterator[Frame]:
    """Freshly regenerate the frame sequence a bundled sample was recorded from."""
    try:
        builder = _SAMPLES[name][2]
    except KeyError as exc:
        raise SampleNotFoundError(name) from exc
    return builder()


def load_sample(name: str) -> Cassette:
    """Load the bundled, pre-recorded cassette for ``name``."""
    try:
        filename = _SAMPLES[name][0]
    except KeyError as exc:
        raise SampleNotFoundError(name) from exc
    text = resources.files(__package__).joinpath(filename).read_text(encoding="utf-8")
    return cassette.loads(text)
