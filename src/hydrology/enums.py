"""Enumerations for hydrology domain APIs (Phase 2)."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hydrology.protocols import RunoffModel


class RunoffMethod(str, Enum):
    """Built-in rainfall–runoff model selectors for :class:`~hydrology.catchment.Catchment`."""

    SIMPLE = "simple"
    AWBM = "awbm"

    @classmethod
    def from_any(cls, value: str | RunoffMethod) -> RunoffMethod:
        """Parse enum member from another member or string (case-insensitive)."""
        if isinstance(value, cls):
            return value
        return cls(value.strip().lower())

    def build(self) -> RunoffModel:
        """Instantiate the corresponding :class:`~hydrology.protocols.RunoffModel`."""
        if self is RunoffMethod.SIMPLE:
            from hydrology.catchment import Rational

            return Rational()
        if self is RunoffMethod.AWBM:
            from hydrology.awbm import Awbm

            return Awbm()
        raise ValueError(f"No RunoffModel factory for {self!r}")


class GraphNodeType(str, Enum):
    """NetworkX node role in a demand / flow graph (GML ``node_type`` attribute)."""

    CATCHMENT = "Catchment"
    JUNCTION = "Junction"
    SINK = "Sink"
    SOURCE = "Source"

    @classmethod
    def from_any(cls, value: str | GraphNodeType) -> GraphNodeType:
        """Parse from enum member or string (case-insensitive; accepts legacy ``sink``)."""
        if isinstance(value, cls):
            return value
        text = str(value).strip()
        if not text:
            raise ValueError("GraphNodeType cannot be parsed from empty string")
        lowered = text.lower()
        for member in cls:
            if member.value.lower() == lowered:
                return member
        raise ValueError(f"Unknown graph node type: {value!r}")
