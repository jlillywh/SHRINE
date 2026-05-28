"""Tests for hydrology.protocols.RunoffModel (roadmap 2.1)."""

from __future__ import annotations

import pytest

from hydrology.awbm import Awbm
from hydrology.catchment import Rational
from hydrology.protocols import (
    AWBM_RUNOFF_UNIT,
    DEFAULT_RUNOFF_UNIT,
    LegacyRunoffAdapter,
    RunoffModel,
    as_runoff_model,
)


class TestRunoffModelProtocol:
    def test_rational_is_runoff_model(self) -> None:
        assert isinstance(Rational(), RunoffModel)

    def test_rational_compute_returns_quantity(self) -> None:
        q = Rational().compute(10.0, 1.0)
        expected = Rational().runoff(10.0, 1.0)
        assert q.to(DEFAULT_RUNOFF_UNIT).magnitude == pytest.approx(expected)

    def test_awbm_is_runoff_model(self) -> None:
        assert isinstance(Awbm(), RunoffModel)

    def test_awbm_compute_uses_metre_per_day(self) -> None:
        model = Awbm()
        q = model.compute(0.01, 0.002)
        expected = model.runoff(0.01, 0.002)
        assert q.to(AWBM_RUNOFF_UNIT).magnitude == pytest.approx(expected)

    def test_legacy_adapter_wraps_runoff_method(self) -> None:
        legacy = Rational()
        wrapped = LegacyRunoffAdapter(legacy)
        assert isinstance(wrapped, RunoffModel)
        assert wrapped.compute(10.0, 1.0).magnitude == legacy.runoff(10.0, 1.0)

    def test_as_runoff_model_passes_through(self) -> None:
        rational = Rational()
        assert as_runoff_model(rational) is rational

    def test_as_runoff_model_wraps_legacy(self) -> None:
        class _Legacy:
            def runoff(self, precip: float, et: float) -> float:
                return precip - et

        wrapped = as_runoff_model(_Legacy(), unit="mm/day")
        assert wrapped.compute(5.0, 1.0).magnitude == 4.0
