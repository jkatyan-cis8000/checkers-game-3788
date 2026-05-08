"""Configuration constants for the Checkers game."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    """Configuration for the checkers game."""
    board_size: int = 8
    starting_rows_red: int = 3
    starting_rows_black: int = 3
    max_moves_without_capture: int = 50


CONFIG = GameConfig()

# Column notation mapping
COLUMN_NAMES = "abcdefgh"
COLUMN_MAP = {col: idx for idx, col in enumerate(COLUMN_NAMES)}
REVERSE_COLUMN_MAP = {idx: col for col, idx in COLUMN_MAP.items()}

# Row notation (1-8 from bottom)
ROW_NAMES = "87654321"
ROW_MAP = {row: idx for idx, row in enumerate(ROW_NAMES)}
REVERSE_ROW_MAP = {idx: row for row, idx in ROW_MAP.items()}
