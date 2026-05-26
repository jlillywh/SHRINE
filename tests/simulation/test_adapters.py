"""Tests for watershed and reservoir simulation adapters."""

from __future__ import annotations

import pytest

from aegis.simulation import (
    Clock,
    ConstantInput,
    InputManager,
    Model,
    NetworkXFlowSolver,
    ReservoirElement,
    RunController,
    SimulationError,
    SimulationPhase,
    WatershedElement,
)
from aegis.simulation.balance import MassBalanceCheck, MassBalanceTerm
from hydrology.catchment import Catchment


class TestWatershedElement:
    def test_run_records_outflow_and_balance(
        self, watershed_model: Model, climate_inputs: InputManager
    ) -> None:
        result = RunController(watershed_model, input_manager=climate_inputs).run()
        assert result.success
        expected = Catchment().outflow(10.0, 1.0) * 2
        assert result.outputs["ws1.outflow"].iloc[0] == pytest.approx(expected, rel=1e-5)
        assert (result.outputs["ws1.total_supply"] == result.outputs["ws1.outflow"]).all()

    def test_balance_terms_close(self, two_catchment_watershed) -> None:
        element = WatershedElement(two_catchment_watershed, element_id="ws1")
        from aegis.simulation.context import RunContext, TimestepContext

        clock = Clock()
        run = RunContext(model_id="t", clock=clock)
        element._last_total_supply = 100.0
        element._last_outflow = 100.0
        terms = element.balance_terms(
            TimestepContext(run=run, step_index=0, current_time=clock.current_date, dt=clock.time_step)
        )
        report = MassBalanceCheck().verify(terms)
        assert report.passed

    def test_missing_evaporation_input(self, watershed_model: Model) -> None:
        inputs = InputManager()
        inputs.bind("precipitation", ConstantInput(1.0))
        with pytest.raises(SimulationError) as exc_info:
            RunController(watershed_model, input_manager=inputs).run()
        assert exc_info.value.phase == SimulationPhase.INPUT
        assert exc_info.value.element_id == "ws1"

    def test_solver_matches_legacy_discharge(self, two_catchment_watershed) -> None:
        precip, et = 8.0, 0.5
        expected = two_catchment_watershed.discharge(precip, et)
        for name, c in two_catchment_watershed.catchments.items():
            two_catchment_watershed.update_capacity(name, c.outflow(precip, et))
        result = NetworkXFlowSolver().solve(
            two_catchment_watershed.dg,
            two_catchment_watershed.source,
            two_catchment_watershed.sink,
        )
        assert result.total_flow == pytest.approx(expected, rel=1e-5)


class TestReservoirElement:
    def test_storage_updates(self, reservoir_model: Model) -> None:
        inputs = InputManager()
        inputs.bind("inflow", ConstantInput(12.0))
        inputs.bind("release", ConstantInput(5.0))
        result = RunController(reservoir_model, input_manager=inputs).run()
        assert result.outputs["res1.storage"].iloc[0] == pytest.approx(57.0, rel=1e-6)

    def test_balance_terms_close(self) -> None:
        from tests.conftest import SimpleStore

        store = SimpleStore(100.0)
        element = ReservoirElement(store, element_id="r1")
        store.inflow = 10.0
        store.request = 3.0
        element._volume_before = 100.0
        store.update()
        element._last_inflow = 10.0
        element._last_outflow = store.outflow
        element._last_overflow = store.overflow

        from aegis.simulation.context import RunContext, TimestepContext
        from aegis.simulation import Clock

        clock = Clock()
        run = RunContext(model_id="t", clock=clock)
        terms = element.balance_terms(
            TimestepContext(run=run, step_index=0, current_time=clock.current_date, dt=clock.time_step)
        )
        assert MassBalanceCheck().verify(terms).passed

    def test_overflow_accounted_in_balance(self) -> None:
        from tests.conftest import SimpleStore

        store = SimpleStore(quantity=95.0, capacity=100.0)
        element = ReservoirElement(store, element_id="r1")
        element._volume_before = 95.0
        store.inflow = 20.0
        store.request = 0.0
        store.update()
        element._last_inflow = 20.0
        element._last_outflow = store.outflow
        element._last_overflow = store.overflow

        from aegis.simulation.context import RunContext, TimestepContext
        from aegis.simulation import Clock

        clock = Clock()
        run = RunContext(model_id="t", clock=clock)
        terms = element.balance_terms(
            TimestepContext(run=run, step_index=0, current_time=clock.current_date, dt=clock.time_step)
        )
        assert store.overflow > 0
        assert MassBalanceCheck().verify(terms).passed
