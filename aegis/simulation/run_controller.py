"""Simulation run loop (RUN-*, §7.0)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from aegis.simulation.balance import MassBalanceCheck
from aegis.simulation.context import RunContext, TimestepContext
from aegis.simulation.errors import SimulationError, SimulationPhase
from aegis.simulation.inputs import InputManager
from aegis.simulation.model import Model
from aegis.simulation.recorder import Recorder
from aegis.simulation.scheduler import ElementScheduler


@dataclass
class RunResult:
    """Outcome of a simulation run (RUN-03)."""

    success: bool
    outputs: pd.DataFrame
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: SimulationError | None = None


class RunController:
    """Executes a model over time.

    Timestep loop (Phase 1): inputs → element update (incl. flow solve) → mass balance → advance.
    """

    def __init__(
        self,
        model: Model,
        *,
        input_manager: InputManager | None = None,
        recorder: Recorder | None = None,
        scheduler: ElementScheduler | None = None,
        mass_balance: MassBalanceCheck | None = None,
        scenario_name: str | None = None,
        seed: int | None = None,
        raise_on_error: bool = True,
        verify_mass_balance: bool = True,
    ) -> None:
        self.model = model
        self.input_manager = input_manager or InputManager()
        self.recorder = recorder or Recorder(model.clock)
        self.scheduler = scheduler or ElementScheduler()
        self.mass_balance = mass_balance or MassBalanceCheck()
        self.scenario_name = scenario_name
        self.seed = seed
        self.raise_on_error = raise_on_error
        self.verify_mass_balance = verify_mass_balance
        self._run_context: RunContext | None = None
        self._initialized = False

    def run(self) -> RunResult:
        clock = self.model.clock
        warnings: list[str] = []
        metadata: dict[str, Any] = {
            "scenario_name": self.scenario_name,
            "seed": self.seed,
            "start": str(clock.start_date),
            "end": str(clock.end_date),
            "time_step": str(clock.time_step),
        }

        try:
            self._execute_run(metadata, warnings)
            return RunResult(
                success=True,
                outputs=self.recorder.to_dataframe(),
                warnings=warnings,
                metadata=metadata,
            )
        except SimulationError as err:
            result = RunResult(
                success=False,
                outputs=self.recorder.to_dataframe(),
                warnings=warnings,
                metadata=metadata,
                error=err,
            )
            if self.raise_on_error:
                raise
            return result
        finally:
            self._initialized = False
            self._run_context = None

    def _execute_run(self, metadata: dict[str, Any], warnings: list[str]) -> None:
        clock = self.model.clock
        self.model.validate()
        self._run_context = RunContext(
            model_id=self.model.name,
            clock=clock,
            scenario_name=self.scenario_name,
            seed=self.seed,
            metadata=metadata,
            recorder=self.recorder,
        )
        clock.reset()
        self.recorder.reset()
        self._initialized = False

        for registered in self.scheduler.execution_order(self.model):
            registered.element.initialize(self._run_context)
        self._initialized = True

        while clock.running:
            self._run_one_timestep()

        for registered in self.scheduler.execution_order(self.model):
            registered.element.finalize(self._run_context)

    def _run_one_timestep(self) -> TimestepContext:
        if self._run_context is None:
            raise SimulationError(
                message="Run not initialized",
                phase=SimulationPhase.INITIALIZE,
            )
        clock = self.model.clock
        step_index = clock.step_index
        self.recorder.begin_timestep(clock.current_date)

        partial = TimestepContext(
            run=self._run_context,
            step_index=step_index,
            current_time=clock.current_date,
            dt=clock.time_step,
        )
        partial.inputs = self.input_manager.values_for_timestep(partial)

        for registered in self.scheduler.execution_order(self.model):
            try:
                registered.element.update(partial)
            except SimulationError:
                raise
            except Exception as exc:
                raise SimulationError(
                    message=str(exc),
                    phase=SimulationPhase.UPDATE,
                    element_id=registered.element_id,
                    step_index=step_index,
                    timestamp=clock.current_date,
                ) from exc

        if self.verify_mass_balance:
            self._verify_timestep_balance(partial)

        clock.advance()
        return partial

    def _verify_timestep_balance(self, timestep_context: TimestepContext) -> None:
        terms = []
        for registered in self.scheduler.execution_order(self.model):
            provider = registered.element
            if hasattr(provider, "balance_terms"):
                terms.extend(provider.balance_terms(timestep_context))
        if terms:
            self.mass_balance.verify_or_raise(
                terms,
                step_index=timestep_context.step_index,
                timestamp=timestep_context.current_time,
            )

    def step(self) -> TimestepContext | None:
        """Advance a single timestep (RUN-04); for debugging."""
        clock = self.model.clock
        if not self._initialized:
            self.model.validate()
            self._run_context = RunContext(
                model_id=self.model.name,
                clock=clock,
                scenario_name=self.scenario_name,
                seed=self.seed,
                recorder=self.recorder,
            )
            for registered in self.scheduler.execution_order(self.model):
                registered.element.initialize(self._run_context)
            self._initialized = True

        if not clock.running:
            return None

        return self._run_one_timestep()

    def finalize(self) -> None:
        """Call element finalize hooks (e.g. after partial stepping)."""
        if self._run_context is None:
            return
        for registered in self.scheduler.execution_order(self.model):
            registered.element.finalize(self._run_context)
        self._initialized = False
        self._run_context = None
