"""Tests for hydrology.enums.GraphNodeType (roadmap 2.7)."""

from __future__ import annotations

import pytest

from hydrology.enums import GraphNodeType
from hydrology.graph_nodes import get_node_type
from hydrology.watershed import Watershed


class TestGraphNodeTypeEnum:
    def test_str_enum_equals_gml_value(self) -> None:
        assert GraphNodeType.CATCHMENT == "Catchment"
        assert GraphNodeType.JUNCTION.value == "Junction"

    def test_from_any_rejects_unknown(self) -> None:
        with pytest.raises(ValueError, match="Unknown graph node type"):
            GraphNodeType.from_any("Dam")

    def test_network_stores_enum_after_add_catchment(self) -> None:
        ws = Watershed()
        ws.link_catchment("C1", "sink")
        assert ws.dg.nodes["C1"]["node_type"] is GraphNodeType.CATCHMENT
        assert get_node_type(ws.dg, "C1") is GraphNodeType.CATCHMENT
