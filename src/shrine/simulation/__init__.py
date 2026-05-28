"""SHRINE simulation framework (``shrine.simulation``).

Stable public API
-----------------
Import framework types from this package only — do not rely on submodules
(``shrine.simulation.run_controller``, etc.) unless documented as extension points.

**Run orchestration:** :class:`Model`, :class:`RunController`, :class:`RunResult`,
:class:`StepResult`, :class:`ElementScheduler`

**Time and context:** :class:`Clock`, :class:`RunContext`, :class:`TimestepContext`

**Elements:** :class:`Simulatable`, :class:`WatershedElement`, :class:`ReservoirElement`,
:class:`ClimateRecorderElement`, :class:`CatchmentElement`, :class:`StorageLike`, :class:`RegisteredElement`

**Inputs:** :class:`InputManager`, :class:`InputProvider`, :class:`ConstantInput`,
:class:`MonthlyLookupInput`, :class:`StochasticInput`

**Flow and balance:** :class:`FlowSolver`, :class:`NetworkXFlowSolver`, :class:`FlowSolveResult`,
:class:`MassBalanceCheck`, :class:`MassBalanceReport`, :class:`MassBalanceTerm`

**Outputs and scenarios:** :class:`Recorder`, :func:`load_scenario_file`, :func:`run_scenario`,
:func:`run_scenarios`, :func:`load_and_run`, :class:`ScenarioConfig`

**Metadata and RNG:** :func:`build_run_metadata`, :func:`enrich_run_metadata`, :class:`RunTimer`,
:func:`make_rng`

**Errors:** :class:`SimulationError`, :class:`SimulationPhase`

See ``README.md`` (Public API section), ``docs/architecture.md``, and ``docs/api-stability.md``.
"""

from __future__ import annotations

from shrine import __version__ as __framework_version__

from shrine.simulation.version import API_VERSION as __api_version__

from shrine.simulation.adapters import (
    CatchmentElement,
    ReservoirElement,
    StorageLike,
    WatershedElement,
)
from shrine.simulation.balance import MassBalanceCheck, MassBalanceReport, MassBalanceTerm
from shrine.simulation.clock import Clock
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.deprecation import warn_api_deprecated
from shrine.simulation.elements import ClimateRecorderElement
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.flow import FlowSolveResult, FlowSolver, NetworkXFlowSolver
from shrine.simulation.inputs import (
    ConstantInput,
    InputManager,
    InputProvider,
    MonthlyLookupInput,
    StochasticInput,
)
from shrine.simulation.metadata import RunTimer, build_run_metadata, enrich_run_metadata
from shrine.simulation.manifest import (
    build_run_manifest,
    element_list_from_model,
    resolve_git_commit,
    scenario_content_hash,
)
from shrine.simulation.model import Model, RegisteredElement
from shrine.simulation.protocols import Simulatable
from shrine.simulation.recorder import Recorder
from shrine.simulation.rng import make_rng
from shrine.simulation.run_controller import RunController, RunResult
from shrine.simulation.session import RunSession
from shrine.simulation.scenario import (
    ScenarioConfig,
    load_and_run,
    load_scenario_file,
    run_scenario,
    run_scenarios,
)
from shrine.simulation.scheduler import ElementScheduler
from shrine.simulation.step import StepResult

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
    # Elements and adapters
    "Simulatable",
    "WatershedElement",
    "CatchmentElement",
    "ReservoirElement",
    "ClimateRecorderElement",
    "StorageLike",
    # Inputs
    "InputManager",
    "InputProvider",
    "ConstantInput",
    "MonthlyLookupInput",
    "StochasticInput",
    # Flow and mass balance
    "FlowSolver",
    "NetworkXFlowSolver",
    "FlowSolveResult",
    "MassBalanceCheck",
    "MassBalanceReport",
    "MassBalanceTerm",
    # Outputs and scenarios
    "Recorder",
    "ScenarioConfig",
    "load_scenario_file",
    "run_scenario",
    "run_scenarios",
    "load_and_run",
    # Metadata, manifest, and RNG
    "build_run_metadata",
    "build_run_manifest",
    "enrich_run_metadata",
    "element_list_from_model",
    "resolve_git_commit",
    "scenario_content_hash",
    "RunTimer",
    "make_rng",
    # Deprecation
    "warn_api_deprecated",
    # Errors
    "SimulationError",
    "SimulationPhase",
]
