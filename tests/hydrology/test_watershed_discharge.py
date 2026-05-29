"""Watershed discharge and GML load (migrated from src/hydrology/test_watershed.py)."""

from __future__ import annotations

from pathlib import Path

import pytest

from hydrology.catchment import Catchment
from hydrology.watershed import Watershed


class TestWatershedDischarge:
    def test_discharge_sums_two_catchments(self, two_catchment_watershed: Watershed) -> None:
        precip, et = 10.0, 1.0
        expected = Catchment().outflow(precip, et) * 2
        assert two_catchment_watershed.discharge(precip, et) == pytest.approx(expected, abs=1e-3)

    def test_load_gml_four_catchments(self, watershed_gml: Path) -> None:
        precip, et = 10.0, 1.0
        expected = Catchment().outflow(precip, et) * 4

        ws = Watershed()
        ws.load_from_file(str(watershed_gml))
        assert ws.discharge(precip, et) == pytest.approx(expected, abs=1e-3)
