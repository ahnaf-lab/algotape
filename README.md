# algotape

A terminal TUI that runs classic algorithms (Dijkstra, BFS, quicksort) step
by step, recording every internal state frame onto a cassette, then gives
you VCR controls to play, pause, step, and rewind through exactly how the
algorithm "thought." Built for people who want to see the reasoning, not
just the final answer.

This is an early milestone: BFS, Dijkstra, and quicksort are instrumented
to emit their internal state as a deterministic sequence of frames via
Python generators, those frame sequences can be saved to and loaded back
from a "cassette" file, a single frame's array/graph state can be drawn
onto a curses screen, and a play/pause/step/rewind state machine can
scrub through a cassette's frame index. Three cassettes also ship
pre-recorded inside the package (a maze, a graph, an array) for a
zero-setup demo. Wiring the state machine into a live, interactive
curses TUI comes in a later milestone.

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

### Rendering a frame

`algotape.render.render_frame(frame)` turns one `Frame` into a list of
plain text lines: a header naming the algorithm/step/event, then an
algorithm-specific view of its state — an array row with `low`/`high`/
`i`/`j`/pivot markers for quicksort, the current node/queue/visited set
for BFS, or a node/distance table for Dijkstra. Keeping this as a pure
function (no terminal required) is what makes it possible to golden-test
the exact rendered output for fixed frames in `tests/test_render.py`.

`algotape.screen.draw_frame(window, frame)` blits those same lines onto
a curses window, and the CLI's `view` command opens a real curses screen
to draw one frame from a saved cassette:

```
python -m algotape.cli view run.json --step 3
```

### VCR controls

`algotape.player.Player` is a play/pause/step/rewind state machine over a
cassette's frame index. It has no notion of curses or wall-clock time —
it only tracks the current index and whether playback is running — so a
driving loop can call `tick()` on its own schedule while playing, and
`step_forward()`/`step_backward()`/`rewind()`/`seek(index)` in response to
key presses:

```python
from algotape.player import Player

player = Player(frame_count=len(tape.frames))
player.play()
player.tick()           # advance one frame; auto-pauses at the last frame
player.step_backward()  # move back one frame and pause
player.rewind()         # jump back to frame 0 and pause
```

Wiring this into the curses `view` command as a live, interactive
playback TUI comes in a later milestone.

### Sample cassettes

Three cassettes ship inside the package itself — a maze, a weighted graph,
and an array — so there's a zero-setup demo to play or view without
recording anything first:

```
python -m algotape.cli samples
python -m algotape.cli play --sample maze
python -m algotape.cli view --sample graph --step 3
```

- `maze` — BFS exploring a small walled grid
- `graph` — Dijkstra finding shortest paths over a weighted graph
- `array` — quicksort sorting a small array

`--sample NAME` is accepted anywhere `play`/`view` would otherwise take a
cassette file `PATH`. `algotape.samples.load_sample(name)` loads the same
bundled cassette from Python, and `algotape.samples.sample_names()` lists
what's available.

Run the test suite with:

```
python -m unittest discover
```

## Status

This project is built autonomously, milestone by milestone, and every
change is gated on its automated tests passing before it is kept.
