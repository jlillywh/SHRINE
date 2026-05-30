"""Input binding for timesteps (INP-*)."""

from __future__ import annotations

from typing import Any, Protocol

import pandas as pd

from shrine.simulation.context import TimestepContext
from shrine.simulation.errors import SimulationError, SimulationPhase


class InputProvider(Protocol):
    """Provides a value at the current simulation time."""

    def value_at(self, context: TimestepContext) -> Any:
        """Return the input value for ``context.current_time``."""
        ...


class ConstantInput:
    """Fixed scalar input."""

    def __init__(self, value: float) -> None:
        self.value = value

    def value_at(self, context: TimestepContext) -> float:
        return self.value


class StochasticInput:
    """Random input drawn from the run's seeded generator (INP-04).

    Supported ``distribution`` values: ``normal``, ``uniform``.
    """

    def __init__(
        self,
        distribution: str,
        *,
        loc: float = 0.0,
        scale: float = 1.0,
        low: float = 0.0,
        high: float = 1.0,
    ) -> None:
        self.distribution = distribution
        self.loc = loc
        self.scale = scale
        self.low = low
        self.high = high

    def value_at(self, context: TimestepContext) -> float:
        rng = context.rng
        if self.distribution == "normal":
            return float(rng.normal(self.loc, self.scale))
        if self.distribution == "uniform":
            return float(rng.uniform(self.low, self.high))
        raise ValueError(f"Unknown distribution: {self.distribution!r}")


class MonthlyLookupInput:
    """Lookup by calendar month name (e.g. ``January``)."""

    def __init__(self, values_by_month: dict[str, float]) -> None:
        self.values_by_month = values_by_month

    def value_at(self, context: TimestepContext) -> float:
        month = context.current_time.month_name()
        try:
            return float(self.values_by_month[month])
        except KeyError as exc:
            raise KeyError(f"No value for month {month!r}") from exc


class TimeSeriesCsvInput:
    """Time-varying scalar input loaded from a CSV column (roadmap 3.14)."""

    def __init__(self, series: pd.Series) -> None:
        if series.empty:
            raise SimulationError(
                message="CSV time series must not be empty",
                phase=SimulationPhase.VALIDATE,
            )
        normalized = series.copy()
        normalized.index = pd.to_datetime(normalized.index)
        self._series = normalized.sort_index()

    def value_at(self, context: TimestepContext) -> float:
        ts = pd.Timestamp(context.current_time)
        try:
            return float(self._series.loc[ts])
        except KeyError:
            pass
        day = ts.normalize()
        dt_index = pd.DatetimeIndex(self._series.index)
        matches = self._series.loc[dt_index.normalize() == day]
        if not matches.empty:
            return float(matches.iloc[0])
        raise SimulationError(
            message=f"No CSV time-series value for {ts.isoformat()}",
            phase=SimulationPhase.INPUT,
            step_index=context.step_index,
            timestamp=ts,
        )


class InputManager:
    """Named global inputs for a model run."""

    def __init__(self) -> None:
        self._bindings: dict[str, InputProvider] = {}

    def bind(self, name: str, provider: InputProvider) -> None:
        """Register ``provider`` under ``name`` for the run."""
        self._bindings[name] = provider

    def values_for_timestep(self, context: TimestepContext) -> dict[str, Any]:
        """Evaluate all bound providers at the current timestep."""
        return {name: provider.value_at(context) for name, provider in self._bindings.items()}
