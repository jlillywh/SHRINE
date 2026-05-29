"""Tests for shrine.simulation.model."""

from __future__ import annotations

import pytest

from shrine.simulation import Model, SimulationError, SimulationPhase
from shrine.simulation.adapters import ReservoirElement
from tests.conftest import SimpleStore


class _DummyElement:
    element_type = "dummy"

    def initialize(self, run_context) -> None:
        pass

    def update(self, timestep_context) -> None:
        pass

    def finalize(self, run_context) -> None:
        pass


class TestModel:
    def test_register_and_get(self) -> None:
        model = Model()
        el = _DummyElement()
        model.register("x", el)
        assert model.get("x") is el

    def test_duplicate_id_raises_validate_phase(self) -> None:
        model = Model()
        model.register("a", _DummyElement())
        with pytest.raises(SimulationError) as exc_info:
            model.register("a", _DummyElement())
        assert exc_info.value.phase == SimulationPhase.VALIDATE

    def test_get_unknown_raises(self) -> None:
        model = Model()
        with pytest.raises(SimulationError):
            model.get("missing")

    def test_validate_requires_elements_by_default(self) -> None:
        with pytest.raises(SimulationError):
            Model().validate()

    def test_validate_allows_empty_when_disabled(self) -> None:
        Model().validate(require_elements=False)

    def test_register_watershed_metadata(self) -> None:
        model = Model()
        model.register_watershed("ws1", _DummyElement())
        assert len(model.watersheds()) == 1
        assert model.watersheds()[0].metadata["kind"] == "watershed"

    def test_multiple_watersheds(self) -> None:
        model = Model()
        model.register_watershed("ws1", _DummyElement())
        model.register_watershed("ws2", _DummyElement())
        assert len(model.watersheds()) == 2

    def test_register_reservoir_element(self) -> None:
        model = Model()
        store = SimpleStore()
        model.register("r1", ReservoirElement(store, element_id="r1"))
        assert model.get("r1").element_type == "reservoir"

    def test_register_reservoir_helper(self) -> None:
        model = Model()
        store = SimpleStore()
        model.register_reservoir("r1", ReservoirElement(store, element_id="r1"))
        registered = model._elements["r1"]
        assert registered.metadata["kind"] == "reservoir"
