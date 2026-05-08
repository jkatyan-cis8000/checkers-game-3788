"""Service layer - game logic.

Contains all business logic for the checkers game:
- Valid move generation
- Capture rules
- Kinging rules
- Win detection
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
    PieceType,
    Position,
)
from src.config import CONFIG


def create_initial_board() -> Board:
    """Create an 8x8 board with pieces in starting positions."""
    board: Board = [[None for _ in range(CONFIG.board_size)] for _ in range(CONFIG.board_size)]
    
    # Place black pieces (top 3 rows)
    for row in range(CONFIG.starting_rows_black):
        for col in range(CONFIG.board_size):
            if (row + col) % 2 == 1:
                board[row][col] = Piece(color=Color.BLACK, piece_type=PieceType.MAN)
    
    # Place red pieces (bottom 3 rows)
    for row in range(CONFIG.board_size - CONFIG.starting_rows_red, CONFIG.board_size):
        for col in range(CONFIG.board_size):
            if (row + col) % 2 == 1:
                board[row][col] = Piece(color=Color.RED, piece_type=PieceType.MAN)
    
    return board


def get_valid_moves(board: Board, position: Position) -> list[Move]:
    """Get all valid moves for a piece at the given position."""
    piece = board[position.row][position.col]
    if piece is None:
        return []
    
    moves = []
    
    # Determine movement directions based on color and piece type
    directions = []
    if piece.color == Color.RED or piece.piece_type == PieceType.KING:
        directions.append((-1, -1))  # Up-left
        directions.append((-1, 1))   # Up-right
    if piece.color == Color.BLACK or piece.piece_type == PieceType.KING:
        directions.append((1, -1))   # Down-left
        directions.append((1, 1))    # Down-right
    
    for dr, dc in directions:
        # Check normal move
        new_row = position.row + dr
        new_col = position.col + dc
        if is_on_board(new_row, new_col) and board[new_row][new_col] is None:
            moves.append(Move(from_pos=position, to_pos=Position(row=new_row, col=new_col)))
        
        # Check capture move
        jump_row = position.row + 2 * dr
        jump_col = position.col + 2 * dc
        if is_on_board(jump_row, jump_col) and board[jump_row][jump_col] is None:
            mid_row = position.row + dr
            mid_col = position.col + dc
            mid_piece = board[mid_row][mid_col]
            if mid_piece is not None and mid_piece.color != piece.color:
                moves.append(Move(from_pos=position, to_pos=Position(row=jump_row, col=jump_col)))
    
    return moves


def get_all_moves(board: Board, color: Color) -> list[tuple[Position, Move]]:
    """Get all valid moves for all pieces of a given color."""
    all_moves = []
    for row in range(CONFIG.board_size):
        for col in range(CONFIG.board_size):
            piece = board[row][col]
            if piece is not None and piece.color == color:
                position = Position(row=row, col=col)
                moves = get_valid_moves(board, position)
                for move in moves:
                    all_moves.append((position, move))
    return all_moves


def is_on_board(row: int, col: int) -> bool:
    """Check if a position is within the board boundaries."""
    return 0 <= row < CONFIG.board_size and 0 <= col < CONFIG.board_size


def execute_move(board: Board, move: Move) -> tuple[Board, Optional[CapturedPiece]]:
    """Execute a move and return the new board and any captured piece."""
    new_board = [row[:] for row in board]  # Deep copy
    piece = new_board[move.from_pos.row][move.from_pos.col]
    captured = None
    
    # Move piece
    new_board[move.from_pos.row][move.from_pos.col] = None
    new_board[move.to_pos.row][move.to_pos.col] = piece
    
    # Check for capture
    row_diff = abs(move.to_pos.row - move.from_pos.row)
    col_diff = abs(move.to_pos.col - move.from_pos.col)
    
    if row_diff == 2 and col_diff == 2:
        mid_row = (move.from_pos.row + move.to_pos.row) // 2
        mid_col = (move.from_pos.col + move.to_pos.col) // 2
        captured_piece = new_board[mid_row][mid_col]
        if captured_piece is not None:
            captured = CapturedPiece(
                position=Position(row=mid_row, col=mid_col),
                piece=captured_piece
            )
            new_board[mid_row][mid_col] = None
    
    # Check for kinging
    if piece.piece_type == PieceType.MAN:
        if (piece.color == Color.RED and move.to_pos.row == 0) or \
           (piece.color == Color.BLACK and move.to_pos.row == CONFIG.board_size - 1):
            new_board[move.to_pos.row][move.to_pos.col] = Piece(
                color=piece.color,
                piece_type=PieceType.KING
            )
    
    return new_board, captured


def create_board_copy(board: Board) -> Board:
    """Create a deep copy of the board."""
    return [row[:] for row in board]


def count_pieces(board: Board, color: Color) -> int:
    """Count the number of pieces for a given color."""
    count = 0
    for row in board:
        for piece in row:
            if piece is not None and piece.color == color:
                count += 1
    return count


def check_win(board: Board) -> Optional[Color]:
    """Check if there's a winner. Returns the winning color or None."""
    red_count = count_pieces(board, Color.RED)
    black_count = count_pieces(board, Color.BLACK)
    
    if red_count == 0:
        return Color.BLACK
    if black_count == 0:
        return Color.RED
    
    # Check if current player has any moves
    # This will be called after turn switching, so we check for the opponent
    # Actually, we need to know whose turn it is - handled in game state
    return None
