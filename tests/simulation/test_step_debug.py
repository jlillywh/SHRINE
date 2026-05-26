"""Tests for RunController step() debugging API (RUN-04)."""

from __future__ import annotations

import pandas as pd
import pytest

from aegis.simulation import (
    Clock,
    ConstantInput,
    InputManager,
    Model,
    RunController,
    SimulationError,
    SimulationPhase,
    StepResult,
    WatershedElement,
)
from aegis.simulation.balance import MassBalanceTerm
from hydrology.watershed import Watershed


class _CounterElement:
    element_type = "counter"

    def __init__(self) -> None:
        self.total = 0

    def initialize(self, run_context) -> None:
        self.total = 0

    def update(self, timestep_context) -> None:
        self.total += 1

    def finalize(self, run_context) -> None:
        pass


class TestStepDebugging:
    def test_step_returns_step_result(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/4/2019"))
        model.register("c1", _CounterElement())
        controller = RunController(model, raise_on_error=False)
        result = controller.step()
        assert isinstance(result, StepResult)
        assert result.step_index == 0
        assert result.current_time == pd.Timestamp("2019-01-01")
        assert result.done is False
        assert controller.is_running

    def test_step_many_then_complete(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/5/2019"))
        model.register("c1", _CounterElement())

        controller = RunController(model, raise_on_error=False)
        controller.reset()
        results = controller.step_many(10)
        assert len(results) == 5
        assert results[-1].done is True
        assert controller.step() is None
        complete = controller.complete()
        assert complete.metadata["debug_mode"] is True
        assert complete.metadata["steps_completed"] == 5
        assert controller.steps_completed == 0  # reset after complete()

    def test_reset_allows_second_session(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        counter = _CounterElement()
        model.register("c1", counter)
        controller = RunController(model, raise_on_error=False)
        controller.step_many(5)
        controller.complete()
        first_total = counter.total

        controller.reset()
        counter.total = 0
        controller.step_many(5)
        controller.finalize()
        assert counter.total == first_total

    def test_watershed_step_includes_balance(self) -> None:
        ws = Watershed()
        ws.add_junction("J1", "sink")
        ws.link_catchment("C1", "J1")
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
        inputs = InputManager()
        inputs.bind("precipitation", ConstantInput(10.0))
        inputs.bind("evaporation", ConstantInput(1.0))
        controller = RunController(model, input_manager=inputs, raise_on_error=False)
        step = controller.step()
        assert step is not None
        assert step.balance is not None
        assert step.balance.passed
        assert step.passed

    def test_balance_failure_on_step(self) -> None:
        class _Bad:
            element_type = "x"

            def initialize(self, run_context) -> None:
                pass

            def update(self, timestep_context) -> None:
                pass

            def finalize(self, run_context) -> None:
                pass

            def balance_terms(self, timestep_context):
                return [MassBalanceTerm("a", 1.0)]

        model = Model(clock=Clock("1/1/2019", "1/2/2019"))
        model.register("x", _Bad())
        with pytest.raises(SimulationError) as exc_info:
            RunController(model).step()
        assert exc_info.value.phase == SimulationPhase.BALANCE

    def test_begin_does_not_advance(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/4/2019"))
        counter = _CounterElement()
        model.register("c1", counter)
        controller = RunController(model, raise_on_error=False)
        controller.begin()
        assert controller.is_initialized
        assert controller.steps_completed == 0
        assert counter.total == 0

    def test_last_step_property(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("c1", _CounterElement())
        controller = RunController(model, raise_on_error=False)
        assert controller.last_step is None
        first = controller.step()
        assert controller.last_step is first
