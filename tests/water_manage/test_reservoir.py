"""Reservoir stage–storage and spillway (migrated from src/water_manage/test_reservoir.py)."""

from __future__ import annotations

import numpy as np
import pytest

from water_manage.reservoir import Reservoir


class TestReservoir:
    def test_volume_equals_quantity(self, reservoir: Reservoir) -> None:
        assert reservoir.volume == reservoir.quantity

    def test_inflow_updates_volume(self, reservoir: Reservoir) -> None:
        reservoir.inflow = 10
        for _ in range(10):
            reservoir.update()
        assert reservoir.volume == pytest.approx(273.25, abs=0.01)

    def test_change_capacity_overflow(self, reservoir: Reservoir) -> None:
        updated_capacity = 25.0
        reservoir.capacity = updated_capacity
        assert reservoir.capacity == updated_capacity

    def test_excess_inflow_overflow(self, reservoir: Reservoir) -> None:
        reservoir.capacity = 25.0
        reservoir.requests[0].amount = np.random.random() + 2.0
        reservoir.update()
        reservoir.inflow = 5.0 + np.random.random()
        reservoir.update()
        assert reservoir.volume == reservoir.capacity

    def test_water_level_output(self, reservoir: Reservoir) -> None:
        assert reservoir.water_level == 9.9

    def test_update_level_sets_volume(self, reservoir: Reservoir) -> None:
        reservoir.water_level = 3.4
        assert reservoir.volume == pytest.approx(59.5, abs=0.01)

    def test_area_output(self, reservoir: Reservoir) -> None:
        reservoir.water_level = 12.52
        assert reservoir.area == pytest.approx(38.276, abs=0.01)

    def test_evaporation(self, reservoir: Reservoir) -> None:
        reservoir.evaporation = 0.0155
        reservoir.update()
        assert reservoir.volume == pytest.approx(172.71, abs=0.01)

    def test_calc_overflow_reduces_volume_above_crest(self) -> None:
        r = Reservoir(init_vol=400.0)
        r.spillway_crest = 5.0
        r.water_level = 12.0
        vol_before = r.volume
        r.calc_overflow()
        assert r.volume < vol_before
        assert r.outflow >= 0.0
