"""Tests for shrine.simulation.flow."""

from __future__ import annotations

import networkx as nx
import pytest

from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.flow import NetworkXFlowSolver
from hydrology.catchment import Catchment
from hydrology.watershed import Watershed


def _built_watershed() -> Watershed:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    return ws


class TestNetworkXFlowSolver:
    def test_max_flow_matches_catchment_sum(self) -> None:
        ws = _built_watershed()
        precip, et = 10.0, 1.0
        expected = Catchment().outflow(precip, et) * 2
        for name, catchment in ws.iter_catchment_items():
            ws.update_capacity(name, catchment.outflow(precip, et))

        result = NetworkXFlowSolver("max").solve(
            ws.dg, ws.source, ws.sink, element_id="test_ws"
        )
        assert result.success
        assert result.method == "maximum_flow"
        assert result.total_flow == pytest.approx(expected, rel=1e-5)
        assert len(result.edge_flows) > 0

    def test_flatten_flow_dict(self) -> None:
        flows = NetworkXFlowSolver._flatten_flow_dict(
            {"source": {"C1": 5.0}, "C1": {"sink": 5.0}}
        )
        assert flows[("source", "C1")] == 5.0
        assert flows[("C1", "sink")] == 5.0

    def test_disconnected_graph_raises_flow_solve_error(self) -> None:
        g = nx.DiGraph()
        g.add_edge("a", "b", capacity=1.0)
        solver = NetworkXFlowSolver()
        with pytest.raises(SimulationError) as exc_info:
            solver.solve(g, "a", "z", element_id="broken")
        assert exc_info.value.phase == SimulationPhase.FLOW_SOLVE
