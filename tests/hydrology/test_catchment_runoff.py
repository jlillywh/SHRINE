"""Tests for Catchment + RunoffModel (roadmap 2.2)."""

from __future__ import annotations

import warnings

import pytest

from hydrology.awbm import Awbm
from hydrology.catchment import Catchment, Rational
from hydrology.enums import RunoffMethod
from hydrology.protocols import RunoffModel


class TestCatchmentRunoffModel:
    def test_accepts_runoff_model_without_warning(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            c = Catchment(area=1000.0, runoff_method=Rational())
        assert isinstance(c.runoff, RunoffModel)
        assert c.outflow(10.0, 1.0) == pytest.approx(5850.0)

    def test_enum_factory_no_warning(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            c = Catchment(area=1000.0, runoff_method=RunoffMethod.SIMPLE)
        assert c.outflow(10.0, 1.0) == pytest.approx(5850.0)

    def test_string_factory_deprecated(self) -> None:
        with pytest.warns(DeprecationWarning, match="string is deprecated"):
            c = Catchment(area=1000.0, runoff_method="simple")
        assert c.outflow(10.0, 1.0) == pytest.approx(5850.0)

    def test_string_awbm_case_insensitive(self) -> None:
        with pytest.warns(DeprecationWarning):
            c_lower = Catchment(area=12600000.0, runoff_method="awbm")
        with pytest.warns(DeprecationWarning):
            c_upper = Catchment(area=12600000.0, runoff_method="AWBM")
        assert c_lower.outflow(0.00654, 0.00025) == pytest.approx(
            c_upper.outflow(0.00654, 0.00025),
        )

    def test_string_simple_matches_rational_instance(self) -> None:
        with pytest.warns(DeprecationWarning):
            from_string = Catchment(area=1000.0, runoff_method="simple")
        from_model = Catchment(area=1000.0, runoff_method=Rational())
        assert from_string.outflow(10.0, 1.0) == pytest.approx(from_model.outflow(10.0, 1.0))

    def test_unknown_string_raises(self) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match="RunoffMethod"):
                Catchment(runoff_method="invalid")

    def test_runoff_method_exposes_loss_for_adapter(self) -> None:
        c = Catchment(area=1000.0, runoff_method=Rational())
        assert c.runoff_method.loss == pytest.approx(0.35)

    def test_awbm_runoff_model_instance(self) -> None:
        c = Catchment(area=1000.0, runoff_method=Awbm())
        assert isinstance(c.runoff, RunoffModel)
        assert c.outflow(0.01, 0.002) >= 0.0
