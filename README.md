# algotape

A terminal TUI that runs classic algorithms (Dijkstra, BFS, quicksort) step
by step, recording every internal state frame onto a cassette, then gives
you VCR controls to play, pause, step, and rewind through exactly how the
algorithm "thought." Built for people who want to see the reasoning, not
just the final answer.

This is an early milestone: BFS, Dijkstra, and quicksort are instrumented
to emit their internal state as a deterministic sequence of frames via
Python generators. The VCR-style playback TUI and the cassette file format
come in later milestones.

## Install

Requires Python 3.9+. No third-party runtime dependencies.

```
pip install -e .
```

## Usage

Each algorithm is a generator that yields a `Frame` for every meaningful
step it takes (an init, a visit, a relax, a swap, a done, and so on),
instead of just returning a final answer:

```python
from algotape.algorithms.bfs import bfs_frames
from algotape.recorder import record

graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
frames = record(bfs_frames(graph, "A"))  # list of plain dicts, one per step
```

`algotape.algorithms` also provides `dijkstra_frames(graph, start)` (graph
maps a node to a list of `(neighbor, weight)` edges) and
`quicksort_frames(values)`.

A small CLI prints the frame sequence of a demo run, one JSON object per
line, as a preview of the instrumentation:

```
python -m algotape.cli bfs
python -m algotape.cli dijkstra
python -m algotape.cli quicksort
```

Run the test suite with:

```
python -m unittest discover
```

## Status

This project is built autonomously, milestone by milestone, and every
change is gated on its automated tests passing before it is kept.
