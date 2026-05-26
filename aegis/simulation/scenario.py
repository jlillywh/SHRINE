"""Scenario configuration from YAML/JSON (SCN-01–03)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

import pandas as pd

from aegis.simulation.clock import Clock
from aegis.simulation.errors import SimulationError, SimulationPhase
from aegis.simulation.inputs import (
    ConstantInput,
    InputManager,
    InputProvider,
    MonthlyLookupInput,
    StochasticInput,
)
from aegis.simulation.metadata import enrich_run_metadata
from aegis.simulation.model import Model

if TYPE_CHECKING:
    from aegis.simulation.run_controller import RunResult


@dataclass
class ScenarioConfig:
    """Declarative scenario: clock, inputs, and optional element overrides."""

    name: str
    seed: int | None = None
    clock: dict[str, Any] = field(default_factory=dict)
    inputs: dict[str, Any] = field(default_factory=dict)
    overrides: dict[str, dict[str, Any]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ScenarioConfig:
        if not isinstance(data, dict):
            raise SimulationError(
                message="Scenario file must contain a mapping at the top level",
                phase=SimulationPhase.VALIDATE,
            )
        name = data.get("name")
        if not name:
            raise SimulationError(
                message="Scenario requires a 'name' field",
                phase=SimulationPhase.VALIDATE,
            )
        clock = data.get("clock") or {}
        if not isinstance(clock, dict):
            raise SimulationError(
                message="'clock' must be a mapping",
                phase=SimulationPhase.VALIDATE,
            )
        inputs = data.get("inputs") or {}
        if not isinstance(inputs, dict):
            raise SimulationError(
                message="'inputs' must be a mapping",
                phase=SimulationPhase.VALIDATE,
            )
        overrides = data.get("overrides") or {}
        if not isinstance(overrides, dict):
            raise SimulationError(
                message="'overrides' must be a mapping",
                phase=SimulationPhase.VALIDATE,
            )
        seed = data.get("seed")
        meta = data.get("metadata") or {}
        if not isinstance(meta, dict):
            raise SimulationError(
                message="'metadata' must be a mapping",
                phase=SimulationPhase.VALIDATE,
            )
        return cls(
            name=str(name),
            seed=int(seed) if seed is not None else None,
            clock=dict(clock),
            inputs=dict(inputs),
            overrides={str(k): dict(v) for k, v in overrides.items()},
            metadata=dict(meta),
        )

    def apply_clock(self, clock: Clock) -> None:
        """Apply clock fields from the scenario onto an existing clock."""
        if not self.clock:
            return
        if "time_step" in self.clock:
            clock.time_step = pd.Timedelta(self.clock["time_step"])
        if "start_date" in self.clock:
            clock.set_start_date(self.clock["start_date"])
        if "end_date" in self.clock:
            clock.end_date = pd.Timestamp(self.clock["end_date"])
            clock.duration = clock.end_date - clock.start_date
            clock.remaining_time = clock.duration
            clock.range = pd.date_range(start=clock.start_date, end=clock.end_date)
        if "duration" in self.clock and "start_date" in self.clock:
            clock.set_duration(self.clock["duration"])

    def apply_element_overrides(self, model: Model) -> None:
        """Set attributes on registered elements (SCN-01 parameter overrides)."""
        for element_id, params in self.overrides.items():
            try:
                element = model.get(element_id)
            except SimulationError as exc:
                raise SimulationError(
                    message=f"Override targets unknown element {element_id!r}",
                    phase=SimulationPhase.VALIDATE,
                    element_id=element_id,
                ) from exc
            for key, value in params.items():
                if hasattr(element, key):
                    setattr(element, key, value)
                elif hasattr(element, "store") and hasattr(element.store, key):
                    setattr(element.store, key, value)
                else:
                    raise SimulationError(
                        message=f"Element {element_id!r} has no attribute {key!r}",
                        phase=SimulationPhase.VALIDATE,
                        element_id=element_id,
                    )

    def apply_to_model(self, model: Model) -> None:
        """Apply clock and element overrides to a model before a run."""
        self.apply_clock(model.clock)
        self.apply_element_overrides(model)

    def build_input_manager(self) -> InputManager:
        """Build input bindings from scenario input definitions."""
        manager = InputManager()
        for name, spec in self.inputs.items():
            manager.bind(name, parse_input_spec(spec, input_name=name))
        return manager


def parse_input_spec(spec: Any, *, input_name: str = "input") -> InputProvider:
    """Parse a scalar or typed input spec into an InputProvider."""
    if isinstance(spec, (int, float)):
        return ConstantInput(float(spec))
    if not isinstance(spec, dict):
        raise SimulationError(
            message=f"Input {input_name!r}: expected number or mapping, got {type(spec).__name__}",
            phase=SimulationPhase.VALIDATE,
        )
    kind = spec.get("type", "constant")
    if kind == "constant":
        if "value" not in spec:
            raise SimulationError(
                message=f"Input {input_name!r}: constant type requires 'value'",
                phase=SimulationPhase.VALIDATE,
            )
        return ConstantInput(float(spec["value"]))
    if kind == "monthly":
        values = spec.get("values")
        if not isinstance(values, dict) or not values:
            raise SimulationError(
                message=f"Input {input_name!r}: monthly type requires non-empty 'values'",
                phase=SimulationPhase.VALIDATE,
            )
        normalized = {str(month): float(v) for month, v in values.items()}
        return MonthlyLookupInput(normalized)
    if kind == "stochastic":
        distribution = spec.get("distribution", "normal")
        return StochasticInput(
            str(distribution),
            loc=float(spec.get("loc", 0.0)),
            scale=float(spec.get("scale", 1.0)),
            low=float(spec.get("low", 0.0)),
            high=float(spec.get("high", 1.0)),
        )
    raise SimulationError(
        message=f"Input {input_name!r}: unknown type {kind!r}",
        phase=SimulationPhase.VALIDATE,
    )


def load_scenario_file(path: str | Path) -> ScenarioConfig:
    """Load a scenario from a ``.json``, ``.yaml``, or ``.yml`` file."""
    path = Path(path)
    if not path.is_file():
        raise SimulationError(
            message=f"Scenario file not found: {path}",
            phase=SimulationPhase.VALIDATE,
        )
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(text)
    elif suffix in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as exc:
            raise SimulationError(
                message="PyYAML is required for YAML scenarios: pip install pyyaml",
                phase=SimulationPhase.VALIDATE,
            ) from exc
        data = yaml.safe_load(text)
    else:
        raise SimulationError(
            message=f"Unsupported scenario file type: {suffix}",
            phase=SimulationPhase.VALIDATE,
        )
    if data is None:
        raise SimulationError(
            message="Scenario file is empty",
            phase=SimulationPhase.VALIDATE,
        )
    scenario = ScenarioConfig.from_dict(data)
    scenario.metadata.setdefault("source_file", str(path))
    return scenario


def run_scenario(
    model: Model,
    scenario: ScenarioConfig,
    *,
    input_manager: InputManager | None = None,
    raise_on_error: bool = True,
    verify_mass_balance: bool = True,
) -> RunResult:
    """Apply scenario to a model and run once (SCN-01)."""
    from aegis.simulation.run_controller import RunController

    scenario.apply_to_model(model)
    inputs = input_manager or scenario.build_input_manager()
    controller = RunController(
        model,
        input_manager=inputs,
        scenario_name=scenario.name,
        seed=scenario.seed,
        raise_on_error=raise_on_error,
        verify_mass_balance=verify_mass_balance,
    )
    result = controller.run()
    result.metadata = enrich_run_metadata(result.metadata, scenario=scenario)
    return result


def run_scenarios(
    build_model: Callable[[], Model],
    scenarios: list[ScenarioConfig],
    *,
    raise_on_error: bool = True,
    verify_mass_balance: bool = True,
) -> list["RunResult"]:
    """Run multiple scenarios with isolated model instances (SCN-02)."""
    results: list[RunResult] = []
    for scenario in scenarios:
        model = build_model()
        results.append(
            run_scenario(
                model,
                scenario,
                raise_on_error=raise_on_error,
                verify_mass_balance=verify_mass_balance,
            )
        )
    return results


def load_and_run(
    build_model: Callable[[], Model],
    scenario_path: str | Path,
    **kwargs: Any,
) -> RunResult:
    """Convenience: load file and run a single scenario."""
    scenario = load_scenario_file(scenario_path)
    return run_scenario(build_model(), scenario, **kwargs)
