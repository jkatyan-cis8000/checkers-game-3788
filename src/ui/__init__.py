"""UI layer - user interface.

Contains all user-facing interfaces (CLI, GUI, web).
May import from: types, config, service, runtime, providers, ui.
"""

from __future__ import annotations

from .cli import print_board, print_game_state, prompt_for_move, play_game

__all__ = ["print_board", "print_game_state", "prompt_for_move", "play_game"]
