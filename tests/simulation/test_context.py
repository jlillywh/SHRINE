"""Tests for RunContext and TimestepContext."""

from __future__ import annotations

import pandas as pd
import pytest

from shrine.simulation import Clock, RunContext, TimestepContext


def _timestep(run: RunContext) -> TimestepContext:
    return TimestepContext(
        run=run,
        step_index=0,
        current_time=pd.Timestamp("2019-01-01"),
        dt=run.clock.time_step,
    )


def test_timestep_context_rng_raises_when_uninitialized() -> None:
    run = RunContext(model_id="t", clock=Clock("1/1/2019", "1/2/2019"))
    object.__setattr__(run, "rng", None)
    with pytest.raises(RuntimeError, match="RunContext.rng is not initialized"):
        _ = _timestep(run).rng


def test_timestep_context_units_registry_raises_when_uninitialized() -> None:
    run = RunContext(model_id="t", clock=Clock("1/1/2019", "1/2/2019"))
    object.__setattr__(run, "units_registry", None)
    with pytest.raises(RuntimeError, match="RunContext.units_registry is not initialized"):
        _ = _timestep(run).units_registry


def test_timestep_context_default_units_raises_when_uninitialized() -> None:
    run = RunContext(model_id="t", clock=Clock("1/1/2019", "1/2/2019"))
    object.__setattr__(run, "default_units", None)
    with pytest.raises(RuntimeError, match="RunContext.default_units is not initialized"):
        _ = _timestep(run).default_units
