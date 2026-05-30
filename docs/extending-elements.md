# Extending the simulation framework with new elements

This guide explains how to add new domain behavior to **`shrine.simulation`** without editing framework internals (NFR-05). The intended pattern is a **thin adapter** around an existing class, or a small new class that implements the **`Simulatable`** lifecycle.

Related docs:

- [simulation-framework-requirements.md](simulation-framework-requirements.md) — requirements ELM-*, MB-*, FLW-*
- [results-recording.md](results-recording.md) — `Recorder` / `TimeHistory`
- [scenarios.md](scenarios.md) — YAML/JSON runs
- [step-debugging.md](step-debugging.md) — `RunController.step()`

---

## 1. Choose adapter vs new implementation

| Situation | Approach |
|-----------|----------|
| Legacy class already works (`Watershed`, `Store`, `Catchment`, …) | **Adapter** in `shrine/simulation/adapters/` that delegates to it |
| New physics or control logic | New element class implementing `Simulatable` |
| Graph-based routing | Domain object **owns** the NetworkX graph; adapter runs the flow solver (D2, TOP-02) |

Reference adapters (import from ``shrine.simulation``):

- `WatershedElement`, `CatchmentElement`, `ReservoirElement`, `StorageLike`
- `ClimateRecorderElement` in `shrine/simulation/elements.py`

