"""Instrumented algorithms that emit their internal state as a sequence of frames."""

from .cassette import Cassette, CassetteError, dumps, load, loads, save
from .frames import Frame
from .recorder import record

__all__ = [
    "Frame",
    "record",
    "Cassette",
    "CassetteError",
    "save",
    "load",
    "dumps",
    "loads",
]
