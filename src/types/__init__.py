"""Type definitions for the Checkers game - main exports."""

from __future__ import annotations

from typing import TypeAlias

from .board import (
    Board,
    CapturedPiece,
    Color,
    GameState,
    Move,
    Piece,
    PieceType,
    Position,
)
from .events import EventType, GameOver, InvalidMove, Message, MoveInput, Prompt, UIEvent
from .move import ParsedMove

__all__ = [
    "Board",
    "CapturedPiece",
    "Color",
    "EventType",
    "GameOver",
    "GameState",
    "InvalidMove",
    "Message",
    "Move",
    "MoveInput",
    "ParsedMove",
    "Piece",
    "PieceType",
    "Position",
    "Prompt",
    "UIEvent",
]
