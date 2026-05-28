"""Tests for water_manage.protocols.StorageElement (roadmap 2.4)."""

from __future__ import annotations

import pytest

from shrine.simulation.adapters.reservoir import ReservoirElement, StorageLike
from tests.conftest import SimpleStore
from water_manage.protocols import StorageElement, as_storage_element
from water_manage.store import Store


class TestStorageElementProtocol:
    def test_store_satisfies_protocol(self) -> None:
        assert isinstance(Store(100.0), StorageElement)

    def test_reservoir_satisfies_protocol(self) -> None:
        from water_manage.reservoir import Reservoir

        assert isinstance(Reservoir(init_vol=50.0), StorageElement)

    def test_simple_store_satisfies_protocol(self) -> None:
        assert isinstance(SimpleStore(25.0, capacity=100.0), StorageElement)

    def test_storage_like_alias_is_storage_element(self) -> None:
        assert StorageLike is StorageElement

    def test_as_storage_element_accepts_store(self) -> None:
        store = Store(10.0)
        assert as_storage_element(store) is store

    def test_as_storage_element_rejects_invalid(self) -> None:
        with pytest.raises(TypeError, match="StorageElement"):
            as_storage_element(object())

    def test_reservoir_element_accepts_store(self) -> None:
        element = ReservoirElement(Store(100.0), element_id="r1")
        assert isinstance(element.store, StorageElement)

    def test_timestep_contract_on_store(self) -> None:
        store = Store(100.0)
        store.inflow = 12.0
        store.request = 5.0
        store.update()
        assert store.quantity == pytest.approx(107.0)
        assert store.outflow == pytest.approx(5.0)
        assert store.overflow == pytest.approx(0.0)
