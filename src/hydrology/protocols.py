"""Typed contracts for hydrology domain modules (Phase 2)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from pint import Quantity

# Default depth rate for simple rational runoff (catchment tests use generic floats).
DEFAULT_RUNOFF_UNIT = "mm/day"
# AWBM ``runoff`` returns depth per day in metres (see ``Awbm.runoff`` docstring).
AWBM_RUNOFF_UNIT = "m/day"


@runtime_checkable
class RunoffModel(Protocol):
    """Per-unit-area rainfall–runoff model.

    Implementations return a pint ``Quantity`` depth rate (e.g. ``mm/day``, ``m/day``).
    Volumetric catchment outflow is ``compute(precip, et).magnitude * area`` when
    magnitudes share consistent length/time dimensions, or use explicit unit conversion.
    """

    def compute(self, precip: float, et: float) -> Quantity:
        """Runoff depth rate from precipitation and evapotranspiration."""
        ...


class LegacyRunoffAdapter:
    """Wrap legacy objects that implement ``runoff(precip, et) -> float``."""

    def __init__(
        self,
        legacy: object,
        *,
        unit: str = DEFAULT_RUNOFF_UNIT,
    ) -> None:
        self._legacy = legacy
        self._unit = unit

    def compute(self, precip: float, et: float) -> Quantity:
        from shrine.units import get_unit_registry

        rate = self._legacy.runoff(precip, et)
        return get_unit_registry().Quantity(rate, self._unit)


def as_runoff_model(model: object, *, unit: str = DEFAULT_RUNOFF_UNIT) -> RunoffModel:
    """Return a :class:`RunoffModel`, wrapping legacy ``runoff`` objects when needed."""
    if isinstance(model, RunoffModel):
        return model
    if hasattr(model, "compute"):
        return model  # type: ignore[return-value]
    return LegacyRunoffAdapter(model, unit=unit)
