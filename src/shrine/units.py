"""SHRINE unit registry and default units (loaded once per process)."""

from __future__ import annotations

import importlib.util
import json
import re
import warnings
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pint import UnitRegistry

from shrine.simulation.errors import SimulationError, SimulationPhase

_UNIT_SYNTAX = re.compile(r"^[a-zA-Z][a-zA-Z0-9./\*\-\s]*$")
_PINT_AVAILABLE = importlib.util.find_spec("pint") is not None

# Package data: ``src/data/shrine_units.json`` (also shipped via setuptools package-data).
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SHRINE_UNITS_JSON = _DATA_DIR / "shrine_units.json"
SHRINE_UNITS_TXT = _DATA_DIR / "shrine_units.txt"


@lru_cache(maxsize=1)
def get_default_units() -> dict[str, str]:
    """Load default unit strings from ``shrine_units.json`` (once per process)."""
    with SHRINE_UNITS_JSON.open(encoding="utf-8") as file:
        data: dict[str, str] = json.load(file)
    return data


@lru_cache(maxsize=1)
def get_unit_registry(*, auto_reduce_dimensions: bool = True) -> UnitRegistry:
    """Return the shared pint ``UnitRegistry`` for simulation runs."""
    from pint import UnitRegistry

    registry = UnitRegistry(auto_reduce_dimensions=auto_reduce_dimensions)
    if SHRINE_UNITS_TXT.is_file():
        registry.load_definitions(str(SHRINE_UNITS_TXT))
    return registry


def load_units(filepath: str | Path | None = None) -> dict[str, str]:
    """Load unit defaults from JSON (defaults to ``shrine_units.json``).

    Prefer :func:`get_default_units` for the canonical SHRINE defaults file.
    """
    path = Path(filepath) if filepath is not None else SHRINE_UNITS_JSON
    if path.resolve() == SHRINE_UNITS_JSON.resolve():
        return dict(get_default_units())
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def reset_unit_caches() -> None:
    """Clear cached registry and defaults (for tests only)."""
    get_default_units.cache_clear()
    get_unit_registry.cache_clear()


def _validate_unit_syntax(text: str, *, field: str) -> None:
    if not _UNIT_SYNTAX.match(text):
        raise SimulationError(
            message=f"Invalid unit in {field}: {text!r}",
            phase=SimulationPhase.VALIDATE,
            details={"field": field, "unit": text},
        )


def _normalize_hydro_unit_text(text: str) -> str:
    """Map common hydrology abbreviations to pint-parseable unit strings."""
    out = text.strip()
    if out == "in":
        return "inch"
    for old, new in (
        ("m3/", "m**3/"),
        ("ft3/", "ft**3/"),
        ("in/", "inch/"),
    ):
        out = out.replace(old, new)
    return out


def _pint_accepts_unit(ureg: UnitRegistry, text: str) -> bool:
    pint_text = _normalize_hydro_unit_text(text)
    try:
        ureg.Unit(pint_text)
        return True
    except Exception:
        try:
            ureg.Quantity(1, pint_text)
            return True
        except Exception:
            return False


def unit_identity_key(
    unit: str,
    registry: UnitRegistry | None = None,
) -> str:
    """Pint unit identity for conflict checks.

    Treats alias spellings as equal (``m3/s`` vs ``m**3/s``) but distinct units
    as conflicting (``m3/s`` vs ``ft3/s``), even though they share dimensions.
    """
    ureg = registry if registry is not None else get_unit_registry()
    pint_text = _normalize_hydro_unit_text(unit)
    return str(ureg.Quantity(1, pint_text).units)


def validate_unit_string(
    unit: Any,
    *,
    field: str,
    registry: UnitRegistry | None = None,
    phase: SimulationPhase = SimulationPhase.VALIDATE,
    warn_if_no_pint: bool = True,
) -> str:
    """Validate a unit string with pint (or syntax-only) and return normalized text."""
    if not isinstance(unit, str) or not unit.strip():
        raise SimulationError(
            message=f"Invalid unit in {field}: unit must be a non-empty string",
            phase=phase,
            details={"field": field, "unit": unit},
        )
    text = unit.strip()
    if not _PINT_AVAILABLE:
        if warn_if_no_pint:
            warnings.warn(
                "pint is not installed; validating units with syntax checks only. "
                "Install project dependencies for full validation (pip install -e .).",
                stacklevel=3,
            )
        _validate_unit_syntax(text, field=field)
        return text
    ureg = registry if registry is not None else get_unit_registry()
    if not _pint_accepts_unit(ureg, text):
        raise SimulationError(
            message=f"Invalid unit in {field}: {unit!r}",
            phase=phase,
            details={"field": field, "unit": unit},
        )
    return text
