"""Command-line entry point for recording, replaying, and viewing cassettes.

``record`` runs a demo algorithm and prints its frame sequence as one JSON
object per line, optionally saving the run to a cassette file. ``play``
loads a previously saved cassette and prints its frames the same way.
``view`` draws a single frame from a cassette onto a curses screen. The
full VCR-style interactive playback controls (step, pause, rewind) come
in a later milestone.
"""

import argparse
import json
import sys
from typing import List, Optional

from . import cassette
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


def _demo_frames(algorithm: str):
    if algorithm == "bfs":
        return bfs_frames(DEMO_GRAPH_UNWEIGHTED, "A")
    if algorithm == "dijkstra":
        return dijkstra_frames(DEMO_GRAPH_WEIGHTED, "A")
    return quicksort_frames(DEMO_ARRAY)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="algotape",
        description="Record and replay algorithm frame sequences as cassettes.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser(
        "record", help="run a demo algorithm and print its frame sequence"
    )
    record_parser.add_argument("algorithm", choices=["bfs", "dijkstra", "quicksort"])
    record_parser.add_argument(
        "--output",
        metavar="PATH",
        help="also save the run to a cassette file at PATH",
    )

    play_parser = subparsers.add_parser(
        "play", help="load a cassette file and print its frame sequence"
    )
    play_parser.add_argument("path", metavar="PATH", help="cassette file to load")

    view_parser = subparsers.add_parser(
        "view", help="draw one frame from a cassette file on a curses screen"
    )
    view_parser.add_argument("path", metavar="PATH", help="cassette file to load")
    view_parser.add_argument(
        "--step",
        type=int,
        default=0,
        help="index into the cassette's frame sequence to draw (default: 0)",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "record":
        frames = list(_demo_frames(args.algorithm))
        if args.output:
            cassette.save(frames, args.output)
        for frame in frames:
            print(json.dumps(frame.to_dict()))
        return 0

    try:
        tape = cassette.load(args.path)
    except (OSError, cassette.CassetteError) as exc:
        print(f"algotape: {exc}", file=sys.stderr)
        return 1

    if args.command == "play":
        for frame in tape.frames:
            print(json.dumps(frame.to_dict()))
        return 0

    if not 0 <= args.step < len(tape.frames):
        print(
            f"algotape: step {args.step} is out of range (0..{len(tape.frames) - 1})",
            file=sys.stderr,
        )
        return 1

    from .screen import view_frame  # imports curses, only needed for this command

    view_frame(tape.frames[args.step])
    return 0


if __name__ == "__main__":
    sys.exit(main())
