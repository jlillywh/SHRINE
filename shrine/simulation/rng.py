"""Seeded random number generation for reproducible runs (INP-04, NFR-02)."""

from __future__ import annotations

import numpy as np


def make_rng(seed: int | None) -> np.random.Generator:
    """Return a NumPy Generator; ``seed=None`` is non-reproducible across processes."""
    if seed is None:
        return np.random.default_rng()
    return np.random.default_rng(seed)
