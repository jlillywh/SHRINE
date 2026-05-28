"""Tests for shrine.simulation.run_controller."""

from __future__ import annotations

import pandas as pd
import pytest

from shrine.simulation import (
    Clock,
    ClimateRecorderElement,
    InputManager,
    Model,
    MonthlyLookupInput,
    RunController,
    SimulationError,
    SimulationPhase,
)
from shrine.simulation.balance import MassBalanceTerm
from shrine.simulation.context import RunContext, TimestepContext
from examples.climate_loop import (
    EVAPORATION_BY_MONTH,
    PRECIPITATION_BY_MONTH,
    build_climate_model,
)


class _CounterElement:
    element_type = "counter"

    def __init__(self) -> None:
        self.total = 0

    def initialize(self, run_context: RunContext) -> None:
        self.total = 0

    def update(self, timestep_context: TimestepContext) -> None:
        self.total += 1

    def finalize(self, run_context: RunContext) -> None:
        pass


class _FailingElement:
    element_type = "failing"

    def initialize(self, run_context: RunContext) -> None:
        pass

    def update(self, timestep_context: TimestepContext) -> None:
        raise RuntimeError("boom")

    def finalize(self, run_context: RunContext) -> None:
        pass


class _BadBalanceElement:
    element_type = "bad_balance"

    def initialize(self, run_context: RunContext) -> None:
        pass

    def update(self, timestep_context: TimestepContext) -> None:
        pass

    def finalize(self, run_context: RunContext) -> None:
        pass

    def balance_terms(self, timestep_context: TimestepContext) -> list[MassBalanceTerm]:
        return [
            MassBalanceTerm("supply", 100.0),
            MassBalanceTerm("outflow", -10.0),
        ]


class TestRunController:
    def test_executes_registered_elements(self) -> None:
        clock = Clock("1/1/2019", "1/5/2019")
        model = Model(clock=clock)
        counter = _CounterElement()
        model.register("c1", counter)
        result = RunController(model, raise_on_error=False).run()
        assert result.success
        assert counter.total > 0

    def test_metadata_in_result(self) -> None:
        clock = Clock("1/1/2019", "1/3/2019")
        model = Model(clock=clock)
        model.register("c1", _CounterElement())
        result = RunController(
            model,
            scenario_name="test_scenario",
            seed=42,
            raise_on_error=False,
        ).run()
        assert result.metadata["scenario_name"] == "test_scenario"
        assert result.metadata["seed"] == 42
        assert result.metadata["reproducible"] is True
        assert "run_id" in result.metadata
        assert result.metadata["status"] == "success"

    def test_fail_fast_raises(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("bad", _FailingElement())
        with pytest.raises(SimulationError) as exc_info:
            RunController(model, raise_on_error=True).run()
        assert exc_info.value.phase == SimulationPhase.UPDATE
        assert exc_info.value.element_id == "bad"

    def test_raise_on_error_false_returns_failed_result(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("bad", _FailingElement())
        result = RunController(model, raise_on_error=False).run()
        assert not result.success
        assert result.error is not None

    def test_mass_balance_violation_raises(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/2/2019"))
        model.register("bb", _BadBalanceElement())
        with pytest.raises(SimulationError) as exc_info:
            RunController(model, verify_mass_balance=True).run()
        assert exc_info.value.phase == SimulationPhase.BALANCE

    def test_mass_balance_can_be_disabled(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/2/2019"))
        model.register("bb", _BadBalanceElement())
        result = RunController(
            model,
            verify_mass_balance=False,
            raise_on_error=False,
        ).run()
        assert result.success

    def test_deterministic_rerun(self) -> None:
        clock = Clock("1/1/2019", "1/5/2019")
        model = Model(clock=clock)
        model.register("c1", _CounterElement())
        r1 = RunController(model, raise_on_error=False).run()
        r2 = RunController(model, raise_on_error=False).run()
        pd.testing.assert_frame_equal(r1.outputs, r2.outputs)

    def test_climate_recorder_integration(self) -> None:
        clock = Clock("1/1/2019", "1/4/2019")
        model = Model(clock=clock)
        model.register("climate", ClimateRecorderElement())
        inputs = InputManager()
        inputs.bind("evaporation", MonthlyLookupInput(EVAPORATION_BY_MONTH))
        inputs.bind("precipitation", MonthlyLookupInput(PRECIPITATION_BY_MONTH))
        result = RunController(model, input_manager=inputs, raise_on_error=False).run()
        assert result.success
        assert result.outputs.loc[pd.Timestamp("2019-01-01"), "evaporation"] == EVAPORATION_BY_MONTH["January"]

    def test_step_and_finalize(self) -> None:
        clock = Clock("1/1/2019", "1/4/2019")
        model = Model(clock=clock)
        counter = _CounterElement()
        model.register("c1", counter)
        controller = RunController(model, raise_on_error=False)
        step = controller.step()
        assert step is not None
        assert counter.total == 1
        controller.finalize()

    def test_climate_loop_example(self) -> None:
        _, controller = build_climate_model(start="1/1/2019", end="1/8/2019")
        result = controller.run()
        jan = result.outputs[result.outputs.index.month == 1]
        assert (jan["evaporation"] == EVAPORATION_BY_MONTH["January"]).all()


class _BareOutputElement:
    element_type = "bare_output"

    def initialize(self, run_context: RunContext) -> None:
        pass

    def update(self, timestep_context: TimestepContext) -> None:
        recorder = timestep_context.recorder
        if recorder is not None:
            recorder.record("out", 1.0)

    def finalize(self, run_context: RunContext) -> None:
        pass


class TestStrictUnits:
    def test_run_controller_strict_units_fails_on_bare_record(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/2/2019"))
        model.register("bare", _BareOutputElement())
        controller = RunController(model, strict_units=True, raise_on_error=False)
        result = controller.run()
        assert not result.success
        assert result.error is not None
        assert result.error.phase == SimulationPhase.RECORD

    def test_climate_recorder_passes_strict_units(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("climate", ClimateRecorderElement())
        inputs = InputManager()
        inputs.bind("evaporation", MonthlyLookupInput(EVAPORATION_BY_MONTH))
        inputs.bind("precipitation", MonthlyLookupInput(PRECIPITATION_BY_MONTH))
        controller = RunController(
            model,
            input_manager=inputs,
            strict_units=True,
            raise_on_error=False,
        )
        result = controller.run()
        assert result.success
        assert result.outputs["evaporation"].notna().all()
