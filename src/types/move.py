"""Type definitions for move notation parsing."""

from __future__ import annotations

from dataclasses import dataclass

from . import Position


@dataclass(frozen=True)
class ParsedMove:
    """A move parsed from notation like 'a3 b4' or 'a3 b4 x' for capture."""
    source: Position
    destination: Position
    is_capture: bool = False
