"""AWBM catchment GoldSim verification (migrated from src/hydrology/test_catchment.py)."""

from __future__ import annotations

import warnings

import pytest

from hydrology.catchment import Catchment
from hydrology.enums import RunoffMethod


class TestCatchmentAwbmVerification:
    """Compare results to Catchment Verification.gsm."""

    @pytest.fixture
    def catchment(self) -> Catchment:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            return Catchment(12600000.0, runoff_method=RunoffMethod.AWBM)

    def test_outflow_matches_goldsim(self, catchment: Catchment) -> None:
        precip = 0.00654
        et = 0.00025
        q = 0.0
        for _ in range(11):
            q = catchment.outflow(precip, et)
        assert q == pytest.approx(8321.71, abs=1.0)
