"""Discover and load third-party ``Simulatable`` elements via setuptools entry points."""

from __future__ import annotations

import importlib.metadata
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.protocols import Simulatable

ELEMENTS_ENTRY_POINT_GROUP = "shrine.elements"

ElementFactory = Callable[..., Simulatable]
ElementPluginTarget = type[Any] | ElementFactory


@dataclass(frozen=True)
class ElementPlugin:
    """Metadata for a registered ``shrine.elements`` entry point."""

    name: str
    value: str
    target: ElementPluginTarget


def _entry_points_for_group(group: str) -> importlib.metadata.EntryPoints:
    return importlib.metadata.entry_points(group=group)


def iter_element_plugins() -> Iterator[importlib.metadata.EntryPoint]:
    """Yield entry points in the ``shrine.elements`` group."""
    return iter(_entry_points_for_group(ELEMENTS_ENTRY_POINT_GROUP))


@lru_cache(maxsize=1)
def _plugin_index() -> dict[str, importlib.metadata.EntryPoint]:
    plugins: dict[str, importlib.metadata.EntryPoint] = {}
    for entry_point in iter_element_plugins():
        if entry_point.name in plugins:
            raise SimulationError(
                message=(
                    f"Duplicate shrine.elements entry point name: {entry_point.name!r} "
                    f"({plugins[entry_point.name].value} vs {entry_point.value})"
                ),
                phase=SimulationPhase.VALIDATE,
            )
        plugins[entry_point.name] = entry_point
    return plugins


def clear_plugin_cache() -> None:
    """Clear cached entry-point lookups (for tests)."""
    _plugin_index.cache_clear()


def list_element_plugins() -> dict[str, str]:
    """Return ``{plugin_name: entry_point_value}`` for all discovered plugins."""
    return {name: ep.value for name, ep in sorted(_plugin_index().items())}


def load_element_plugin(name: str) -> ElementPlugin:
    """Load an entry point by name without instantiating an element."""
    try:
        entry_point = _plugin_index()[name]
    except KeyError as exc:
        known = ", ".join(sorted(_plugin_index())) or "(none)"
        raise SimulationError(
            message=f"Unknown element plugin: {name!r}; known plugins: {known}",
            phase=SimulationPhase.VALIDATE,
            details={"plugin_name": name, "known_plugins": list(_plugin_index())},
        ) from exc

    try:
        target = entry_point.load()
    except Exception as exc:
        raise SimulationError(
            message=f"Failed to load element plugin {name!r} ({entry_point.value})",
            phase=SimulationPhase.VALIDATE,
            details={"plugin_name": name, "entry_point": entry_point.value},
        ) from exc

    if not isinstance(target, type) and not callable(target):
        raise SimulationError(
            message=(
                f"Element plugin {name!r} must resolve to a class or callable factory; "
                f"got {type(target).__name__}"
            ),
            phase=SimulationPhase.VALIDATE,
            details={"plugin_name": name, "entry_point": entry_point.value},
        )

    return ElementPlugin(name=name, value=entry_point.value, target=target)


def create_element_from_plugin(name: str, /, *args: Any, **kwargs: Any) -> Simulatable:
    """Instantiate a ``Simulatable`` from a ``shrine.elements`` entry point."""
    plugin = load_element_plugin(name)
    try:
        element = plugin.target(*args, **kwargs)
    except Exception as exc:
        raise SimulationError(
            message=f"Failed to construct element from plugin {name!r}",
            phase=SimulationPhase.VALIDATE,
            details={"plugin_name": name, "entry_point": plugin.value},
        ) from exc

    if not isinstance(element, Simulatable):
        raise SimulationError(
            message=(
                f"Element plugin {name!r} did not return a Simulatable instance; "
                f"got {type(element).__name__}"
            ),
            phase=SimulationPhase.VALIDATE,
            details={"plugin_name": name, "entry_point": plugin.value},
        )
    return element
