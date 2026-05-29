"""Shared pytest fixtures for SHRINE simulation and domain tests (roadmap 2.10)."""

from __future__ import annotations

from pathlib import Path

import pytest

from hydrology.watershed import Watershed
from shrine.simulation import Clock, InputManager, Model
from shrine.simulation.adapters import ReservoirElement, WatershedElement
from tests.path_fixtures import NETWORK_GML, REPO_ROOT, WATERSHED_GML
from water_manage.allocator import Allocator
from water_manage.flow_network import Network
from water_manage.request import Request
from water_manage.reservoir import Reservoir
from water_manage.store import Store


class SimpleStore:
    """Minimal storage (no legacy validation imports)."""

    def __init__(self, quantity: float = 100.0, capacity: float = float("inf")) -> None:
        self._quantity = quantity
        self._capacity = capacity
        self.inflow = 0.0
        self.request = 0.0
        self.outflow = 0.0
        self.overflow = 0.0

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, amount: float) -> None:
        self._quantity = amount

    @property
    def capacity(self) -> float:
        return self._capacity

    @capacity.setter
    def capacity(self, value: float) -> None:
        self._capacity = value

    def update(self) -> None:
        self._quantity += self.inflow - self.request
        if self._quantity > self._capacity:
            self.overflow = self._quantity - self._capacity
            self._quantity = self._capacity
        else:
            self.overflow = 0.0
        if self._quantity < 0.0:
            self.outflow = self.request + self._quantity
            self._quantity = 0.0
        else:
            self.outflow = self.request


# --- Paths ---


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def watershed_gml() -> Path:
    return WATERSHED_GML


@pytest.fixture
def network_gml() -> Path:
    return NETWORK_GML


# --- Clocks (simulation + legacy domain) ---


@pytest.fixture
def short_clock() -> Clock:
    """Four-day simulation clock (1–5 Jan 2019)."""
    return Clock("1/1/2019", "1/5/2019")


@pytest.fixture
def week_clock() -> Clock:
    """One-week simulation clock (1–8 Jan 2019)."""
    return Clock("1/1/2019", "1/8/2019")


@pytest.fixture
def month_clock() -> Clock:
    """Ten-day simulation clock (common in scenario/golden tests)."""
    return Clock("1/1/2019", "1/10/2019")


@pytest.fixture
def legacy_clock():
    """Legacy domain clock for WGEN and other ``global_attributes`` modules."""
    from global_attributes.clock import Clock as LegacyClock

    return LegacyClock()


# --- Hydrology / watershed ---


@pytest.fixture
def two_catchment_watershed() -> Watershed:
    """Two catchments (C1, C2) → junction J1 → sink."""
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    return ws


@pytest.fixture
def nested_junction_watershed() -> Watershed:
    """Nested junctions: C1→J1, C2→J5→J1→sink."""
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.add_junction("J5", "J1")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J5")
    return ws


@pytest.fixture
def watershed_model(short_clock: Clock, two_catchment_watershed: Watershed) -> Model:
    model = Model(name="TestBasin", clock=short_clock)
    model.register_watershed(
        "ws1",
        WatershedElement(two_catchment_watershed, element_id="ws1"),
    )
    return model


# --- Water manage / storage ---


@pytest.fixture
def flow_network() -> Network:
    return Network()


@pytest.fixture
def bounded_store() -> Store:
    """Legacy :class:`~water_manage.store.Store` with quantity 10 and capacity 15."""
    store = Store(10.0)
    store.capacity = 15.0
    return store


@pytest.fixture
def reservoir() -> Reservoir:
    """Legacy reservoir at water level 9.9 m with spillway crest 10.9 m."""
    r = Reservoir()
    r.water_level = 9.9
    r.spillway_crest = 10.9
    return r


@pytest.fixture
def standard_allocator() -> Allocator:
    """Allocator with supply 60 and four prioritized requests."""
    return Allocator(
        60,
        [
            Request("pumping", 10, 2),
            Request("farm", 18, 2),
            Request("mine", 35, 3),
            Request("evaporation", 18, 1),
        ],
    )


# --- Simulation helpers ---


@pytest.fixture
def climate_inputs() -> InputManager:
    from shrine.simulation import ConstantInput

    inputs = InputManager()
    inputs.bind("precipitation", ConstantInput(10.0))
    inputs.bind("evaporation", ConstantInput(1.0))
    return inputs


@pytest.fixture
def simple_store() -> SimpleStore:
    return SimpleStore(50.0)


@pytest.fixture
def reservoir_model(short_clock: Clock, simple_store: SimpleStore) -> Model:
    model = Model(clock=short_clock)
    model.register("res1", ReservoirElement(simple_store, element_id="res1"))
    return model
