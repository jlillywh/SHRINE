"""Simulation run loop (RUN-*, §7.0)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

import pandas as pd

from shrine.simulation.balance import (
    MassBalanceCheck,
    MassBalanceReport,
    MassBalanceTerm,
)
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.inputs import InputManager
from shrine.simulation.manifest import attach_output_units, build_run_manifest
from shrine.simulation.metadata import RunTimer, build_run_metadata, enrich_run_metadata
from shrine.simulation.model import Model
from shrine.simulation.recorder import Recorder
from shrine.simulation.scheduler import ElementScheduler
from shrine.simulation.step import StepResult
from shrine.units import get_default_units, get_unit_registry

if TYPE_CHECKING:
    from shrine.simulation.scenario import ScenarioConfig
    from shrine.simulation.session import RunSession


@dataclass
class RunResult:
    """Outcome of a simulation run (RUN-03)."""

    success: bool
    outputs: pd.DataFrame
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    manifest: dict[str, Any] = field(default_factory=dict)
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
        scenario: ScenarioConfig | None = None,
        raise_on_error: bool = True,
        verify_mass_balance: bool = True,
        strict_units: bool = False,
    ) -> None:
        self.model = model
        self.input_manager = input_manager or InputManager()
        self.recorder = recorder or Recorder(
            model.clock,
            units_registry=get_unit_registry(),
            strict_units=strict_units,
        )
        self.scheduler = scheduler or ElementScheduler()
        self.mass_balance = mass_balance or MassBalanceCheck()
        self.scenario_name = scenario_name or (scenario.name if scenario else None)
        self.seed = seed if seed is not None else (scenario.seed if scenario else None)
        self.scenario = scenario
        self.raise_on_error = raise_on_error
        self.verify_mass_balance = verify_mass_balance
        self.strict_units = strict_units
        self._run_context: RunContext | None = None
        self._initialized = False
        self._last_step: StepResult | None = None
        self._step_count = 0
        self._run_started_at: str | None = None

    def session(self) -> RunSession:
        """Return a :class:`RunSession` for ``with controller.session():`` stepping."""
        from shrine.simulation.session import RunSession

        return RunSession(self)

    def run(self) -> RunResult:
        warnings: list[str] = []
        timer = RunTimer()
        started_at = datetime.now(timezone.utc).isoformat()
        self._run_started_at = started_at
        metadata = enrich_run_metadata(
            build_run_metadata(
                self.model,
                scenario_name=self.scenario_name,
                seed=self.seed,
            ),
            scenario=self.scenario,
        )
        metadata["started_at_utc"] = started_at

        try:
            self._execute_run(metadata, warnings)
            metadata = enrich_run_metadata(
                metadata,
                elapsed_seconds=timer.elapsed(),
                status="success",
            )
            metadata["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
            manifest = build_run_manifest(self.model, metadata, scenario=self.scenario)
            attach_output_units(manifest, self.recorder.units)
            metadata["manifest"] = manifest
            return RunResult(
                success=True,
                outputs=self.recorder.to_dataframe(),
                warnings=warnings,
                metadata=metadata,
                manifest=manifest,
            )
        except SimulationError as err:
            metadata = enrich_run_metadata(
                metadata,
                elapsed_seconds=timer.elapsed(),
                status="failed",
            )
            metadata["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
            manifest = build_run_manifest(self.model, metadata, scenario=self.scenario)
            attach_output_units(manifest, self.recorder.units)
            metadata["manifest"] = manifest
            result = RunResult(
                success=False,
                outputs=self.recorder.to_dataframe(),
                warnings=warnings,
                metadata=metadata,
                manifest=manifest,
                error=err,
            )
            if self.raise_on_error:
                raise
            return result
        finally:
            self._tear_down_run()

    @property
    def is_initialized(self) -> bool:
        """True after initialize hooks have run for the current session."""
        return self._initialized

    @property
    def is_running(self) -> bool:
        """True while the clock has timesteps remaining in the current session."""
        return self._initialized and self.model.clock.running

    @property
    def steps_completed(self) -> int:
        """Number of timesteps executed in the current session."""
        return self._step_count

    @property
    def last_step(self) -> StepResult | None:
        """Most recent ``step()`` result, if any."""
        return self._last_step

    def reset(self) -> None:
        """Reset clock, recorder, and session state for interactive stepping (RUN-04)."""
        self._tear_down_run()
        self.model.clock.reset()
        self.recorder.reset()
        self._last_step = None
        self._step_count = 0

    def begin(self) -> None:
        """Validate and run element ``initialize`` hooks without advancing time."""
        self.reset()
        self._begin_session(metadata=None)

    def step(self) -> StepResult | None:
        """Advance one timestep and return diagnostics; ``None`` when the run is finished."""
        if not self._initialized:
            self._begin_session(metadata=None)
        clock = self.model.clock
        if not clock.running:
            return None

        ctx, balance = self._run_one_timestep(collect_balance=True)

        result = StepResult(
            step_index=ctx.step_index,
            current_time=ctx.current_time,
            inputs=dict(ctx.inputs),
            timestep_context=ctx,
            balance=balance,
            done=not clock.running,
        )
        self._last_step = result
        return result

    def step_many(self, count: int) -> list[StepResult]:
        """Advance up to ``count`` timesteps; stops early if the clock finishes."""
        if count < 1:
            return []
        results: list[StepResult] = []
        for _ in range(count):
            result = self.step()
            if result is None:
                break
            results.append(result)
        return results

    def complete(self) -> RunResult:
        """Finalize a stepped session and return outputs (RUN-04)."""
        if self._run_context is not None:
            for registered in self.scheduler.execution_order(self.model):
                registered.element.finalize(self._run_context)
        finished_at = datetime.now(timezone.utc).isoformat()
        metadata = enrich_run_metadata(
            build_run_metadata(
                self.model,
                scenario_name=self.scenario_name,
                seed=self.seed,
            ),
            scenario=self.scenario,
            status="success",
        )
        metadata["started_at_utc"] = self._run_started_at or finished_at
        metadata["finished_at_utc"] = finished_at
        metadata["debug_mode"] = True
        metadata["steps_completed"] = self._step_count
        manifest = build_run_manifest(self.model, metadata, scenario=self.scenario)
        attach_output_units(manifest, self.recorder.units)
        metadata["manifest"] = manifest
        outputs = self.recorder.to_dataframe()
        self._tear_down_run()
        return RunResult(
            success=True,
            outputs=outputs,
            metadata=metadata,
            manifest=manifest,
        )

    def _tear_down_run(self) -> None:
        self._initialized = False
        self._run_context = None
        self._step_count = 0
        self._run_started_at = None

    def _begin_session(self, metadata: dict[str, Any] | None) -> None:
        if self._run_started_at is None:
            self._run_started_at = datetime.now(timezone.utc).isoformat()
        self.model.validate()
        self._run_context = RunContext(
            model_id=self.model.name,
            clock=self.model.clock,
            scenario_name=self.scenario_name,
            seed=self.seed,
            metadata=metadata or {},
            recorder=self.recorder,
            units_registry=get_unit_registry(),
            default_units=get_default_units(),
        )
        for registered in self.scheduler.execution_order(self.model):
            registered.element.initialize(self._run_context)
        self._initialized = True

    def _execute_run(self, metadata: dict[str, Any], warnings: list[str]) -> None:
        self.reset()
        self._begin_session(metadata)

        while self.model.clock.running:
            self._run_one_timestep()

        if self._run_context is not None:
            for registered in self.scheduler.execution_order(self.model):
                registered.element.finalize(self._run_context)

    def _run_one_timestep(
        self,
        *,
        collect_balance: bool = False,
    ) -> tuple[TimestepContext, MassBalanceReport | None]:
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

        balance_report: MassBalanceReport | None = None
        terms = self._collect_balance_terms(partial)
        if terms:
            balance_report = self.mass_balance.verify(terms)
            if self.verify_mass_balance and not balance_report.passed:
                raise SimulationError(
                    message=f"Mass balance violation: residual={balance_report.residual}",
                    phase=SimulationPhase.BALANCE,
                    step_index=partial.step_index,
                    timestamp=partial.current_time,
                    details={"terms": [(t.name, t.value) for t in terms]},
                )
        elif collect_balance:
            balance_report = None

        clock.advance()
        self._step_count += 1
        return partial, balance_report

    def _collect_balance_terms(self, timestep_context: TimestepContext) -> list[MassBalanceTerm]:
        terms: list[MassBalanceTerm] = []
        for registered in self.scheduler.execution_order(self.model):
            provider = registered.element
            if hasattr(provider, "balance_terms"):
                terms.extend(provider.balance_terms(timestep_context))
        return terms

    def finalize(self) -> None:
        """Call element finalize hooks without building a ``RunResult``."""
        if self._run_context is None:
            return
        for registered in self.scheduler.execution_order(self.model):
            registered.element.finalize(self._run_context)
        self._tear_down_run()
