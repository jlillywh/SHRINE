"""Store mass balance and bounds (migrated from src/water_manage/test_store.py)."""

from __future__ import annotations

import pytest

from water_manage.store import Store


class TestStoreOutflows:
    def test_reduced_outflow_when_emptying(self, bounded_store: Store) -> None:
        bounded_store.inflow = 0.43
        bounded_store.request = 15.0
        bounded_store.update()
        assert bounded_store.outflow < bounded_store.request

    def test_name(self) -> None:
        s = Store()
        s.name = "Big Pond"
        assert s.name == "Big Pond"

    def test_upper_bound_at_capacity(self, bounded_store: Store) -> None:
        bounded_store.inflow = 7.43
        bounded_store.outflow = 0.03
        bounded_store.update()
        assert bounded_store.quantity == pytest.approx(bounded_store.capacity, abs=1e-4)

    def test_lower_bound_at_zero(self, bounded_store: Store) -> None:
        bounded_store.inflow = 0.43
        bounded_store.request = 10.438
        bounded_store.update()
        assert bounded_store.quantity == pytest.approx(0.0, abs=1e-4)

    def test_setting_quantity_respects_bounds(self, bounded_store: Store) -> None:
        bounded_store.quantity = 999.99
        assert bounded_store.quantity == bounded_store.capacity
        bounded_store.quantity = 1.0
        assert bounded_store.quantity == pytest.approx(1.0, abs=1e-4)
        bounded_store.quantity = 13.8685
        assert bounded_store.quantity == pytest.approx(13.8685, abs=1e-4)

    def test_overflow_accumulates(self, bounded_store: Store) -> None:
        bounded_store.inflow = 0.6295
        cumulative_overflow = 0.0
        for _ in range(10):
            bounded_store.update()
            cumulative_overflow += bounded_store.overflow
        assert cumulative_overflow == pytest.approx(1.295, abs=1e-4)

    def test_quantity_initial(self) -> None:
        assert Store(32.54).quantity == 32.54

    def test_quantity_setter(self) -> None:
        s = Store()
        s.quantity = 132.54
        assert s.quantity == 132.54

    def test_outflow_update(self, bounded_store: Store) -> None:
        bounded_store.inflow = 0.13
        bounded_store.request = 1.43
        bounded_store.update()
        assert bounded_store.quantity == pytest.approx(10.0 + 0.13 - 1.43, abs=1e-4)
