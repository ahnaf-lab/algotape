"""The frame format every instrumented algorithm emits.

A frame is one snapshot of an algorithm's internal state at a single
point in its execution. A full run produces an ordered sequence of
frames that a cassette can later be built from and scrubbed through.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class Frame:
    algorithm: str
    step: int
    event: str
    state: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "step": self.step,
            "event": self.event,
            "state": self.state,
        }
