"""Providers layer - external service providers.

Contains adapters for external services (e.g., persistence, APIs).
May import from: types, config, utils, providers.
"""

from __future__ import annotations


def sample_provider() -> str:
    """Sample provider function."""
    return "providers"
