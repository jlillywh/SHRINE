"""Simulation model registry (MDL-*)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from shrine.simulation.clock import Clock
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.protocols import Simulatable


@dataclass
class RegisteredElement:
    """Element entry in a model."""

    element_id: str
    element: Simulatable
    metadata: dict[str, Any] = field(default_factory=dict)


class Model:
    """Top-level simulation model: clock, element registry, validation."""

    def __init__(
        self,
        name: str = "Model",
        clock: Clock | None = None,
    ) -> None:
        self.name = name
        self.clock = clock or Clock()
        self._elements: dict[str, RegisteredElement] = {}

    def register(
        self,
        element_id: str,
        element: Simulatable,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Register a simulatable element by unique id (MDL-02)."""
        if element_id in self._elements:
            raise SimulationError(
                message=f"Duplicate element id: {element_id!r}",
                phase=SimulationPhase.VALIDATE,
                element_id=element_id,
            )
        self._elements[element_id] = RegisteredElement(
            element_id=element_id,
            element=element,
            metadata=dict(metadata or {}),
        )

    def register_watershed(
        self,
        element_id: str,
        element: Simulatable,
        **metadata: Any,
    ) -> None:
        """Register a watershed (or other graph-owning) element (MDL-07)."""
        meta = {"kind": "watershed", **metadata}
        self.register(element_id, element, metadata=meta)

    def register_catchment(
        self,
        element_id: str,
        element: Simulatable,
        **metadata: Any,
    ) -> None:
        """Register a standalone catchment element (local runoff, no flow network)."""
        meta = {"kind": "catchment", **metadata}
        self.register(element_id, element, metadata=meta)

    def register_reservoir(
        self,
        element_id: str,
        element: Simulatable,
        **metadata: Any,
    ) -> None:
        """Register a storage/reservoir element (local mass balance, no flow network)."""
        meta = {"kind": "reservoir", **metadata}
        self.register(element_id, element, metadata=meta)

    def register_plugin(
        self,
        element_id: str,
        plugin_name: str,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Register an element loaded from a ``shrine.elements`` entry point."""
        from shrine.simulation.plugins import create_element_from_plugin

        element = create_element_from_plugin(plugin_name, *args, **kwargs)
        self.register(element_id, element)

    def get(self, element_id: str) -> Simulatable:
        if element_id not in self._elements:
            raise SimulationError(
                message=f"Unknown element id: {element_id!r}",
                phase=SimulationPhase.VALIDATE,
                element_id=element_id,
            )
        return self._elements[element_id].element

    def elements(self) -> list[RegisteredElement]:
        return list(self._elements.values())

    def watersheds(self) -> list[RegisteredElement]:
        return [e for e in self.elements() if e.metadata.get("kind") == "watershed"]

    def validate(self, *, require_elements: bool = True) -> None:
        """Pre-run validation (MDL-05)."""
        if require_elements and not self._elements:
            raise SimulationError(
                message="Model has no registered elements",
                phase=SimulationPhase.VALIDATE,
            )
        ids = [e.element_id for e in self.elements()]
        if len(ids) != len(set(ids)):
            raise SimulationError(
                message="Duplicate element ids detected",
                phase=SimulationPhase.VALIDATE,
            )