For storage adapters, see [§14 `StorageLike` and reservoir overrides](#14-storagelike-and-reservoir-overrides). For a step-by-step **adapter** workflow, see [§15 Adapter authoring checklist](#15-adapter-authoring-checklist). For tests, see [§16 Testing checklist](#16-testing-checklist).

---

## 2. The `Simulatable` contract (ELM-01)

```python
from shrine.simulation.context import RunContext, TimestepContext

class MyElement:
    element_type = "my_element"  # short label for logs/metadata (ELM-03)

    def initialize(self, run_context: RunContext) -> None:
        """Once per run, before the first timestep."""

    def update(self, timestep_context: TimestepContext) -> None:
        """Once per timestep; do not advance the clock (ELM-02)."""

    def finalize(self, run_context: RunContext) -> None:
        """Optional post-run hook (ELM-04)."""
```

`Simulatable` is a `typing.Protocol` in `shrine/simulation/protocols.py`. You do not need to inherit from it; structural typing is enough.

Optional hooks (not on the protocol, but used by the framework when present):

| Method | Purpose |
|--------|---------|
| `balance_terms(timestep_context) -> list[MassBalanceTerm]` | Mass balance check at end of timestep (MB-01) |
| `element_id` attribute | Used in errors and output names (adapters set this explicitly) |

---

## 3. Timestep loop (what the framework does)

Each timestep (§7.0 in the requirements doc):

1. **Inputs** — `InputManager` fills `timestep_context.inputs`
2. **Update** — each registered element’s `update()` in registration order (`ElementScheduler`)
3. **Mass balance** — for elements with `balance_terms`, terms are summed and checked
4. **Record** — elements write via `timestep_context.recorder` (if they choose)
5. **Advance clock** — only `RunController` advances time

Your element must **not** call `clock.advance()` or mutate the global clock.

---

## 4. Context objects

### `RunContext` (whole run)

Available in `initialize` / `finalize`:

| Field | Use |
|-------|-----|
| `model_id` | Model name |
| `clock` | Authoritative simulation clock |
| `recorder` | Register output variables in `initialize` |
| `rng` | Seeded `numpy.random.Generator` when `RunController(seed=…)` |
| `seed`, `scenario_name`, `metadata` | Run provenance |
| `units_registry` | Shared pint `UnitRegistry` (from `shrine_units.json` / optional `.txt` defs) |
| `default_units` | Default unit strings per dimension (`time`, `length`, …) from `src/data/shrine_units.json` |

Loaded once per process via `shrine.units.get_unit_registry()` / `get_default_units()`; `RunController` injects them when building `RunContext`. Use these in adapters that emit or convert physical quantities instead of creating a local registry.

### `TimestepContext` (one step)

Available in `update` (and `balance_terms`):

| Field | Use |
|-------|-----|
| `step_index` | 0-based step counter |
| `current_time` | `pandas.Timestamp` for this step |
| `dt` | `Timedelta` step length |
| `inputs` | Named values from `InputManager` |
| `recorder` | Record outputs for this timestep |
| `rng` | Same generator as the run |
| `units_registry`, `default_units` | Same as the run (`run.units_registry`, `run.default_units`) |

When `RunController(strict_units=True)`, every `recorder.record` must have unit metadata (`register(..., unit=)`, `record(..., unit=)`, or a pint `Quantity` value). Bare floats without metadata raise `SimulationError` (`phase=record`).

Read inputs by key (agree on names with scenario files and `InputManager.bind`):

```python
def update(self, timestep_context: TimestepContext) -> None:
    demand = float(timestep_context.inputs.get("demand", 0.0))
```

Missing required inputs should raise **`SimulationError`** with `phase=SimulationPhase.INPUT` (see watershed adapter).

---

## 5. Inputs (ELM-06)

Do **not** read Excel, CSV, or monthly tables inside the element. Bind inputs on the controller:

```python
from shrine.simulation import ConstantInput, InputManager, MonthlyLookupInput

inputs = InputManager()
inputs.bind("demand", ConstantInput(5.0))
# or MonthlyLookupInput({...}), StochasticInput(...), scenario YAML, etc.

RunController(model, input_manager=inputs, seed=42).run()
```

Interpolation, monthly lookup, and stochastic draws live in **`shrine/simulation/inputs.py`**.

---

## 6. Recording outputs (OUT-01–03)

Register variables once; record each timestep:

```python
def initialize(self, run_context: RunContext) -> None:
    recorder = run_context.recorder
    if recorder is not None:
        recorder.register(f"{self.element_id}.storage", unit="m3")
        recorder.register(f"{self.element_id}.outflow", unit="m3/s")

def update(self, timestep_context: TimestepContext) -> None:
    # ... update domain state ...
    recorder = timestep_context.recorder
    if recorder is not None:
        recorder.record(f"{self.element_id}.storage", self.storage)
        recorder.record(f"{self.element_id}.outflow", self.outflow)
```

After `run()`, results are in `result.outputs` (wide DataFrame). Legacy plotting: `TimeHistory.from_run_result(result)` — see [results-recording.md](results-recording.md).

Use a consistent **`element_id` prefix** so multi-element models stay namespaced (`basin.outflow`, `res1.storage`).

---

## 7. Mass balance (MB-01–03)

Implement `balance_terms` so the framework can verify closure each timestep:

```python
from shrine.simulation.balance import MassBalanceTerm

def balance_terms(self, timestep_context: TimestepContext) -> list[MassBalanceTerm]:
    return [
        MassBalanceTerm(f"{self.element_id}.inflow", self._last_inflow),
        MassBalanceTerm(f"{self.element_id}.outflow", -self._last_outflow),
        MassBalanceTerm(f"{self.element_id}.storage_delta", -(self.storage - self._volume_before)),
    ]
```

Convention: terms **sum to zero** when balanced. Use negative signs for outflows and storage increases that reduce the residual.

Disable checks for exploratory runs: `RunController(model, verify_mass_balance=False)`.

---

## 8. Network / flow elements (ELM-07, FLW-01)

If your element owns a directed graph (like `hydrology.watershed.Watershed`):

1. In `update`, apply local physics (e.g. catchment runoff → node supplies).
2. Call a **`FlowSolver`** (`NetworkXFlowSolver` in `shrine/simulation/flow.py`) on **your** graph.
3. Apply solved edge flows back to domain objects.
4. Expose balance terms comparing total supply vs routed outflow.

Do **not** pass flow scalars directly into downstream elements’ `update` methods; routing goes through the solver (D3).

On solver failure, raise `SimulationError` with `phase=SimulationPhase.FLOW_SOLVE` and `details` from `FlowSolveResult` (see `WatershedElement`).

---

## 9. Register on the model

```python
from shrine.simulation import Clock, Model, RunController

model = Model(name="MyProject", clock=Clock("1/1/2019", "12/31/2019"))
model.register("pump1", MyElement(element_id="pump1"))
model.register_watershed("basin", WatershedElement(ws, element_id="basin"))  # tags kind=watershed

model.validate()  # duplicate ids, empty model, etc.
result = RunController(model, input_manager=inputs).run()
```

- **`register(element_id, element)`** — unique string id (MDL-02).
- **`register_watershed(...)`** — same as `register` with `metadata["kind"] = "watershed"` for filtering.
- **`register_catchment(...)`** — same with `metadata["kind"] = "catchment"` for standalone hillslope runoff.
- **`register_reservoir(...)`** — same with `metadata["kind"] = "reservoir"` for local storage (`ReservoirElement`).

Scenario **overrides** can set element attributes before a run (`ScenarioConfig.overrides`); reservoir elements use a fixed allowlist — see [§14](#14-storagelike-and-reservoir-overrides) and [scenarios.md](scenarios.md).

---

## 10. Execution order (TOP-01)

`ElementScheduler` runs elements in **registration order** (v1). If element B depends on A’s outputs at the same timestep, register A first.

Future versions may add explicit dependencies; avoid hidden cross-element mutable globals.

---

## 11. Errors (D6, RUN-07)

Raise **`SimulationError`** with a clear `phase` and context:

```python
from shrine.simulation.errors import SimulationError, SimulationPhase

raise SimulationError(
    message="Release exceeds storage",
    phase=SimulationPhase.UPDATE,
    element_id=self.element_id,
    step_index=timestep_context.step_index,
    timestamp=timestep_context.current_time,
    details={"storage": self.storage, "release": release},
)
```

Unexpected exceptions in `update` are wrapped as `SimulationError` with `phase=UPDATE`. Prefer raising `SimulationError` yourself for domain failures.

---

## 12. Minimal custom element (copy-paste starter)

```python
from shrine.simulation.context import RunContext, TimestepContext

class DemandElement:
    """Applies a demand taken from bound inputs; records applied demand."""

    element_type = "demand"

    def __init__(self, element_id: str = "demand") -> None:
        self.element_id = element_id
        self.applied = 0.0

    def initialize(self, run_context: RunContext) -> None:
        if run_context.recorder is not None:
            run_context.recorder.register(f"{self.element_id}.applied")

    def update(self, timestep_context: TimestepContext) -> None:
        self.applied = float(timestep_context.inputs.get("demand", 0.0))
        if timestep_context.recorder is not None:
            timestep_context.recorder.record(f"{self.element_id}.applied", self.applied)

    def finalize(self, run_context: RunContext) -> None:
        pass
```

Wire-up:

```python
model.register("d1", DemandElement("d1"))
inputs = InputManager()
inputs.bind("demand", ConstantInput(3.0))
RunController(model, input_manager=inputs).run()
```

Working example script: `examples/custom_element.py`.

---

## 13. Where to put code

| Piece | Location |
|-------|----------|
| Reusable adapter for existing SHRINE class | `shrine/simulation/adapters/<name>.py`, export in `adapters/__init__.py` |
| Built-in / tutorial element | `shrine/simulation/elements.py` or project `examples/` |
| Project-specific element | Your package or script; register on `Model` |

Keep adapters **thin**: translate context ↔ legacy API, raise structured errors, register outputs.

---

## 14. `StorageLike` and reservoir overrides

Canonical protocol: **`water_manage.protocols.StorageElement`** (import as `StorageLike` from `shrine.simulation`).

`ReservoirElement` (`shrine/simulation/adapters/reservoir.py`) wraps any object that satisfies **`StorageElement`**: a structural protocol (no inheritance required) with writable `inflow` / `request`, readable `quantity` / `outflow` / `overflow`, and a no-arg `update()` that applies the current inflow and request.

Production storage uses `water_manage.store.Store`. Tests often use `tests.conftest.SimpleStore`, which implements the same surface.

### 14.1 Timestep contract

Each timestep the adapter:

1. Reads `timestep_context.inputs[inflow_key]` (default `inflow`).
2. Reads `timestep_context.inputs[release_key]` when `release_key` is set (default `release`), else uses `default_release`.
3. Assigns `store.inflow` and `store.request`, then calls `store.update()` with no arguments.
4. Records `store.quantity` and `store.outflow` and builds mass-balance terms from inflow, outflow, overflow, and Δstorage.

Custom storage backends must follow that contract; do not call `update(inflow, request)` from the adapter — set attributes first, then call `update()`.

### 14.2 Scenario overrides (SCN-01)

For registered `ReservoirElement` instances, `ScenarioConfig.apply_element_overrides` only accepts these keys (unknown keys raise `SimulationError` at validate phase):

| Target | Keys |
|--------|------|
| Element | `default_release`, `inflow_key`, `release_key` |
| `element.store` | `capacity`, `quantity` |

Example:

```yaml
overrides:
  res1:
    default_release: 5.0
    capacity: 1.0e6
```

Constants live in `RESERVOIR_ELEMENT_OVERRIDE_KEYS` and `STORAGE_OVERRIDE_KEYS` in `reservoir.py`. Other element types still use generic `hasattr` / `setattr` override logic.

### 14.3 Implementing a new `StorageLike` backend

- Expose `inflow`, `request`, `outflow`, `overflow` as attributes.
- Provide `quantity` (property or attribute) readable after `update()`.
- Implement `update()` to apply the current `inflow` and `request` to internal state.
- If scenarios should override bounds or initial state, add settable `capacity` and `quantity` (see `Store` in `water_manage/store.py`).

---

## 15. Adapter authoring checklist

Use this **before and while** you add an adapter. It complements [§16 Testing checklist](#16-testing-checklist) (run after the adapter exists).

### 15.1 Pre-flight (decide before coding)

| Question | Guidance |
|----------|----------|
| Does legacy code already do the physics? | **Yes** → adapter. **No** → new `Simulatable` ([§12](#12-minimal-custom-element-copy-paste-starter)). |
| Does the domain object **own a NetworkX graph**? | **Yes** → follow `WatershedElement` ([§8](#8-network-flow-elements-elm-07-flw-01)); call `FlowSolver` in `update`. |
| Is it **local** runoff/storage with no routing? | **Yes** → follow `CatchmentElement` or `ReservoirElement`; no flow solver in the adapter. |
| What are the **input keys**? | Match scenario YAML and `InputManager.bind` (e.g. `precipitation`, `evaporation`, `inflow`, `release`). Document defaults in the constructor. |
| What **outputs** must be recorded? | List `{element_id}.variable` names; register in `initialize`, record in `update`. |
| Should **mass balance** run? | Storage and routing elements: implement `balance_terms`. Pure recorders or pass-through: optional. |
| Where does the class live? | `src/shrine/simulation/adapters/<name>.py`; export from `adapters/__init__.py` and `shrine.simulation` `__all__`. |

Reference implementations:

| Adapter | Legacy type | Graph? | Typical inputs | Recorded outputs |
|---------|-------------|--------|----------------|------------------|
| `WatershedElement` | `hydrology.watershed.Watershed` | Yes | `precipitation`, `evaporation` | `{id}.outflow`, `{id}.total_supply` |
| `CatchmentElement` | `hydrology.catchment.Catchment` | No | `precipitation`, `evaporation` | `{id}.outflow` |
| `ReservoirElement` | `water_manage.store.Store` (via `StorageLike`) | No | `inflow`, `release` (optional) | `{id}.storage`, `{id}.outflow` |

### 15.2 Implementation checklist

Copy an existing adapter file and tick through:

- [ ] **`element_type`** — short string for logs/metadata (e.g. `"catchment"`, `"watershed"`).
- [ ] **`element_id`** — constructor argument; prefix for all recorder keys and errors.
- [ ] **Domain import** — use `TYPE_CHECKING` for types; lazy-import legacy class in `__init__` when building a default instance.
- [ ] **`initialize`** — `recorder.register(f"{element_id}.…")` for every column you will record (optional `unit=` when known).
- [ ] **`update`** — read `timestep_context.inputs` only; **do not** read files or advance `clock`.
- [ ] **Missing inputs** — catch `KeyError` (or validate keys) and raise `SimulationError` with `phase=SimulationPhase.INPUT`, `element_id`, `step_index`, `timestamp` (see `WatershedElement` / `CatchmentElement`).
- [ ] **Delegate** — call legacy methods (`outflow`, `update`, graph + solver); keep physics in domain code, not in the adapter.
- [ ] **Record** — `recorder.record(...)` after domain state is updated; guard with `if recorder is not None`.
- [ ] **`balance_terms`** — return `list[MassBalanceTerm]` that sum to ~0 when balanced; store `_last_*` floats during `update` for terms.
- [ ] **`finalize`** — `pass` unless domain needs teardown.
- [ ] **Public API** — add to `adapters/__init__.py` `__all__` and `shrine/simulation/__init__.py` `__all__` (stable API).
- [ ] **Model helper** (optional) — `register_watershed` / `register_catchment` / `register_reservoir` if the kind filter helps callers.

### 15.3 Adapter skeleton

```python
"""Adapter: legacy MyDomain → Simulatable."""

from __future__ import annotations

from typing import TYPE_CHECKING

from shrine.simulation.balance import MassBalanceTerm
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.errors import SimulationError, SimulationPhase

if TYPE_CHECKING:
    from mydomain import MyDomain


class MyDomainElement:
    element_type = "my_domain"

    def __init__(
        self,
        domain: MyDomain | None = None,
        *,
        element_id: str = "my_domain",
        forcing_key: str = "forcing",
    ) -> None:
        if domain is None:
            from mydomain import MyDomain

            domain = MyDomain()
        self.domain = domain
        self.element_id = element_id
        self.forcing_key = forcing_key
        self._last_out = 0.0

    def initialize(self, run_context: RunContext) -> None:
        if run_context.recorder is not None:
            run_context.recorder.register(f"{self.element_id}.out")

    def update(self, timestep_context: TimestepContext) -> None:
        try:
            forcing = float(timestep_context.inputs[self.forcing_key])
        except KeyError as exc:
            raise SimulationError(
                message=f"Missing input: {exc}",
                phase=SimulationPhase.INPUT,
                element_id=self.element_id,
                step_index=timestep_context.step_index,
                timestamp=timestep_context.current_time,
            ) from exc
        self._last_out = self.domain.step(forcing)
        if timestep_context.recorder is not None:
            timestep_context.recorder.record(f"{self.element_id}.out", self._last_out)

    def balance_terms(self, timestep_context: TimestepContext) -> list[MassBalanceTerm]:
        return [MassBalanceTerm(f"{self.element_id}.out", self._last_out)]

    def finalize(self, run_context: RunContext) -> None:
        pass
```

Replace `balance_terms` / flow-solver blocks with the pattern from `WatershedElement` or `ReservoirElement` as needed.

### 15.4 Done when

- [ ] `tests/simulation/test_adapters.py` (or focused test module) covers run, outputs, missing input, and balance (if applicable).
- [ ] Optional: `examples/<name>_run.py` runnable headless after `pip install -e ".[dev]"`.
- [ ] README or this doc cross-link if the adapter is user-facing.

---

## 16. Testing checklist

1. **Unit test** the element with a short `Clock` and `RunController(..., raise_on_error=False)`.
2. Assert **outputs** in `result.outputs` or via `recorder.to_dataframe()`.
3. If `balance_terms` is implemented, test both passing and failing cases (`verify_mass_balance=True`).
4. For adapters, test against a **minimal domain fixture** (see `tests/conftest.py`, `tests/simulation/test_adapters.py`).
5. Add an **acceptance-style** test if the element satisfies a requirements AT-* item.

```python
def test_demand_element_records_input():
    model = Model(clock=Clock("1/1/2019", "1/3/2019"))
    model.register("d1", DemandElement("d1"))
    inputs = InputManager()
    inputs.bind("demand", ConstantInput(4.0))
    result = RunController(model, input_manager=inputs).run()
    assert result.outputs["d1.applied"].iloc[0] == 4.0
```

---

## 17. Publishing a third-party element (`shrine.elements`)

SHRINE discovers optional **`Simulatable`** implementations via the setuptools entry-point group **`shrine.elements`** (roadmap **4.1**). This lets other packages register elements without forking core or editing `Model` internals.

### 17.1 Register in your package

In your `pyproject.toml`:

```toml
[project.entry-points."shrine.elements"]
my_demand = "my_package.elements:DemandElement"
```

The target may be:

| Target | Use when |
|--------|----------|
| **Class** | Callers pass constructor args (`create_element_from_plugin("my_demand", element_id="d1")`) |
| **Factory callable** | You need custom wiring before returning a `Simulatable` instance |

Your class or factory **must** return an object that satisfies the [`Simulatable` contract (§2)](#2-the-simulatable-contract-elm-01) (`element_type`, `initialize`, `update`, `finalize`). Structural typing is enough — you do not need to inherit from `Simulatable`.

### 17.2 Load and register at runtime

```python
from shrine.simulation import Model, create_element_from_plugin, list_element_plugins

print(list_element_plugins())  # {'watershed': '...', 'my_demand': '...', ...}

model = Model()
model.register_plugin("d1", "my_demand", element_id="d1")
# equivalent:
model.register("d1", create_element_from_plugin("my_demand", element_id="d1"))
```

Framework helpers (stable API, `shrine.simulation.__api_version__` **1.1+**):

| Symbol | Purpose |
|--------|---------|
| `ELEMENTS_ENTRY_POINT_GROUP` | Group name (`"shrine.elements"`) |
| `list_element_plugins()` | `{name: entry_point_value}` for discovery / docs |
| `load_element_plugin(name)` | Load class or factory without constructing |
| `create_element_from_plugin(name, …)` | Construct and validate a `Simulatable` |
| `Model.register_plugin(id, name, …)` | Convenience wrapper around `register` |

Built-in SHRINE adapters are registered under the same group (`watershed`, `catchment`, `reservoir`, `climate_recorder`) so third-party tools can enumerate all available element types consistently.

Errors during discovery or construction raise **`SimulationError`** with `phase=validate` and `details` including the plugin name.

### 17.3 Distribution checklist

- [ ] Element implements `Simulatable` and is covered by tests in **your** package
- [ ] Entry point name is stable and documented (lowercase, underscores)
- [ ] Constructor kwargs are documented (`element_id`, input key overrides, etc.)
- [ ] License compatible with MIT ecosystem (see [ADR-0004](adr/0004-mit-license.md))
- [ ] Optional: scaffold from [shrine-element-cookiecutter](../shrine-element-cookiecutter/) ([cookiecutter guide](cookiecutter-element.md))

---

## 18. Debugging

- **Step mode:** `controller.reset()` then `controller.step()` in a loop — see [step-debugging.md](step-debugging.md).
- **Scenarios:** run from JSON/YAML — [scenarios.md](scenarios.md).
- **Solver / balance failures:** read `SimulationError.phase`, `element_id`, `step_index`, and `details`.

---

## 19. Checklist before opening a PR

- [ ] Adapter followed [§15](#15-adapter-authoring-checklist) (if wrapping legacy code)
- [ ] Reservoir/storage: `StorageLike` contract and override keys documented if applicable ([§14](#14-storagelike-and-reservoir-overrides))
- [ ] Implements `initialize` / `update` (and `finalize` if needed)
- [ ] Does not advance the clock inside `update`
- [ ] Reads forcing via `timestep_context.inputs`, not ad hoc files
- [ ] Registers and records outputs with `{element_id}.variable` names
- [ ] Raises `SimulationError` with phase + element id for expected failures
- [ ] `balance_terms` provided if the element participates in storage/routing balance
- [ ] Graph routing uses `FlowSolver`, not manual downstream arguments (if applicable)
- [ ] Tests added under `tests/simulation/` or `tests/results/`
- [ ] Example or doc cross-link if the element is user-facing
