"""Runtime layer - application entry point and orchestration.

Contains the main game loop and coordinates between layers.
May import from: types, config, repo, service, providers, runtime.
"""

from __future__ import annotations

from .app import main

__all__ = ["main"]
