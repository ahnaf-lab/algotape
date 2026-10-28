"""Instrumented algorithms that emit their internal state as a sequence of frames."""

from .frames import Frame
from .recorder import record

__all__ = ["Frame", "record"]
