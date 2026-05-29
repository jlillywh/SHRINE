"""Deprecation helpers for colocated tests still under ``src/`` (roadmap 2.11)."""

from __future__ import annotations

import warnings


def deprecate_colocated_module(*, path: str, migrated_to: str | None = None) -> None:
    """Warn that a colocated test module is deprecated in favor of ``tests/``."""
    message = (
        f"{path} is deprecated colocated test code. "
        "Run ``pytest tests/`` instead (modernization roadmap 2.11)."
    )
    if migrated_to:
        message += f" Migrated coverage: {migrated_to}."
    warnings.warn(message, DeprecationWarning, stacklevel=2)
