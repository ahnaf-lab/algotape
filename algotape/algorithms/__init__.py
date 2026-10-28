"""Instrumented algorithm implementations.

Every algorithm here is a generator function that yields Frame objects
instead of (or as well as) returning a final answer, so the full
sequence of internal states can be recorded and replayed later.
"""

from .bfs import bfs_frames
from .dijkstra import dijkstra_frames
from .quicksort import quicksort_frames

__all__ = ["bfs_frames", "dijkstra_frames", "quicksort_frames"]
