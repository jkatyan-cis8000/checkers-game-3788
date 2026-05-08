"""UI layer - CLI interface.

Contains the command-line interface for the checkers game.
May import from: types, config, service, runtime, providers, ui.
"""

from __future__ import annotations

from typing import Optional

from src.types import Board, Color, GameState, Move, Piece, Position
from src.service import game as game_service, state as state_service
from src.utils.move_parser import parse_move_input, format_position


def print_board(board: Board) -> None:
    """Print the board to stdout with coordinates."""
    # Print column headers
    print("   a b c d e f g h")
    print("  -----------------")
    
    for row_idx, row in enumerate(board):
        # Print row number on left
        print(f"{8 - row_idx}|", end="")
        for piece in row:
            if piece is None:
                print(" .", end="")
            elif piece.color == Color.RED:
                print(" R", end="")
            else:
                print(" B", end="")
        print(f"| {8 - row_idx}")
    
    print("  -----------------")
    print("   a b c d e f g h")
    print()


def print_game_state(game_state: GameState) -> None:
    """Print the current game state."""
    print_board(game_state.board)
    turn_str = "RED" if game_state.current_turn == Color.RED else "BLACK"
    print(f"Turn: {turn_str}")
    print(f"Red pieces: {game_state.red_pieces}")
    print(f"Black pieces: {game_state.black_pieces}")
    print()


def get_valid_moves_for_turn(game_state: GameState) -> list[tuple[Position, Move]]:
    """Get all valid moves for the current player."""
    return game_service.get_all_moves(game_state.board, game_state.current_turn)


def prompt_for_move(game_state: GameState) -> Optional[Move]:
    """
    Prompt the current player for a move.
    
    Returns the move or None if the player wants to quit.
    """
    while True:
        print_game_state(game_state)
        turn_str = "RED" if game_state.current_turn == Color.RED else "BLACK"
        user_input = input(f"{turn_str}'s move (e.g., 'a3 b4', 'q' to quit): ").strip()
        
        if user_input.lower() == 'q':
            return None
        
        parsed = parse_move_input(user_input)
        if parsed is None:
            print("Invalid format. Use 'a3 b4' format.")
            continue
        
        source = parsed.source
        dest = parsed.destination
        move = Move(from_pos=source, to_pos=dest)
        
        # Validate the move
        valid_moves = get_valid_moves_for_turn(game_state)
        valid_positions = [(pos, m) for pos, m in valid_moves]
        
        # Find if this move is valid
        found = False
        for pos, m in valid_positions:
            if m.from_pos == source and m.to_pos == dest:
                found = True
                break
        
        if not found:
            print("Invalid move. Try again.")
            continue
        
        return move


def play_game() -> None:
    """Run a simple CLI game loop."""
    game_state = state_service.initialize_game()
    
    while True:
        move = prompt_for_move(game_state)
        if move is None:
            print("Game quit.")
            break
        
        game_state, captured = state_service.make_move(game_state, move)
        
        if captured:
            print(f"Piece captured at {format_position(captured.position)}!")
        
        winner = state_service.check_win(game_state)
        if winner:
            print_game_state(game_state)
            winner_str = "RED" if winner == Color.RED else "BLACK"
            print(f"{winner_str} wins!")
            break
