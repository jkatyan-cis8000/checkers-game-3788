"""Utils layer - move parsing helpers.

Contains functions for parsing user input into move objects.
May import from: types, config, utils.
"""

from __future__ import annotations

from src.types import Move, Position, ParsedMove
from src.config import COLUMN_MAP, REVERSE_COLUMN_MAP, ROW_MAP, REVERSE_ROW_MAP


def parse_move_input(input_str: str) -> ParsedMove | None:
    """
    Parse a move input string like 'a3 b4' or 'a3x b4' for capture.
    
    Returns ParsedMove with source and destination positions, or None if invalid.
    """
    try:
        input_str = input_str.strip()
        parts = input_str.split()
        
        if len(parts) < 2:
            return None
        
        source_str = parts[0]
        dest_str = parts[1]
        
        # Parse source position
        source_pos = parse_position(source_str)
        if source_pos is None:
            return None
        
        # Parse destination position
        dest_pos = parse_position(dest_str)
        if dest_pos is None:
            return None
        
        return ParsedMove(
            source=source_pos,
            destination=dest_pos,
            is_capture=len(parts) > 2 and parts[2] == 'x'
        )
    except (ValueError, IndexError):
        return None


def parse_position(pos_str: str) -> Position | None:
    """
    Parse a position string like 'a3' into a Position object.
    
    Returns Position or None if the format is invalid.
    """
    try:
        pos_str = pos_str.strip()
        if len(pos_str) != 2:
            return None
        
        col_char = pos_str[0].lower()
        row_char = pos_str[1]
        
        if col_char not in COLUMN_MAP:
            return None
        if row_char not in ROW_MAP:
            return None
        
        return Position(row=ROW_MAP[row_char], col=COLUMN_MAP[col_char])
    except (ValueError, IndexError):
        return None


def format_position(pos: Position) -> str:
    """
    Format a Position as a string like 'a3'.
    
    Uses the config's column and row name mappings.
    """
    col_name = REVERSE_COLUMN_MAP[pos.col]
    row_name = REVERSE_ROW_MAP[pos.row]
    return f"{col_name}{row_name}"
