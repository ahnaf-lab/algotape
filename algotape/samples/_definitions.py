"""Source definitions for the bundled sample cassettes.

Each sample is defined here as plain data (a maze grid, a weighted graph,
an array) so the shipped cassette files can be regenerated and checked
against the exact frame sequence the current algorithms produce, instead
of being hand-maintained blobs that could silently drift out of sync with
``algotape.algorithms``.
"""

from typing import Dict, Iterator, List, Tuple

from ..algorithms.bfs import bfs_frames
from ..algorithms.dijkstra import dijkstra_frames
from ..algorithms.quicksort import quicksort_frames
from ..frames import Frame

#: '.' is an open cell, '#' is a wall. Rows need not all be the same length.
MAZE_GRID = [
    "....",
    ".##.",
    "..#.",
    "#...",
]
MAZE_START = "0,0"

GRAPH: Dict[str, List[Tuple[str, float]]] = {
    "A": [("B", 2), ("C", 5)],
    "B": [("C", 1), ("D", 4)],
    "C": [("D", 1), ("E", 3)],
    "D": [("E", 2), ("F", 6)],
    "E": [("F", 1)],
    "F": [],
}
GRAPH_START = "A"

ARRAY = [7, 2, 9, 4, 1, 8, 5, 3]

_DIRECTIONS: Tuple[Tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _maze_adjacency(grid: List[str]) -> Dict[str, List[str]]:
    """Turn an ASCII maze grid into the node/neighbour map ``bfs_frames`` expects.

    Each open cell becomes a node named ``"row,col"``, linked to its open
    up/down/left/right neighbours in that fixed order, which keeps the
    emitted frame sequence deterministic.
    """
    adjacency: Dict[str, List[str]] = {}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != ".":
                continue
            neighbors = []
            for dr, dc in _DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == ".":
                    neighbors.append(f"{nr},{nc}")
            adjacency[f"{r},{c}"] = neighbors
    return adjacency


def maze_frames() -> Iterator[Frame]:
    """Frame sequence for BFS exploring the bundled maze from ``MAZE_START``."""
    return bfs_frames(_maze_adjacency(MAZE_GRID), MAZE_START)


def graph_frames() -> Iterator[Frame]:
    """Frame sequence for Dijkstra over the bundled weighted graph."""
    return dijkstra_frames(GRAPH, GRAPH_START)


def array_frames() -> Iterator[Frame]:
    """Frame sequence for quicksort over the bundled array."""
    return quicksort_frames(ARRAY)
