"""Legacy Simulator removal (1.6). Migrated from src/global_attributes/test_legacy_simulator.py."""

from __future__ import annotations

import pytest

from global_attributes.simulator import Simulator


def test_simulator_init_warns_and_raises() -> None:
    with pytest.warns(DeprecationWarning, match="RunController"):
        with pytest.raises(NotImplementedError, match="RunController"):
            Simulator()
