"""Runtime layer - application entry point and orchestration.

Contains the main game loop and coordinates between layers.
May import from: types, config, repo, service, providers, runtime.
"""

from __future__ import annotations

from src.ui.cli import play_game


def main() -> int:
    """Run the checkers game."""
    play_game()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
