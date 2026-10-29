"""Render a single Frame's internal state as plain text lines.

Turning a Frame into lines of text is kept separate from the curses
window that eventually draws them (see ``screen.py``), so the exact
rendered output can be golden-tested without needing a real terminal.
"""

from typing import Any, Dict, List

from .frames import Frame

#: index -> list of marker keys that point at a single array cell, and the
#: short label drawn underneath it.
_ARRAY_MARKERS = (("low", "low"), ("high", "high"), ("i", "i"), ("j", "j"), ("pivot_index", "piv"))


def render_frame(frame: Frame) -> List[str]:
    """Render ``frame`` as a list of plain text lines, one per row."""
    header = f"{frame.algorithm} | step {frame.step} | {frame.event}"
    lines = [header, "-" * len(header)]
    renderer = _RENDERERS.get(frame.algorithm, _render_generic)
    lines.extend(renderer(frame.state))
    return lines


def _cell_width(cells: List[Any]) -> int:
    return max((len(str(c)) for c in cells), default=1) + 2


def _render_row(values: List[Any], width: int) -> str:
    return "".join(f"{str(v):^{width}}" for v in values)


def _render_array(state: Dict[str, Any]) -> List[str]:
    array = state.get("array")
    if array is None:
        return [f"state: {state}"]

    labels: Dict[int, List[str]] = {}
    for key, label in _ARRAY_MARKERS:
        index = state.get(key)
        if isinstance(index, int) and 0 <= index < len(array):
            labels.setdefault(index, []).append(label)

    marker_text = {index: "/".join(names) for index, names in labels.items()}
    width = max(_cell_width(array), _cell_width(list(marker_text.values())))

    lines = [_render_row(array, width)]
    if marker_text:
        lines.append(_render_row([marker_text.get(i, "") for i in range(len(array))], width))
    return lines


def _render_bfs(state: Dict[str, Any]) -> List[str]:
    lines = []
    if "node" in state:
        lines.append(f"current: {state['node']}")
    if "neighbor" in state:
        lines.append(f"neighbor: {state['neighbor']}")
    lines.append(f"queue:   [{', '.join(state.get('queue', []))}]")
    lines.append(f"visited: [{', '.join(state.get('visited', []))}]")
    return lines


def _render_dijkstra(state: Dict[str, Any]) -> List[str]:
    lines = []
    if "node" in state:
        lines.append(f"current: {state['node']}")
    if "neighbor" in state:
        lines.append(
            f"relaxing: {state['node']} -> {state['neighbor']} = {state.get('new_dist')}"
        )

    dist = state.get("dist")
    if isinstance(dist, dict):
        nodes = sorted(dist)
        width = max(_cell_width(nodes), _cell_width([dist[n] for n in nodes]))
        lines.append(_render_row(nodes, width))
        lines.append(_render_row([dist[n] for n in nodes], width))
    elif dist is not None:
        lines.append(f"dist: {dist}")
    return lines


def _render_generic(state: Dict[str, Any]) -> List[str]:
    return [f"state: {state}"]


_RENDERERS = {
    "quicksort": _render_array,
    "bfs": _render_bfs,
    "dijkstra": _render_dijkstra,
}
