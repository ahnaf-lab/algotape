# algotape

A terminal TUI that runs classic algorithms (Dijkstra, BFS, quicksort) step
by step, recording every internal state frame onto a cassette, then gives
you VCR controls to play, pause, step, and rewind through exactly how the
algorithm "thought." Built for people who want to see the reasoning, not
just the final answer.

This is an early milestone: BFS, Dijkstra, and quicksort are instrumented
to emit their internal state as a deterministic sequence of frames via
Python generators, and those frame sequences can now be saved to and
loaded back from a "cassette" file. The VCR-style interactive playback
TUI comes in a later milestone.

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

### Cassettes

A frame sequence can be saved to a "cassette" file — a plain JSON document
with a format version, the algorithm name, and the ordered list of frames —
and loaded back into the same `Frame` objects:

```python
from algotape import cassette
from algotape.algorithms.quicksort import quicksort_frames

cassette.save(quicksort_frames([5, 3, 8, 1, 9, 2]), "run.json")

tape = cassette.load("run.json")
tape.algorithm  # "quicksort"
tape.frames     # list[Frame], identical to the frames that were saved
```

`cassette.dumps`/`cassette.loads` do the same thing against a string
instead of a file, for callers that don't want to touch disk. Loading
rejects anything that isn't well-formed JSON, is missing a required
field, or carries a cassette format version this version of algotape
doesn't recognise.

A small CLI records a demo run and can replay a saved cassette, printing
the frame sequence as one JSON object per line either way:

```
python -m algotape.cli record bfs
python -m algotape.cli record dijkstra
python -m algotape.cli record quicksort --output run.json
python -m algotape.cli play run.json
```

Run the test suite with:

```
python -m unittest discover
```

## Status

This project is built autonomously, milestone by milestone, and every
change is gated on its automated tests passing before it is kept.
