"""Tests for hydrology.graph_nodes (roadmap 2.5)."""

from __future__ import annotations

import pytest

from hydrology.catchment import Catchment
from hydrology.enums import GraphNodeType
from hydrology.graph_nodes import (
    CatchmentNode,
    JunctionNode,
    SinkNode,
    SourceNode,
    attach_payloads_from_node_type,
    catchment_from_payload,
    get_node_payload,
    get_node_payload_or_raise,
    get_node_type,
    iter_catchment_items,
    iter_catchment_nodes,
)
from hydrology.watershed import Watershed


class TestGraphNodePayloads:
    def test_watershed_link_catchment_sets_payload(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        payload = get_node_payload_or_raise(ws.dg, "C1", CatchmentNode)
        assert payload.node_id == "C1"
        assert payload.catchment is ws.get_catchment("C1")
        assert get_node_type(ws.dg, "C1") is GraphNodeType.CATCHMENT

    def test_add_junction_sets_payload(self) -> None:
        ws = Watershed()
        ws.add_junction("J1", "sink")
        payload = get_node_payload_or_raise(ws.dg, "J1", JunctionNode)
        assert payload.node_id == "J1"
        assert get_node_type(ws.dg, "J1") is GraphNodeType.JUNCTION

    def test_source_and_sink_payloads(self) -> None:
        ws = Watershed()
        assert isinstance(get_node_payload(ws.dg, "source"), SourceNode)
        assert isinstance(get_node_payload(ws.dg, "sink"), SinkNode)

    def test_discharge_unchanged_with_payloads(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        expected = Catchment().outflow(10.0, 1.0)
        assert ws.discharge(10.0, 1.0) == expected

    def test_attach_payloads_from_legacy_node_type(self) -> None:
        import networkx as nx

        graph = nx.DiGraph()
        graph.add_node("source", node_type="Source")
        graph.add_node("C1", node_type="Catchment")
        graph.add_node("J1", node_type="Junction")
        graph.add_node("sink", node_type="Sink")
        attach_payloads_from_node_type(
            graph,
            source_id="source",
            sink_id="sink",
        )
        assert len(iter_catchment_nodes(graph)) == 1
        assert catchment_from_payload(graph, "C1") is not None

    def test_iter_catchment_items_is_source_of_truth(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        ws.link_catchment("C2", "sink")
        items = dict(ws.iter_catchment_items())
        assert set(items) == {"C1", "C2"}
        with pytest.warns(DeprecationWarning):
            assert set(ws.catchments) == {"C1", "C2"}


class TestGraphNodeType:
    def test_from_any_accepts_gml_strings(self) -> None:
        assert GraphNodeType.from_any("Catchment") is GraphNodeType.CATCHMENT
        assert GraphNodeType.from_any("junction") is GraphNodeType.JUNCTION
        assert GraphNodeType.from_any("sink") is GraphNodeType.SINK

    def test_load_gml_sets_enum_node_types(self) -> None:
        from pathlib import Path

        gml = Path(__file__).resolve().parents[2] / "src/hydrology/test_data/watershed_GML_input.gml"
        ws = Watershed()
        ws.load_from_file(str(gml))
        assert get_node_type(ws.dg, "C1") is GraphNodeType.CATCHMENT
        assert get_node_type(ws.dg, "J1") is GraphNodeType.JUNCTION
