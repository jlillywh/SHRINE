"""Top-level element execution order (TOP-01)."""

from __future__ import annotations

from aegis.simulation.model import Model, RegisteredElement


class ElementScheduler:
    """Returns registered elements in registration order (v1).

    Future: topological sort across top-level elements when dependencies exist.
    """

    def execution_order(self, model: Model) -> list[RegisteredElement]:
        return model.elements()
