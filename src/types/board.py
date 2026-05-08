"""Type definitions for the Checkers game."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import NewType


class Color(Enum):
    """Piece color - RED moves up, BLACK moves down."""
    RED = "red"
    BLACK = "black"


class PieceType(Enum):
    """Type of piece - regular or king."""
    MAN = "man"
    KING = "king"


@dataclass(frozen=True)
class Position:
    """Board position as (row, col)."""
    row: int
    col: int


@dataclass(frozen=True)
class Piece:
    """A checkers piece."""
    color: Color
    piece_type: PieceType = PieceType.MAN


@dataclass(frozen=True)
class Move:
    """A move from one position to another."""
    from_pos: Position
    to_pos: Position


@dataclass(frozen=True)
class CapturedPiece:
    """A piece that was captured during a move."""
    position: Position
    piece: Piece


@dataclass
class GameState:
    """Current state of the game."""
    board: list[list[Piece | None]]
    current_turn: Color
    red_pieces: int
    black_pieces: int
    move_history: list[Move]


# Board representation: 8x8 grid
Board = list[list[Piece | None]]
