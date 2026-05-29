"""Reference scenario registry (roadmap 3.10)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from shrine.simulation import Model
from tests.reference.models import (
    build_dendritic_routing_model,
    build_nested_junction_model,
    build_single_catchment_model,
    build_twin_catchment_model,
)


@dataclass(frozen=True)
class ReferenceCase:
    scenario: str
    builder: Callable[[], Model]
    golden: str
    expected_first_outflow: float | None = None


REFERENCE_CASES: tuple[ReferenceCase, ...] = (
    ReferenceCase(
        scenario="scenarios/reference/synthetic_single_catchment.yaml",
        builder=build_single_catchment_model,
        golden="synthetic_single_catchment.outputs.sha256",
        expected_first_outflow=5850.0,
    ),
    ReferenceCase(
        scenario="scenarios/reference/synthetic_twin_catchment.yaml",
        builder=build_twin_catchment_model,
        golden="synthetic_twin_catchment.outputs.sha256",
        expected_first_outflow=9100.0,
    ),
    ReferenceCase(
        scenario="scenarios/reference/synthetic_nested_junction.yaml",
        builder=build_nested_junction_model,
        golden="synthetic_nested_junction.outputs.sha256",
        expected_first_outflow=14950.0,
    ),
    ReferenceCase(
        scenario="scenarios/reference/published_dendritic_routing.yaml",
        builder=build_dendritic_routing_model,
        golden="published_dendritic_routing.outputs.sha256",
        expected_first_outflow=23400.0,
    ),
)
