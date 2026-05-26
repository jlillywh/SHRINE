"""Tests for aegis.simulation.errors."""

from __future__ import annotations

import pandas as pd

from aegis.simulation import SimulationError, SimulationPhase


class TestSimulationError:
    def test_str_includes_phase_and_element(self) -> None:
        err = SimulationError(
            message="solver failed",
            phase=SimulationPhase.FLOW_SOLVE,
            element_id="ws1",
            step_index=3,
            timestamp=pd.Timestamp("2020-01-04"),
        )
        text = str(err)
        assert "solver failed" in text
        assert "flow_solve" in text
        assert "ws1" in text
        assert "step_index=3" in text

    def test_is_exception(self) -> None:
        err = SimulationError("x", SimulationPhase.VALIDATE)
        assert isinstance(err, Exception)

    def test_details_dict(self) -> None:
        err = SimulationError(
            "x",
            SimulationPhase.BALANCE,
            details={"terms": [("a", 1.0)]},
        )
        assert err.details["terms"] == [("a", 1.0)]
