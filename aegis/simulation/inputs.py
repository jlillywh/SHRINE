"""Input binding for timesteps (INP-*)."""

from __future__ import annotations

from typing import Any, Protocol

from aegis.simulation.context import TimestepContext


class InputProvider(Protocol):
    """Provides a value at the current simulation time."""

    def value_at(self, context: TimestepContext) -> Any:
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
        rng = context.run.rng
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


class InputManager:
    """Named global inputs for a model run."""

    def __init__(self) -> None:
        self._bindings: dict[str, InputProvider] = {}

    def bind(self, name: str, provider: InputProvider) -> None:
        self._bindings[name] = provider

    def values_for_timestep(self, context: TimestepContext) -> dict[str, Any]:
        return {name: provider.value_at(context) for name, provider in self._bindings.items()}
