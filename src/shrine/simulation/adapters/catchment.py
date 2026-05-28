"""Adapter: legacy :class:`~hydrology.catchment.Catchment` → :class:`~shrine.simulation.protocols.Simulatable`."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from shrine.simulation.balance import MassBalanceTerm
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.errors import SimulationError, SimulationPhase

if TYPE_CHECKING:
    from hydrology.catchment import Catchment

RunoffMethodName = Literal["simple", "awbm"]


class CatchmentElement:
    """Single catchment runoff each timestep (rational or AWBM via legacy ``Catchment``).

    Unlike :class:`~shrine.simulation.adapters.watershed.WatershedElement`, this adapter
    does not own a flow network — it only computes local runoff from precip and ET inputs.
    """

    element_type = "catchment"

    def __init__(
        self,
        catchment: Catchment | None = None,
        *,
        element_id: str = "catchment",
        area: float = 1000.0,
        runoff_method: RunoffMethodName | str = "simple",
        precip_key: str = "precipitation",
        et_key: str = "evaporation",
    ) -> None:
        if catchment is None:
            from hydrology.catchment import Catchment

            catchment = Catchment(area=area, runoff_method=runoff_method)
        self.catchment = catchment
        self.element_id = element_id
        self.precip_key = precip_key
        self.et_key = et_key
        self._last_precip = 0.0
        self._last_et = 0.0
        self._last_outflow = 0.0
        self._last_moisture_in = 0.0
        self._last_internal_loss = 0.0

    def initialize(self, run_context: RunContext) -> None:
        recorder = run_context.recorder
        if recorder is not None:
            recorder.register(f"{self.element_id}.outflow")

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

        outflow = float(self.catchment.outflow(precip, et))
        moisture_in = max(0.0, precip - et) * float(self.catchment.area)
        loss_fraction = float(getattr(self.catchment.runoff_method, "loss", 0.0))
        internal_loss = moisture_in * loss_fraction

        self._last_precip = precip
        self._last_et = et
        self._last_outflow = outflow
        self._last_moisture_in = moisture_in
        self._last_internal_loss = internal_loss

        recorder = timestep_context.recorder
        if recorder is not None:
            recorder.record(f"{self.element_id}.outflow", outflow)

    def balance_terms(self, timestep_context: TimestepContext) -> list[MassBalanceTerm]:
        """Moisture surplus (P−ET)×area − internal loss − runoff outflow ≈ 0 (rational method)."""
        prefix = self.element_id
        return [
            MassBalanceTerm(f"{prefix}.moisture_in", self._last_moisture_in),
            MassBalanceTerm(f"{prefix}.internal_loss", -self._last_internal_loss),
            MassBalanceTerm(f"{prefix}.outflow", -self._last_outflow),
        ]

    def finalize(self, run_context: RunContext) -> None:
        pass
