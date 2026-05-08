"""Type definitions for UI events."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union


class EventType(Enum):
    """Types of UI events."""
    MOVE_INPUT = "move_input"
    INVALID_MOVE = "invalid_move"
    GAME_OVER = "game_over"
    PROMPT = "prompt"
    MESSAGE = "message"


@dataclass(frozen=True)
class MoveInput:
    """User input for a move."""
    move_string: str


@dataclass(frozen=True)
class InvalidMove:
    """Event for an invalid move attempt."""
    move_string: str
    reason: str


@dataclass(frozen=True)
class GameOver:
    """Event for game over."""
    winner_color: str


@dataclass(frozen=True)
class Prompt:
    """Event prompting user for input."""
    message: str


@dataclass(frozen=True)
class Message:
    """Event for informational messages."""
    message: str


UIEvent = Union[MoveInput, InvalidMove, GameOver, Prompt, Message]
