"""Dijkstra's shortest-path algorithm, instrumented to yield a frame per step."""

import heapq
from typing import Dict, Iterator, List, Tuple

from ..frames import Frame


def dijkstra_frames(
    graph: Dict[str, List[Tuple[str, float]]], start: str
) -> Iterator[Frame]:
    """Run Dijkstra's algorithm from ``start``, yielding a Frame per step.

    ``graph`` maps a node to a list of ``(neighbor, weight)`` edges. The
    heap stores ``(distance, node)`` pairs, so ties are broken by node name
    rather than insertion order, which keeps the emitted frames deterministic.
    """
    step = 0

    def emit(event: str, **state) -> Frame:
        nonlocal step
        frame = Frame(algorithm="dijkstra", step=step, event=event, state=state)
        step += 1
        return frame

    dist: Dict[str, float] = {start: 0}
    visited = set()
    heap: List[Tuple[float, str]] = [(0, start)]
    yield emit("init", start=start, dist=dict(dist))

    while heap:
        current_dist, node = heapq.heappop(heap)
        if node in visited:
            yield emit("skip_stale", node=node, dist=current_dist)
            continue
        visited.add(node)
        yield emit("visit", node=node, dist=current_dist)

        for neighbor, weight in graph.get(node, []):
            candidate = current_dist + weight
            if neighbor not in dist or candidate < dist[neighbor]:
                dist[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
                yield emit(
                    "relax",
                    node=node,
                    neighbor=neighbor,
                    new_dist=candidate,
                    dist=dict(dist),
                )
            else:
                yield emit(
                    "no_relax",
                    node=node,
                    neighbor=neighbor,
                    candidate=candidate,
                    dist=dict(dist),
                )

    yield emit("done", dist=dict(dist))
