"""Turns a frame generator into a plain, serialisable list of frames."""

from typing import Any, Dict, Iterable, List

from .frames import Frame


def record(frame_iter: Iterable[Frame]) -> List[Dict[str, Any]]:
    """Fully drain a frame generator into a list of plain dicts."""
    return [frame.to_dict() for frame in frame_iter]
