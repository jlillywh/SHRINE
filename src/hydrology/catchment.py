"""Catchment rainfall–runoff (legacy domain; Phase 2 typed runoff)."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Union

from hydrology.enums import RunoffMethod
from hydrology.protocols import RunoffModel, as_runoff_model

if TYPE_CHECKING:
    from hydrology.awbm import Awbm

RunoffMethodArg = Union[RunoffModel, RunoffMethod, str, "Rational", "Awbm"]


def _warn_string_runoff_method(name: str, *, stacklevel: int = 3) -> None:
    warnings.warn(
        f"Passing runoff_method={name!r} as a string is deprecated; "
        f"use RunoffMethod (e.g. RunoffMethod.SIMPLE) or a RunoffModel instance.",
        DeprecationWarning,
        stacklevel=stacklevel,
    )


def _resolve_runoff(runoff_method: RunoffMethodArg) -> RunoffModel:
    if isinstance(runoff_method, RunoffMethod):
        return runoff_method.build()
    if isinstance(runoff_method, str):
        _warn_string_runoff_method(runoff_method, stacklevel=4)
        return RunoffMethod.from_any(runoff_method).build()
    return as_runoff_model(runoff_method)


def _legacy_peer(model: RunoffModel) -> object:
    """Underlying object for legacy attribute access (``.loss``, ``.runoff``)."""
    from hydrology.protocols import LegacyRunoffAdapter

    if isinstance(model, LegacyRunoffAdapter):
        return model._legacy
    return model


class Catchment:
    """
    A class used to create watershed catchment objects.

    The catchment represents a portion of a watershed that
    accepts rainfall (less et) to produce an outflow.

    Parameters
    ----------
    area : float
        Catchment area (legacy tests treat this as m² for volumetric outflow).
    runoff_method : RunoffModel, RunoffMethod, or str
        ``RunoffModel`` instance (preferred), ``RunoffMethod`` enum, or deprecated string.
    """

    def __init__(
        self,
        area: float = 1000.0,
        runoff_method: RunoffMethodArg = RunoffMethod.SIMPLE,
    ) -> None:
        self.area = area
        self._runoff = _resolve_runoff(runoff_method)
        self.runoff_method = _legacy_peer(self._runoff)

    @property
    def runoff(self) -> RunoffModel:
        """Typed runoff model (Phase 2)."""
        return self._runoff

    def outflow(self, precip: float, et: float) -> float:
        """Volumetric outflow from precipitation and evapotranspiration."""
        if hasattr(self.runoff_method, "runoff"):
            depth_rate = float(self.runoff_method.runoff(precip, et))
        else:
            depth_rate = float(self._runoff.compute(precip, et).magnitude)
        return depth_rate * self.area


class Rational:
    """A class used to represent a simple mass balance of inflow and outflow"""

    def __init__(self) -> None:
        self.loss = 0.35

    def runoff(self, precip: float, et: float) -> float:
        precip_excess = precip - et
        return precip_excess * (1 - self.loss)

    def compute(self, precip: float, et: float):
        """Runoff depth rate (:class:`~hydrology.protocols.RunoffModel`)."""
        from hydrology.protocols import DEFAULT_RUNOFF_UNIT
        from shrine.units import get_unit_registry

        return get_unit_registry().Quantity(self.runoff(precip, et), DEFAULT_RUNOFF_UNIT)
