"""Legacy unit helpers; prefer ``shrine.units`` for new code."""

from __future__ import annotations

from shrine.units import get_default_units, get_unit_registry, load_units

__all__ = ["get_default_units", "get_unit_registry", "load_units", "ureg"]


def __getattr__(name: str):
    if name == "ureg":
        return get_unit_registry()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
