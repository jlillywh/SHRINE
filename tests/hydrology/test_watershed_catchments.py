"""Tests for Watershed catchment storage on graph nodes (roadmap 2.6)."""

from __future__ import annotations

import warnings

import pytest

from hydrology.catchment import Catchment
from hydrology.graph_nodes import CatchmentNode, get_node_payload_or_raise
from hydrology.watershed import Watershed


class TestWatershedCatchmentRegistry:
    def test_get_catchment_from_graph(self) -> None:
        ws = Watershed()
        created = ws.link_catchment("C1", "sink")
        assert ws.get_catchment("C1") is created

    def test_custom_catchment_instance(self) -> None:
        ws = Watershed()
        custom = Catchment(area=2000.0)
        ws.link_catchment("C1", "sink", catchment=custom)
        assert ws.get_catchment("C1") is custom
        assert ws.get_catchment("C1").area == 2000.0

    def test_no_parallel_dict_on_init(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        assert "catchments" not in ws.__dict__

    def test_catchments_property_deprecated_snapshot(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        with pytest.warns(DeprecationWarning, match="Watershed.catchments is deprecated"):
            snap = ws.catchments
        assert snap["C1"] is ws.get_catchment("C1")

    def test_discharge_uses_graph_catchments(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        expected = ws.get_catchment("C1").outflow(10.0, 1.0)
        assert ws.discharge(10.0, 1.0) == pytest.approx(expected)

    def test_payload_is_canonical_after_link(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        payload = get_node_payload_or_raise(ws.dg, "C1", CatchmentNode)
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            assert payload.catchment is ws.get_catchment("C1")
