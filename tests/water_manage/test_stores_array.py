"""StoreArray batch updates (migrated from src/water_manage/test_stores_array.py)."""

from __future__ import annotations

import pytest

from water_manage.store_array import StoreArray


class TestStoreArray:
    @pytest.fixture
    def store_array(self) -> StoreArray:
        sa = StoreArray(4)
        sa.update([2.5, 7.8, 23.65, 5.23], [11.0, 0.0, 2.2, 100.0])
        return sa

    def test_total_quantity(self, store_array: StoreArray) -> None:
        assert store_array.total_quantity() == 29.25

    def test_total_overflow(self, store_array: StoreArray) -> None:
        assert store_array.total_overflow() == 0.0

    def test_total_outflow(self, store_array: StoreArray) -> None:
        assert store_array.total_outflow() == pytest.approx(9.93)
