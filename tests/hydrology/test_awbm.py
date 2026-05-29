"""AWBM bucket model verification (migrated from src/hydrology/test_awbm.py)."""

from __future__ import annotations

import pytest

from hydrology.awbm import Awbm


@pytest.fixture
def primed_awbm() -> Awbm:
    awbm = Awbm()
    awbm.buckets.set_quantities([0.0042, 0.05, 0.0429])
    awbm.base.quantity = 0.01
    awbm.surface.quantity = 0.01
    for _ in range(10):
        awbm.runoff(0.01, 0.001)
    return awbm


class TestAwbmBucketCase:
    """Compare results to GoldSim model: AWBM Verification.gsm."""

    def test_update_comp_capacity(self, primed_awbm: Awbm) -> None:
        new_buckets = [0.05743, 0.14333, 0.29849]
        primed_awbm.set_comp_capacity(new_buckets)
        for i, cap in enumerate(new_buckets):
            assert primed_awbm.buckets.stores[i].capacity == pytest.approx(
                cap * primed_awbm.partial_area_fraction[i]
            )

    def test_buckets_quantity(self, primed_awbm: Awbm) -> None:
        assert primed_awbm.buckets.total_quantity() == pytest.approx(0.152, abs=1e-3)

    def test_buckets_overflow(self, primed_awbm: Awbm) -> None:
        assert primed_awbm.buckets.total_overflow() == pytest.approx(0.0051, abs=1e-3)

    def test_surface_quantity(self, primed_awbm: Awbm) -> None:
        assert primed_awbm.surface.quantity == pytest.approx(0.0106, abs=1e-3)

    def test_base_quantity(self, primed_awbm: Awbm) -> None:
        assert primed_awbm.base.quantity == pytest.approx(0.0048565, abs=1e-4)


class TestAwbmSurfaceStore:
    def test_store_outflow(self) -> None:
        awbm = Awbm()
        awbm.buckets.set_quantities([0.00502, 0.140, 0.063])
        precip = 0.00654
        et = 0.00025
        outflow = 0.0
        for _ in range(10):
            outflow += awbm.runoff(precip, et)
        assert outflow == pytest.approx(0.024936, abs=1e-3)
