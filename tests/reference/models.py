"""Model builders for scenarios/reference/ (roadmap 3.10)."""

from __future__ import annotations

from collections.abc import Callable

from hydrology.watershed import Watershed
from shrine.simulation import Model, WatershedElement

ModelBuilder = Callable[[], Model]


def build_single_catchment_model() -> Model:
    """REF-1C: one catchment draining directly to the sink."""
    ws = Watershed()
    ws.link_catchment("C1", "sink")
    model = Model(name="RefSingleCatchment")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def build_twin_catchment_model() -> Model:
    """REF-2C: two parallel catchments converging at J1."""
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    model = Model(name="RefTwinCatchment")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def build_nested_junction_model() -> Model:
    """REF-NJ: C1→J1, C2→J5→J1 (matches tests/conftest nested_junction_watershed)."""
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.add_junction("J5", "J1")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J5")
    model = Model(name="RefNestedJunction")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def build_dendritic_routing_model() -> Model:
    """REF-4C2J: four catchments, two junctions (tests/water_manage/test_network layout)."""
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.add_junction("J2", "J1")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    ws.link_catchment("C3", "J2")
    ws.link_catchment("C4", "J2")
    model = Model(name="RefDendriticRouting")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model
