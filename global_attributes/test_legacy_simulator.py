"""Legacy Simulator removal (1.6)."""

from __future__ import annotations

import warnings

import pytest

from global_attributes.simulator import Simulator


def test_simulator_init_warns_and_raises() -> None:
    with pytest.warns(DeprecationWarning, match="RunController"):
        with pytest.raises(NotImplementedError, match="RunController"):
            Simulator()
