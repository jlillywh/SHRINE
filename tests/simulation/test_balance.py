"""Tests for shrine.simulation.balance."""

from __future__ import annotations

import pytest

from shrine.simulation.balance import MassBalanceCheck, MassBalanceTerm
from shrine.simulation.errors import SimulationError, SimulationPhase


class TestMassBalanceCheck:
    def test_balanced_terms_pass(self) -> None:
        check = MassBalanceCheck(tolerance=1e-6)
        report = check.verify(
            [
                MassBalanceTerm("inflow", 100.0),
                MassBalanceTerm("outflow", -100.0),
            ]
        )
        assert report.passed
        assert report.residual == pytest.approx(0.0)

    def test_imbalance_fails(self) -> None:
        check = MassBalanceCheck(tolerance=1e-6)
        report = check.verify(
            [
                MassBalanceTerm("inflow", 100.0),
                MassBalanceTerm("outflow", -90.0),
            ]
        )
        assert not report.passed
        assert report.residual == pytest.approx(10.0)

    def test_verify_or_raise(self) -> None:
        check = MassBalanceCheck()
        with pytest.raises(SimulationError) as exc_info:
            check.verify_or_raise(
                [MassBalanceTerm("a", 1.0)],
                step_index=2,
            )
        assert exc_info.value.phase == SimulationPhase.BALANCE
        assert exc_info.value.step_index == 2
