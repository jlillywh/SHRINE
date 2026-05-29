"""Model builder shared by benchmark tests and update scripts."""

from __future__ import annotations

from hydrology.watershed import Watershed
from shrine.simulation import Model, WatershedElement


def build_benchmark_watershed_model() -> Model:
    """Twin catchments → junction → sink (matches scenario driver topology)."""
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    model = Model(name="BenchmarkBasin")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model
