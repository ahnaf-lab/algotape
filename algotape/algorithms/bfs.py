"""Breadth-first search, instrumented to yield a frame for every state change."""

from collections import deque
from typing import Dict, Iterator, List

from ..frames import Frame


def bfs_frames(graph: Dict[str, List[str]], start: str) -> Iterator[Frame]:
    """Walk ``graph`` breadth-first from ``start``, yielding a Frame per step.

    ``graph`` maps a node to its neighbours in the exact order they should
    be explored, which is what keeps the emitted frame sequence deterministic
    for a given input.
    """
    step = 0

    def emit(event: str, **state) -> Frame:
        nonlocal step
        frame = Frame(algorithm="bfs", step=step, event=event, state=state)
        step += 1
        return frame

    visited = {start}
    queue = deque([start])
    yield emit("init", start=start, queue=list(queue), visited=sorted(visited))

    while queue:
        node = queue.popleft()
        yield emit("dequeue", node=node, queue=list(queue), visited=sorted(visited))
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            queue.append(neighbor)
            yield emit(
                "visit",
                node=node,
                neighbor=neighbor,
                queue=list(queue),
                visited=sorted(visited),
            )

    yield emit("done", visited=sorted(visited))
