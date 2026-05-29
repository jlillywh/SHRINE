"""Flow network routing (migrated from src/water_manage/test_network.py)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from water_manage.flow_network import Network


class TestFlowNetwork:
    def test_flow_capacity(self, flow_network: Network) -> None:
        flow = np.random.random()
        flow_network.add_catchment("C1")
        flow_network.update_capacity("C1", flow)
        assert flow_network.outflow() == flow

    def test_two_catchments_to_sink(self, flow_network: Network) -> None:
        flow1 = np.random.random()
        flow2 = np.random.random()
        flow_network.add_catchment("C1")
        flow_network.add_catchment("C2")
        flow_network.update_capacity("C1", flow1)
        flow_network.update_capacity("C2", flow2)
        assert flow_network.outflow() == pytest.approx(flow1 + flow2)

    def test_junction_joins_two_catchments(self, flow_network: Network) -> None:
        flow1 = np.random.random()
        flow2 = np.random.random()
        flow_network.add_junction("J1", "sink")
        flow_network.add_catchment("C1", "J1")
        flow_network.add_catchment("C2", "J1")
        flow_network.update_capacity("C1", flow1)
        flow_network.update_capacity("C2", flow2)
        assert flow_network.outflow() == pytest.approx(flow1 + flow2)

    def test_multiple_junctions(self, flow_network: Network) -> None:
        flow1 = np.random.uniform(1, 100)
        flow2 = np.random.uniform(1, 100)
        flow3 = np.random.uniform(1, 100)
        flow4 = np.random.uniform(1, 100)
        expected_sum = flow1 + flow2 + flow3 + flow4
        flow_network.add_junction("J1", "sink")
        flow_network.add_junction("J2", "J1")
        flow_network.add_catchment("C1", "J1")
        flow_network.add_catchment("C2", "J1")
        flow_network.add_catchment("C3", "J2")
        flow_network.add_catchment("C4", "J2")
        flow_network.update_capacity("C1", flow1)
        flow_network.update_capacity("C2", flow2)
        flow_network.update_capacity("C3", flow3)
        flow_network.update_capacity("C4", flow4)
        assert flow_network.outflow() == pytest.approx(expected_sum, abs=1e-5)

    def test_update_all(self, flow_network: Network) -> None:
        flow1 = np.random.uniform(1, 100)
        flow2 = np.random.uniform(1, 100)
        flow3 = np.random.uniform(1, 100)
        flow4 = np.random.uniform(1, 100)
        expected_sum = flow1 + flow2 + flow3 + flow4
        flow_network.add_junction("J1", "sink")
        flow_network.add_junction("J2", "J1")
        flow_network.add_catchment("C1", "J1")
        flow_network.add_catchment("C2", "J1")
        flow_network.add_catchment("C3", "J2")
        flow_network.add_catchment("C4", "J2")
        flow_network.update_all({"C1": flow1, "C2": flow2, "C3": flow3, "C4": flow4})
        assert flow_network.outflow() == pytest.approx(expected_sum, abs=1e-5)

    def test_read_from_gml(self, flow_network: Network, network_gml: Path) -> None:
        flow_network.load_from_file(str(network_gml))
        flow1 = np.random.uniform(1, 100)
        flow2 = np.random.uniform(1, 100)
        flow3 = np.random.uniform(1, 100)
        flow4 = np.random.uniform(1, 100)
        expected_sum = flow1 + flow2 + flow3 + flow4
        flow_network.update_all({"C1": flow1, "C2": flow2, "C3": flow3, "C4": flow4})
        flow_network.outflow()
        assert flow_network.outflow() == pytest.approx(expected_sum, abs=1e-5)
