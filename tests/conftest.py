"""Shared pytest fixtures for Aegis simulation tests."""

from __future__ import annotations

import pytest

from aegis.simulation import Clock, InputManager, Model
from aegis.simulation.adapters import ReservoirElement, WatershedElement
from hydrology.watershed import Watershed


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


@pytest.fixture
def short_clock() -> Clock:
    return Clock("1/1/2019", "1/5/2019")


@pytest.fixture
def week_clock() -> Clock:
    return Clock("1/1/2019", "1/8/2019")


@pytest.fixture
def two_catchment_watershed() -> Watershed:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    return ws


@pytest.fixture
def watershed_model(short_clock: Clock, two_catchment_watershed: Watershed) -> Model:
    model = Model(name="TestBasin", clock=short_clock)
    model.register_watershed(
        "ws1",
        WatershedElement(two_catchment_watershed, element_id="ws1"),
    )
    return model


@pytest.fixture
def climate_inputs() -> InputManager:
    from aegis.simulation import ConstantInput

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
