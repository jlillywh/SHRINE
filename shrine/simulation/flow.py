"""Flow solve types and backends (FLW-*, D3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import networkx as nx

from shrine.simulation.errors import SimulationError, SimulationPhase


@dataclass
class FlowSolveResult:
    """Result of a network flow solve for one timestep (FLW-02)."""

    success: bool
    method: str
    total_flow: float = 0.0
    edge_flows: dict[tuple[str, str], float] = field(default_factory=dict)
    residual: float | None = None
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)


SolveMethod = Literal["max", "min_cost"]


class NetworkXFlowSolver:
    """NetworkX max-flow / min-cost flow backend (FLW-04)."""

    def __init__(self, method: SolveMethod = "max") -> None:
        self.method = method

    def solve(
        self,
        graph: nx.DiGraph,
        source: str,
        sink: str,
        *,
        capacity_attr: str = "capacity",
        element_id: str | None = None,
    ) -> FlowSolveResult:
        try:
            if self.method == "max":
                return self._solve_max_flow(graph, source, sink, capacity_attr, element_id)
            return self._solve_min_cost(graph, source, sink, element_id)
        except nx.NetworkXError as exc:
            raise SimulationError(
                message=f"Flow solve failed: {exc}",
                phase=SimulationPhase.FLOW_SOLVE,
                element_id=element_id,
                details={"method": self.method, "source": source, "sink": sink},
            ) from exc

    def _solve_max_flow(
        self,
        graph: nx.DiGraph,
        source: str,
        sink: str,
        capacity_attr: str,
        element_id: str | None,
    ) -> FlowSolveResult:
        flow_value, flow_dict = nx.maximum_flow(
            graph, source, sink, capacity=capacity_attr
        )
        edge_flows = self._flatten_flow_dict(flow_dict)
        total_at_sink = sum(flow_dict[pred][sink] for pred in graph.predecessors(sink))
        return FlowSolveResult(
            success=True,
            method="maximum_flow",
            total_flow=float(total_at_sink),
            edge_flows=edge_flows,
            residual=float(flow_value) - float(total_at_sink),
            message="ok",
            details={"flow_value": float(flow_value)},
        )

    def _solve_min_cost(
        self,
        graph: nx.DiGraph,
        source: str,
        sink: str,
        element_id: str | None,
    ) -> FlowSolveResult:
        flow_cost, flow_dict = nx.network_simplex(graph)
        edge_flows = self._flatten_flow_dict(flow_dict)
        total_at_sink = sum(flow_dict[pred][sink] for pred in graph.predecessors(sink))
        return FlowSolveResult(
            success=True,
            method="network_simplex",
            total_flow=float(total_at_sink),
            edge_flows=edge_flows,
            message="ok",
            details={"flow_cost": float(flow_cost)},
        )

    @staticmethod
    def _flatten_flow_dict(flow_dict: dict[str, dict[str, float]]) -> dict[tuple[str, str], float]:
        edge_flows: dict[tuple[str, str], float] = {}
        for upstream, targets in flow_dict.items():
            for downstream, flow in targets.items():
                if flow:
                    edge_flows[(upstream, downstream)] = float(flow)
        return edge_flows


# Backwards-compatible alias
FlowSolver = NetworkXFlowSolver
