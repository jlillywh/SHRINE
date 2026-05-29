"""Nested junction routing (migrated from src/hydrology/test_junction.py; API drift fixed)."""

from __future__ import annotations

import pytest

from hydrology.catchment import Catchment
from hydrology.watershed import Watershed


class TestWatershedJunctionRouting:
    """Two catchments on nested junctions (J5 → J1 → sink) combine at the outlet."""

    def test_discharge_equals_sum_of_catchments(self, nested_junction_watershed: Watershed) -> None:
        precip, et = 500.0, 0.0
        single = Catchment().outflow(precip, et)
        expected = single * 2
        assert nested_junction_watershed.discharge(precip, et) == pytest.approx(expected)

    def test_repeated_timesteps_stable(self, nested_junction_watershed: Watershed) -> None:
        precip, et = 500.0, 0.0
        first = nested_junction_watershed.discharge(precip, et)
        for _ in range(9):
            assert nested_junction_watershed.discharge(precip, et) == pytest.approx(first)
