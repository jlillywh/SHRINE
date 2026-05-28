"""Scenario configuration from YAML/JSON (SCN-01–03)."""

from __future__ import annotations

import calendar
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

import pandas as pd

from shrine.simulation.clock import Clock
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.inputs import (
    ConstantInput,
    InputManager,
    InputProvider,
    MonthlyLookupInput,
    StochasticInput,
)
from shrine.simulation.metadata import enrich_run_metadata
from shrine.simulation.manifest import scenario_content_hash
from shrine.simulation.adapters.reservoir import (
    ReservoirElement,
    apply_reservoir_element_override,
)
from shrine.simulation.model import Model
from shrine.units import validate_unit_string

if TYPE_CHECKING:
    from shrine.simulation.run_controller import RunResult

_TOP_LEVEL_KEYS = frozenset({"name", "seed", "clock", "inputs", "overrides", "metadata"})
_CLOCK_KEYS = frozenset({"start_date", "end_date", "time_step", "duration"})
_INPUT_KEYS_BY_TYPE: dict[str, frozenset[str]] = {
    "constant": frozenset({"type", "value", "unit"}),
    "monthly": frozenset({"type", "values", "unit"}),
    "stochastic": frozenset({"type", "distribution", "loc", "scale", "low", "high", "unit"}),
}
_STOCHASTIC_DISTRIBUTIONS = frozenset({"normal", "uniform"})
_VALID_MONTHS = frozenset(calendar.month_name[1:])


def _validate_unknown_keys(
    data: dict[str, Any],
    allowed: frozenset[str],
    *,
    section: str,
) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise SimulationError(
            message=f"Unknown keys in {section}: {unknown}",
            phase=SimulationPhase.VALIDATE,
            details={"section": section, "unknown_keys": unknown},
        )


def _validate_timedelta(value: Any, *, field: str) -> None:
    try:
        pd.Timedelta(value)
    except (TypeError, ValueError) as exc:
        raise SimulationError(
            message=f"Invalid duration in {field}: {value!r}",
            phase=SimulationPhase.VALIDATE,
            details={"field": field, "value": value},
        ) from exc


def _validate_unit(unit: Any, *, field: str) -> None:
    validate_unit_string(unit, field=field, phase=SimulationPhase.VALIDATE)


def _validate_clock(clock: dict[str, Any]) -> None:
    _validate_unknown_keys(clock, _CLOCK_KEYS, section="clock")
    if "time_step" in clock:
        _validate_timedelta(clock["time_step"], field="clock.time_step")
    if "duration" in clock:
        _validate_timedelta(clock["duration"], field="clock.duration")


def _validate_input_spec(spec: dict[str, Any], *, input_name: str) -> None:
    kind = str(spec.get("type", "constant"))
    allowed = _INPUT_KEYS_BY_TYPE.get(kind)
    if allowed is None:
        raise SimulationError(
            message=f"Input {input_name!r}: unknown type {kind!r}",
            phase=SimulationPhase.VALIDATE,
            details={"input": input_name, "type": kind},
        )
    _validate_unknown_keys(spec, allowed, section=f"inputs.{input_name}")
    if "unit" in spec:
        _validate_unit(spec["unit"], field=f"inputs.{input_name}.unit")
    if kind == "monthly":
        values = spec.get("values")
        if isinstance(values, dict):
            unknown_months = sorted(set(values) - _VALID_MONTHS)
            if unknown_months:
                raise SimulationError(
                    message=(
                        f"Input {input_name!r}: unknown month names in 'values': "
                        f"{unknown_months}"
                    ),
                    phase=SimulationPhase.VALIDATE,
                    details={"input": input_name, "unknown_months": unknown_months},
                )
    if kind == "stochastic":
        distribution = str(spec.get("distribution", "normal"))
        if distribution not in _STOCHASTIC_DISTRIBUTIONS:
            raise SimulationError(
                message=(
                    f"Input {input_name!r}: unknown distribution {distribution!r} "
                    f"(allowed: {sorted(_STOCHASTIC_DISTRIBUTIONS)})"
                ),
                phase=SimulationPhase.VALIDATE,
                details={"input": input_name, "distribution": distribution},
            )


def _validate_inputs(inputs: dict[str, Any]) -> None:
    for name, spec in inputs.items():
        if isinstance(spec, dict):
            _validate_input_spec(spec, input_name=name)


def _validate_overrides(overrides: dict[str, Any]) -> None:
    for element_id, params in overrides.items():
        if not isinstance(params, dict):
            raise SimulationError(
                message=f"Override for {element_id!r} must be a mapping",
                phase=SimulationPhase.VALIDATE,
                element_id=str(element_id),
            )


def _validate_scenario_dict(data: dict[str, Any]) -> None:
    _validate_unknown_keys(data, _TOP_LEVEL_KEYS, section="scenario")
    clock = data.get("clock") or {}
    if isinstance(clock, dict) and clock:
        _validate_clock(clock)
    inputs = data.get("inputs") or {}
    if isinstance(inputs, dict) and inputs:
        _validate_inputs(inputs)
    overrides = data.get("overrides") or {}
    if isinstance(overrides, dict) and overrides:
        _validate_overrides(overrides)
    meta = data.get("metadata")
    if meta is not None and not isinstance(meta, dict):
        raise SimulationError(
            message="'metadata' must be a mapping",
            phase=SimulationPhase.VALIDATE,
        )


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
        _validate_scenario_dict(data)
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
                if isinstance(element, ReservoirElement):
                    apply_reservoir_element_override(element, key, value)
                elif hasattr(element, key):
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
        if str(distribution) not in _STOCHASTIC_DISTRIBUTIONS:
            raise SimulationError(
                message=(
                    f"Input {input_name!r}: unknown distribution {distribution!r} "
                    f"(allowed: {sorted(_STOCHASTIC_DISTRIBUTIONS)})"
                ),
                phase=SimulationPhase.VALIDATE,
            )
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
    scenario.metadata["content_hash"] = scenario_content_hash(scenario)
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
    from shrine.simulation.run_controller import RunController

    scenario.apply_to_model(model)
    inputs = input_manager or scenario.build_input_manager()
    controller = RunController(
        model,
        input_manager=inputs,
        scenario_name=scenario.name,
        seed=scenario.seed,
        scenario=scenario,
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
