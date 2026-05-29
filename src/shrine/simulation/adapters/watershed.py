"""Adapter: legacy :class:`~hydrology.watershed.Watershed` → :class:`~shrine.simulation.protocols.Simulatable`."""

from __future__ import annotations

from typing import TYPE_CHECKING

from shrine.simulation.balance import MassBalanceTerm
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.flow import FlowSolveResult, NetworkXFlowSolver, SolveMethod

if TYPE_CHECKING:
    from hydrology.watershed import Watershed


class WatershedElement:
    """Runs a graph-owning watershed each timestep (D2, FLW-01).

    The underlying :class:`~hydrology.watershed.Watershed` retains ownership of
    the NetworkX graph. This adapter:

    1. Reads precip/ET from timestep inputs
    2. Updates catchment supplies on the graph
    3. Solves flows (max-flow by default)
    4. Exposes mass-balance terms (supply vs routed outflow)
    """

    element_type = "watershed"

    def __init__(
        self,
        watershed: Watershed | None = None,
        *,
        element_id: str = "watershed",
        precip_key: str = "precipitation",
        et_key: str = "evaporation",
        solve_method: SolveMethod = "max",
    ) -> None:
        if watershed is None:
            from hydrology.watershed import Watershed

            watershed = Watershed()
        self.watershed = watershed
        self.element_id = element_id
        self.precip_key = precip_key
        self.et_key = et_key
        self._solver = NetworkXFlowSolver(method=solve_method)
        self._last_total_supply = 0.0
        self._last_outflow = 0.0
        self._last_solve: FlowSolveResult | None = None

    def initialize(self, run_context: RunContext) -> None:
        recorder = run_context.recorder
        if recorder is not None:
            recorder.register(f"{self.element_id}.outflow")
            recorder.register(f"{self.element_id}.total_supply")

    def update(self, timestep_context: TimestepContext) -> None:
        try:
            precip = float(timestep_context.inputs[self.precip_key])
            et = float(timestep_context.inputs[self.et_key])
        except KeyError as exc:
            raise SimulationError(
                message=f"Missing climate input: {exc}",
                phase=SimulationPhase.INPUT,
                element_id=self.element_id,
                step_index=timestep_context.step_index,
                timestamp=timestep_context.current_time,
            ) from exc

        total_supply = 0.0
        from hydrology.graph_nodes import iter_catchment_items

        for name, catchment in iter_catchment_items(self.watershed.dg):
            supply = float(catchment.outflow(precip, et))
            self.watershed.update_capacity(name, supply)
            total_supply += supply

        solve_result = self._solver.solve(
            self.watershed.dg,
            self.watershed.source,
            self.watershed.sink,
            element_id=self.element_id,
        )
        self._last_solve = solve_result
        self._last_total_supply = total_supply
        self._last_outflow = solve_result.total_flow

        recorder = timestep_context.recorder
        if recorder is not None:
            recorder.record(f"{self.element_id}.outflow", self._last_outflow)
            recorder.record(f"{self.element_id}.total_supply", self._last_total_supply)

    def balance_terms(self, timestep_context: TimestepContext) -> list[MassBalanceTerm]:
        """Catchment supply should match routed outflow at the sink (± tolerance)."""
        prefix = self.element_id
        return [
            MassBalanceTerm(f"{prefix}.total_supply", self._last_total_supply),
            MassBalanceTerm(f"{prefix}.routed_outflow", -self._last_outflow),
        ]

    def finalize(self, run_context: RunContext) -> None:
        pass

    @property
    def last_solve(self) -> FlowSolveResult | None:
        return self._last_solve
