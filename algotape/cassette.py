"""The cassette file format: serialize a frame sequence to disk and back.

A cassette is a JSON document with a small header (a format version and
the algorithm name) plus the ordered list of frames recorded during a run.
This is the file the VCR-style playback controls built in a later
milestone will read from and scrub through.
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from .frames import Frame

CASSETTE_FORMAT_VERSION = 1


class CassetteError(ValueError):
    """Raised when a file is not a valid, recognised cassette."""


@dataclass(frozen=True)
class Cassette:
    algorithm: str
    frames: List[Frame]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "format_version": CASSETTE_FORMAT_VERSION,
            "algorithm": self.algorithm,
            "frames": [frame.to_dict() for frame in self.frames],
        }


def frames_to_cassette(frames: Iterable[Frame]) -> Cassette:
    """Drain a frame sequence into a Cassette.

    The algorithm name is taken from the frames themselves, so the caller
    never has to repeat it.
    """
    frame_list = list(frames)
    if not frame_list:
        raise CassetteError("cannot build a cassette from an empty frame sequence")
    algorithm = frame_list[0].algorithm
    return Cassette(algorithm=algorithm, frames=frame_list)


def dumps(frames: Iterable[Frame]) -> str:
    """Serialize a frame sequence to a cassette JSON string."""
    return json.dumps(frames_to_cassette(frames).to_dict(), indent=2)


def loads(text: str) -> Cassette:
    """Parse a cassette JSON string back into a Cassette of Frame objects."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CassetteError(f"not valid JSON: {exc}") from exc
    return _cassette_from_dict(data)


def save(frames: Iterable[Frame], path: str) -> None:
    """Record a frame sequence onto a cassette file at ``path``."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(dumps(frames))
        f.write("\n")


def load(path: str) -> Cassette:
    """Load a cassette file back into a Cassette of Frame objects."""
    with open(path, "r", encoding="utf-8") as f:
        return loads(f.read())


def _cassette_from_dict(data: Any) -> Cassette:
    if not isinstance(data, dict):
        raise CassetteError("cassette must be a JSON object")

    if data.get("format_version") != CASSETTE_FORMAT_VERSION:
        raise CassetteError(
            f"unsupported cassette format version: {data.get('format_version')!r}"
        )

    algorithm = data.get("algorithm")
    raw_frames = data.get("frames")
    if not isinstance(algorithm, str) or not isinstance(raw_frames, list):
        raise CassetteError("cassette is missing required 'algorithm' or 'frames' field")

    frames = [_frame_from_dict(raw) for raw in raw_frames]
    return Cassette(algorithm=algorithm, frames=frames)


def _frame_from_dict(raw: Any) -> Frame:
    if not isinstance(raw, dict):
        raise CassetteError("each frame must be a JSON object")
    try:
        return Frame(
            algorithm=raw["algorithm"],
            step=raw["step"],
            event=raw["event"],
            state=raw.get("state", {}),
        )
    except KeyError as exc:
        raise CassetteError(f"frame missing required field: {exc}") from exc
