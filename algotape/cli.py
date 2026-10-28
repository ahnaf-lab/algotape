"""Print the deterministic frame sequence of a demo run of an algorithm.

This is a thin preview of the instrumentation built in this milestone;
the VCR-style playback controls come in a later milestone.
"""

import argparse
import json
import sys
from typing import List, Optional

from .algorithms.bfs import bfs_frames
from .algorithms.dijkstra import dijkstra_frames
from .algorithms.quicksort import quicksort_frames

DEMO_GRAPH_UNWEIGHTED = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": [],
}

DEMO_GRAPH_WEIGHTED = {
    "A": [("B", 1), ("C", 4)],
    "B": [("C", 2), ("D", 5)],
    "C": [("D", 1)],
    "D": [],
}

DEMO_ARRAY = [5, 3, 8, 1, 9, 2]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="algotape",
        description="Print the deterministic state frames of a demo algorithm run, one JSON object per line.",
    )
    parser.add_argument("algorithm", choices=["bfs", "dijkstra", "quicksort"])
    args = parser.parse_args(argv)

    if args.algorithm == "bfs":
        frames = bfs_frames(DEMO_GRAPH_UNWEIGHTED, "A")
    elif args.algorithm == "dijkstra":
        frames = dijkstra_frames(DEMO_GRAPH_WEIGHTED, "A")
    else:
        frames = quicksort_frames(DEMO_ARRAY)

    for frame in frames:
        print(json.dumps(frame.to_dict()))

    return 0


if __name__ == "__main__":
    sys.exit(main())
