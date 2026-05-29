"""Output recording (OUT-*)."""

from __future__ import annotations

from numbers import Real
from typing import TYPE_CHECKING, Any, cast

import numpy as np
import pandas as pd

from shrine.simulation.clock import Clock
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.units import get_unit_registry, unit_identity_key, validate_unit_string

if TYPE_CHECKING:
    from pint import UnitRegistry


def _is_bare_numeric(value: Any) -> bool:
    """True when *value* carries no unit (plain number)."""
    if isinstance(value, bool):
        return False
    if isinstance(value, Real):
        return True
    if isinstance(value, (np.floating, np.integer)):
        return True
    return False


def _quantity_unit(value: Any) -> str | None:
    try:
        from pint import Quantity

        if isinstance(value, Quantity):
            return str(value.units)
    except ImportError:
        pass
    return None


class Recorder:
    """Records named outputs per timestep into a wide DataFrame."""

    def __init__(
        self,
        clock: Clock,
        *,
        units_registry: UnitRegistry | None = None,
        validate_units: bool = True,
        strict_units: bool = False,
    ) -> None:
        self._clock = clock
        self._rows: list[dict[str, Any]] = []
        self._units: dict[str, str] = {}
        self._unit_dim_keys: dict[str, str] = {}
        self._units_registry = units_registry
        self._validate_units = validate_units
        self._strict_units = strict_units

    def _registry(self) -> UnitRegistry:
        if self._units_registry is None:
            return get_unit_registry()
        return self._units_registry

    def _set_unit_metadata(self, variable: str, unit: str | None) -> None:
        if unit is None:
            return
        field = f"recorder.{variable}"
        if self._validate_units:
            normalized = validate_unit_string(
                unit,
                field=field,
                registry=self._registry(),
                phase=SimulationPhase.RECORD,
            )
        else:
            normalized = unit.strip()
        registry = self._registry()
        identity_key = unit_identity_key(normalized, registry)
        existing_key = self._unit_dim_keys.get(variable)
        if existing_key is not None and existing_key != identity_key:
            existing = self._units[variable]
            raise SimulationError(
                message=f"Conflicting units for output {variable!r}: "
                f"{existing!r} vs {normalized!r}",
                phase=SimulationPhase.RECORD,
                details={
                    "variable": variable,
                    "existing_unit": existing,
                    "new_unit": normalized,
                },
            )
        if variable not in self._units:
            self._units[variable] = normalized
        self._unit_dim_keys[variable] = identity_key

    def register(self, variable: str, *, unit: str | None = None) -> None:
        self._set_unit_metadata(variable, unit)
        if self._strict_units and unit is None and variable not in self._units:
            raise SimulationError(
                message=f"Output {variable!r} registered without unit metadata (strict_units=True)",
                phase=SimulationPhase.RECORD,
                details={"variable": variable},
            )

    def _enforce_strict_units(self, variable: str, value: Any) -> None:
        if not self._strict_units:
            return
        if variable in self._units:
            return
        if _quantity_unit(value) is not None:
            return
        if not _is_bare_numeric(value):
            return
        raise SimulationError(
            message=f"Bare numeric value recorded for {variable!r} without unit metadata "
            f"(strict_units=True); register with unit= or pass unit= on record",
            phase=SimulationPhase.RECORD,
            details={"variable": variable, "value_type": type(value).__name__},
        )

    def begin_timestep(self, timestamp: pd.Timestamp) -> None:
        """Start a new output row for the current timestep."""
        self._rows.append({"time": timestamp})

    def record(
        self,
        variable: str,
        value: Any,
        *,
        unit: str | None = None,
    ) -> None:
        effective_unit = unit or _quantity_unit(value)
        self._set_unit_metadata(variable, effective_unit)
        self._enforce_strict_units(variable, value)
        if not self._rows:
            self.begin_timestep(self._clock.current_date)
        self._rows[-1][variable] = value

    def to_dataframe(self) -> pd.DataFrame:
        if not self._rows:
            return pd.DataFrame()
        df = pd.DataFrame(self._rows).set_index("time")
        df.index.name = "time"
        return cast(pd.DataFrame, df)

    @property
    def units(self) -> dict[str, str]:
        return dict(self._units)

    def reset(self) -> None:
        self._rows.clear()

    def load_dataframe(self, df: pd.DataFrame) -> None:
        """Replace recorded rows from a wide time-indexed DataFrame."""
        self.reset()
        if df.empty:
            return
        frame = df.copy()
        if frame.index.name != "time":
            frame = frame.reset_index()
            if "time" not in frame.columns:
                frame = frame.rename(columns={frame.columns[0]: "time"})
            frame = frame.set_index("time")
        for ts, row in frame.iterrows():
            self.begin_timestep(pd.Timestamp(cast(Any, ts)))
            for col, val in row.items():
                if pd.notna(val):
                    self.record(str(col), val)

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        clock: Clock | None = None,
        *,
        units_registry: UnitRegistry | None = None,
        validate_units: bool = True,
        strict_units: bool = False,
    ) -> Recorder:
        """Build a recorder pre-filled from a wide DataFrame (time index)."""
        if clock is None:
            if df.empty:
                clock = Clock()
            else:
                index = pd.DatetimeIndex(df.index)
                step = index[1] - index[0] if len(index) > 1 else pd.Timedelta("1 days")
                clock = Clock(index[0], index[-1], time_step=step)
        recorder = cls(
            clock,
            units_registry=units_registry,
            validate_units=validate_units,
            strict_units=strict_units,
        )
        recorder.load_dataframe(df)
        return recorder
