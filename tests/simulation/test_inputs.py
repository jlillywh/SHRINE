"""Tests for aegis.simulation.inputs."""

from __future__ import annotations

import pandas as pd
import pytest

from aegis.simulation import ConstantInput, MonthlyLookupInput
from aegis.simulation.context import RunContext, TimestepContext
from aegis.simulation import Clock


def _timestep(month: int, day: int = 1) -> TimestepContext:
    clock = Clock("1/1/2019", "12/31/2019")
    run = RunContext(model_id="t", clock=clock)
    ts = pd.Timestamp(year=2019, month=month, day=day)
    return TimestepContext(run=run, step_index=0, current_time=ts, dt=clock.time_step)


class TestConstantInput:
    def test_value_at(self) -> None:
        provider = ConstantInput(3.14)
        assert provider.value_at(_timestep(1)) == 3.14


class TestMonthlyLookupInput:
    def test_month_name_lookup(self) -> None:
        values = {"January": 0.1, "February": 0.2}
        provider = MonthlyLookupInput(values)
        assert provider.value_at(_timestep(1, 15)) == pytest.approx(0.1)
        ctx = _timestep(2, 1)
        assert provider.value_at(ctx) == pytest.approx(0.2)

    def test_missing_month_raises(self) -> None:
        provider = MonthlyLookupInput({"January": 1.0})
        with pytest.raises(KeyError):
            provider.value_at(_timestep(3, 1))
