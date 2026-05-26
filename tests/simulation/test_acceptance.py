"""Acceptance tests mapped to docs/simulation-framework-requirements.md (AT-*)."""

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
    WatershedElement,
)
from hydrology.catchment import Catchment
from hydrology.watershed import Watershed
from tests.conftest import SimpleStore
from aegis.simulation.adapters import ReservoirElement


class _CounterElement:
    element_type = "counter"

    def __init__(self) -> None:
        self.n = 0

    def initialize(self, run_context) -> None:
        self.n = 0

    def update(self, timestep_context) -> None:
        self.n += 1

    def finalize(self, run_context) -> None:
        pass


# AT-01
def test_at01_clock_only_timestep_count() -> None:
    clock = Clock("1/1/2019", "1/10/2019")
    model = Model(clock=clock)
    model.register("noop", _CounterElement())
    RunController(model, raise_on_error=False).run()
    # After full run, clock has advanced to end and stopped
    assert clock.current_date == clock.end_date
    assert not clock.running


# AT-02
def test_at02_dummy_element_output_count() -> None:
    clock = Clock("1/1/2019", "1/5/2019")
    model = Model(clock=clock)
    counter = _CounterElement()
    model.register("c1", counter)
    RunController(model, raise_on_error=False).run()
    assert counter.n == 5  # 1/1 .. 1/5 inclusive while running


# AT-04 / AT-05 covered in test_adapters

# AT-06
def test_at06_duplicate_id_fails_validate() -> None:
    model = Model()
    model.register("x", _CounterElement())
    with pytest.raises(SimulationError) as exc_info:
        model.register("x", _CounterElement())
    assert exc_info.value.phase == SimulationPhase.VALIDATE


# AT-07
def test_at07_identical_runs_match() -> None:
    clock = Clock("1/1/2019", "1/5/2019")
    model = Model(clock=clock)
    model.register("c1", _CounterElement())
    r1 = RunController(model, raise_on_error=False).run().outputs
    r2 = RunController(model, raise_on_error=False).run().outputs
    pd.testing.assert_frame_equal(r1, r2)


# AT-09
def test_at09_mass_balance_violation_fail_fast() -> None:
    from aegis.simulation.balance import MassBalanceTerm

    class _Imbalanced:
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
    model.register("x", _Imbalanced())
    with pytest.raises(SimulationError) as exc_info:
        RunController(model).run()
    assert exc_info.value.phase == SimulationPhase.BALANCE


def _build_two_catchment_watershed() -> Watershed:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    return ws


# AT-10
def test_at10_two_watersheds_independent() -> None:
    clock = Clock("1/1/2019", "1/3/2019")
    model = Model(clock=clock)
    ws_a = _build_two_catchment_watershed()
    ws_b = _build_two_catchment_watershed()
    model.register_watershed("ws1", WatershedElement(ws_a, element_id="ws1"))
    model.register_watershed("ws2", WatershedElement(ws_b, element_id="ws2"))
    inputs = InputManager()
    inputs.bind("precipitation", ConstantInput(8.0))
    inputs.bind("evaporation", ConstantInput(0.5))
    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    expected = Catchment().outflow(8.0, 0.5) * 2
    assert result.outputs["ws1.outflow"].iloc[0] == pytest.approx(expected, rel=1e-5)
    assert result.outputs["ws2.outflow"].iloc[0] == pytest.approx(expected, rel=1e-5)
    assert ws_a is not ws_b
    assert ws_a.dg is not ws_b.dg
