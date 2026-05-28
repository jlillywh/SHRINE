"""Fuzz-light mass balance checks for SimpleStore + constant inflows (roadmap 1.16)."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

import pandas as pd
import pytest

from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController
from shrine.simulation.adapters import ReservoirElement
from shrine.simulation.balance import MassBalanceCheck
from shrine.simulation.context import RunContext, TimestepContext
from tests.conftest import SimpleStore

FUZZ_SEED = 20240528
FUZZ_TERM_STEPS = 200
FUZZ_RUN_STEPS = 40


@dataclass(frozen=True)
class ReservoirCase:
    quantity: float
    capacity: float
    inflow: float
    release: float
    steps: int
    use_release_input: bool

    def label(self) -> str:
        cap = "inf" if math.isinf(self.capacity) else f"{self.capacity:.2f}"
        rel = "input" if self.use_release_input else "default"
        return (
            f"q={self.quantity:.2f},cap={cap},in={self.inflow:.2f},"
            f"out={self.release:.2f},n={self.steps},rel={rel}"
        )


def _clock_for_steps(steps: int) -> Clock:
    start = pd.Timestamp("1/1/2019")
    end = start + pd.Timedelta(days=max(steps - 1, 0))
    return Clock(start, end)


def _generate_cases(count: int, *, seed: int = FUZZ_SEED) -> list[ReservoirCase]:
    rng = random.Random(seed)
    cases: list[ReservoirCase] = []
    for _ in range(count):
        capacity = math.inf if rng.random() < 0.25 else rng.uniform(10.0, 500.0)
        cases.append(
            ReservoirCase(
                quantity=rng.uniform(0.0, 250.0),
                capacity=capacity,
                inflow=rng.uniform(0.0, 50.0),
                release=rng.uniform(0.0, 50.0),
                steps=rng.randint(1, 20),
                use_release_input=rng.random() < 0.7,
            )
        )
    return cases


def _assert_balance_terms_each_step(case: ReservoirCase) -> None:
    store = SimpleStore(case.quantity, case.capacity)
    if case.use_release_input:
        element = ReservoirElement(store, element_id="res", default_release=0.0)
    else:
        element = ReservoirElement(
            store,
            element_id="res",
            release_key=None,
            default_release=case.release,
        )
    check = MassBalanceCheck(tolerance=1e-9)
    clock = _clock_for_steps(case.steps)
    run = RunContext(model_id="fuzz", clock=clock)
    inputs: dict[str, Any] = {"inflow": case.inflow}
    if case.use_release_input:
        inputs["release"] = case.release

    for step in range(case.steps):
        ctx = TimestepContext(
            run=run,
            step_index=step,
            current_time=clock.current_date,
            dt=clock.time_step,
            inputs=inputs,
        )
        element.update(ctx)
        report = check.verify(element.balance_terms(ctx))
        assert report.passed, (
            f"balance failed at step {step} for {case.label()}: "
            f"residual={report.residual}, terms={report.terms}"
        )
        clock.advance()


def _run_controller_case(case: ReservoirCase) -> None:
    store = SimpleStore(case.quantity, case.capacity)
    if case.use_release_input:
        element = ReservoirElement(store, element_id="res", default_release=0.0)
    else:
        element = ReservoirElement(
            store,
            element_id="res",
            release_key=None,
            default_release=case.release,
        )
    clock = _clock_for_steps(case.steps)
    model = Model(name="FuzzReservoir", clock=clock)
    model.register("res", element)
    inputs = InputManager()
    inputs.bind("inflow", ConstantInput(case.inflow))
    if case.use_release_input:
        inputs.bind("release", ConstantInput(case.release))
    result = RunController(
        model,
        input_manager=inputs,
        verify_mass_balance=True,
        raise_on_error=False,
    ).run()
    assert result.success, f"run failed for {case.label()}: {result.error}"


class TestSimpleStoreMassBalanceFuzz:
    @pytest.mark.parametrize(
        "case",
        _generate_cases(FUZZ_TERM_STEPS),
        ids=lambda c: c.label(),
    )
    def test_balance_terms_random_cases(self, case: ReservoirCase) -> None:
        _assert_balance_terms_each_step(case)

    @pytest.mark.parametrize(
        "case",
        _generate_cases(FUZZ_RUN_STEPS),
        ids=lambda c: f"run-{c.label()}",
    )
    def test_run_controller_random_cases(self, case: ReservoirCase) -> None:
        _run_controller_case(case)

    def test_overflow_edge_in_fuzz_space(self) -> None:
        case = ReservoirCase(
            quantity=98.0,
            capacity=100.0,
            inflow=25.0,
            release=2.0,
            steps=5,
            use_release_input=True,
        )
        _assert_balance_terms_each_step(case)
        _run_controller_case(case)

    def test_drain_to_empty_in_fuzz_space(self) -> None:
        case = ReservoirCase(
            quantity=5.0,
            capacity=200.0,
            inflow=0.0,
            release=20.0,
            steps=3,
            use_release_input=True,
        )
        _assert_balance_terms_each_step(case)
