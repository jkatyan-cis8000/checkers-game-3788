"""Service layer - game state management.

Manages the game state and provides methods to update it.
"""

from __future__ import annotations

from typing import Optional

from src.types import (
    Board,
    CapturedPiece,
    Color,
    GameState,
    Move,
    Piece,
    Position,
)
from src.service import game as game_service


def initialize_game() -> GameState:
    """Initialize a new game state."""
    board = game_service.create_initial_board()
    return GameState(
        board=board,
        current_turn=Color.RED,
        red_pieces=game_service.count_pieces(board, Color.RED),
        black_pieces=game_service.count_pieces(board, Color.BLACK),
        move_history=[]
    )


def make_move(game_state: GameState, move: Move) -> tuple[GameState, Optional[CapturedPiece]]:
    """
    Execute a move and return the updated game state.
    
    Returns the new game state and any captured piece.
    """
    board = game_service.create_board_copy(game_state.board)
    new_board, captured = game_service.execute_move(board, move)
    
    # Count remaining pieces
    red_count = game_service.count_pieces(new_board, Color.RED)
    black_count = game_service.count_pieces(new_board, Color.BLACK)
    
    # Switch turn
    next_turn = Color.BLACK if game_state.current_turn == Color.RED else Color.RED
    
    new_state = GameState(
        board=new_board,
        current_turn=next_turn,
        red_pieces=red_count,
        black_pieces=black_count,
        move_history=game_state.move_history + [move]
    )
    
    return new_state, captured


def check_win(game_state: GameState) -> Optional[Color]:
    """Check if there's a winner in the current game state."""
    if game_state.red_pieces == 0:
        return Color.BLACK
    if game_state.black_pieces == 0:
        return Color.RED
    
    return None
