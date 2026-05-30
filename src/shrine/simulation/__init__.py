"""SHRINE simulation framework (``shrine.simulation``).

Stable public API
-----------------
Import framework types from this package only — do not rely on submodules
(``shrine.simulation.run_controller``, etc.) unless documented as extension points.

**Run orchestration:** :class:`Model`, :class:`RunController`, :class:`RunResult`,
:class:`StepResult`, :class:`ElementScheduler`

**Time and context:** :class:`Clock`, :class:`RunContext`, :class:`TimestepContext`

**Units:** :func:`shrine.units.get_unit_registry`, :func:`shrine.units.get_default_units` (injected on :class:`RunContext`)

**Elements:** :class:`Simulatable`, :class:`WatershedElement`, :class:`ReservoirElement`,
:class:`ClimateRecorderElement`, :class:`CatchmentElement`, :class:`StorageLike`, :class:`RegisteredElement`

**Inputs:** :class:`InputManager`, :class:`InputProvider`, :class:`ConstantInput`,
:class:`MonthlyLookupInput`, :class:`StochasticInput`, :class:`TimeSeriesCsvInput`,
:func:`load_csv_timeseries`, :func:`bind_csv_columns`

**Flow and balance:** :class:`FlowSolver`, :class:`NetworkXFlowSolver`, :class:`FlowSolveResult`,
:class:`MassBalanceCheck`, :class:`MassBalanceReport`, :class:`MassBalanceTerm`

**Outputs and scenarios:** :class:`Recorder`, :func:`export_run_result`, :func:`load_scenario_file`, :func:`run_scenario`,
:func:`run_scenarios`, :func:`load_and_run`, :class:`ScenarioConfig`

**Metadata and RNG:** :func:`build_run_metadata`, :func:`enrich_run_metadata`, :class:`RunTimer`,
:func:`make_rng`

**Errors:** :class:`SimulationError`, :class:`SimulationPhase`

See ``README.md`` (Public API section), ``docs/architecture.md``, and ``docs/api-stability.md``.
"""

from __future__ import annotations

from shrine import __version__ as __framework_version__
from shrine.simulation.adapters import (
    CatchmentElement,
    ReservoirElement,
    StorageElement,
    StorageLike,
    WatershedElement,
)
from shrine.simulation.balance import (
    MassBalanceCheck,
    MassBalanceReport,
    MassBalanceTerm,
)
from shrine.simulation.clock import Clock
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.deprecation import warn_api_deprecated
from shrine.simulation.elements import ClimateRecorderElement
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.export import export_run_result
from shrine.simulation.flow import FlowSolver, FlowSolveResult, NetworkXFlowSolver
from shrine.simulation.golden import outputs_content_hash
from shrine.simulation.import_csv import bind_csv_columns, load_csv_timeseries
from shrine.simulation.inputs import (
    ConstantInput,
    InputManager,
    InputProvider,
    MonthlyLookupInput,
    StochasticInput,
    TimeSeriesCsvInput,
)
from shrine.simulation.manifest import (
    attach_output_units,
    build_run_manifest,
    element_list_from_model,
    resolve_git_commit,
    scenario_content_hash,
)
from shrine.simulation.metadata import RunTimer, build_run_metadata, enrich_run_metadata
from shrine.simulation.model import Model, RegisteredElement
from shrine.simulation.protocols import Simulatable
from shrine.simulation.recorder import Recorder
from shrine.simulation.rng import make_rng
from shrine.simulation.run_controller import RunController, RunResult
from shrine.simulation.scenario import (
    ScenarioConfig,
    load_and_run,
    load_scenario_file,
    run_scenario,
    run_scenarios,
)
from shrine.simulation.scheduler import ElementScheduler
from shrine.simulation.session import RunSession
from shrine.simulation.step import StepResult
from shrine.simulation.version import API_VERSION as __api_version__
from shrine.units import get_default_units, get_unit_registry, validate_unit_string

__all__ = [
    # Version
    "__api_version__",
    "__framework_version__",
    # Run orchestration
    "Model",
    "RegisteredElement",
    "RunController",
    "RunResult",
    "RunSession",
    "StepResult",
    "ElementScheduler",
    # Time and context
    "Clock",
    "RunContext",
    "TimestepContext",
    "get_default_units",
    "get_unit_registry",
    "validate_unit_string",
    # Elements and adapters
    "Simulatable",
    "WatershedElement",
    "CatchmentElement",
    "ReservoirElement",
    "ClimateRecorderElement",
    "StorageElement",
    "StorageLike",
    # Inputs
    "InputManager",
    "InputProvider",
    "ConstantInput",
    "MonthlyLookupInput",
    "StochasticInput",
    "TimeSeriesCsvInput",
    "load_csv_timeseries",
    "bind_csv_columns",
    # Flow and mass balance
    "FlowSolver",
    "NetworkXFlowSolver",
    "FlowSolveResult",
    "MassBalanceCheck",
    "MassBalanceReport",
    "MassBalanceTerm",
    # Outputs and scenarios
    "Recorder",
    "export_run_result",
    "ScenarioConfig",
    "load_scenario_file",
    "run_scenario",
    "run_scenarios",
    "load_and_run",
    # Metadata, manifest, and RNG
    "build_run_metadata",
    "build_run_manifest",
    "attach_output_units",
    "enrich_run_metadata",
    "element_list_from_model",
    "resolve_git_commit",
    "scenario_content_hash",
    "outputs_content_hash",
    "RunTimer",
    "make_rng",
    # Deprecation
    "warn_api_deprecated",
    # Errors
    "SimulationError",
    "SimulationPhase",
]
