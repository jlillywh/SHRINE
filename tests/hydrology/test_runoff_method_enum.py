"""Tests for hydrology.enums.RunoffMethod (roadmap 2.3)."""

from __future__ import annotations

import warnings

import pytest

from hydrology.awbm import Awbm
from hydrology.catchment import Catchment, Rational
from hydrology.enums import RunoffMethod
from hydrology.protocols import RunoffModel


class TestRunoffMethodEnum:
    def test_members(self) -> None:
        assert RunoffMethod.SIMPLE.value == "simple"
        assert RunoffMethod.AWBM.value == "awbm"

    def test_from_any_case_insensitive(self) -> None:
        assert RunoffMethod.from_any("AWBM") is RunoffMethod.AWBM
        assert RunoffMethod.from_any(RunoffMethod.SIMPLE) is RunoffMethod.SIMPLE

    def test_build_simple(self) -> None:
        model = RunoffMethod.SIMPLE.build()
        assert isinstance(model, Rational)
        assert isinstance(model, RunoffModel)

    def test_build_awbm(self) -> None:
        model = RunoffMethod.AWBM.build()
        assert isinstance(model, Awbm)

    def test_catchment_accepts_enum_without_warning(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            c = Catchment(area=1000.0, runoff_method=RunoffMethod.SIMPLE)
        assert c.outflow(10.0, 1.0) == pytest.approx(5850.0)

    def test_catchment_enum_matches_rational_instance(self) -> None:
        from_enum = Catchment(area=1000.0, runoff_method=RunoffMethod.SIMPLE)
        from_model = Catchment(area=1000.0, runoff_method=Rational())
        assert from_enum.outflow(10.0, 1.0) == pytest.approx(from_model.outflow(10.0, 1.0))

    def test_invalid_enum_string_raises(self) -> None:
        with pytest.raises(ValueError):
            RunoffMethod.from_any("not_a_method")
