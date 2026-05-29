# Concepts

SHRINE separates **orchestration** (when things run, what inputs apply, how outputs are recorded) from **physics** (how catchments, reservoirs, and networks behave). New application code should use **`shrine.simulation`** for orchestration and call domain objects through **adapters**.

See [Architecture](architecture.md) for layered diagrams (framework, adapters, domain); this page is the concise mental model.

## Three layers

| Layer | Package | Role |
|-------|---------|------|
| **Framework** | `shrine.simulation` | Clock, run loop, inputs, recording, flow dispatch, mass balance, scenarios |
| **Adapters** | `shrine.simulation.adapters` | Thin `Simulatable` wrappers that translate framework context ↔ domain API |
| **Domain** | `hydrology`, `water_manage`, `inputs`, … | Catchments, networks, storage, tables, legacy helpers |

Only **`RunController`** advances time. Domain code does not own the global simulation clock unless you are running a legacy script directly.

## Model and elements

A **`Model`** holds a shared **`Clock`** and a registry of **elements**. Each element implements **`Simulatable`**:

| Phase | Method | Purpose |
|-------|--------|---------|
| Setup | `initialize(run_context)` | One-time setup before the first timestep |
| Loop | `update(timestep_context)` | Called once per timestep, in registration order |
| Teardown | `finalize(run_context)` | Cleanup after the last timestep |

Built-in adapters include **`WatershedElement`**, **`ReservoirElement`**, **`CatchmentElement`**, and **`ClimateRecorderElement`**. Register them on the model:

```python
model.register("basin", WatershedElement(watershed, element_id="basin"))
# or convenience helpers:
model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
```

Custom elements are documented in [Extending elements](extending-elements.md).

## Run lifecycle

**`RunController`** drives the standard lifecycle:

1. **Validate** — clock, element graph, input bindings, scenario overrides
2. **Initialize** — call `initialize()` on each element; build run metadata
3. **Timestep loop** — for each clock step: bind inputs → `update()` each element → mass balance → record
4. **Finalize** — call `finalize()` on each element; attach manifest to `RunResult`

The result is a **`RunResult`** with `success`, `outputs` (`Recorder` DataFrame), `metadata`, and `manifest` (provenance for reproducibility).

Use **`RunController.step()`** for interactive debugging — see [Step debugging](step-debugging.md).

## Time and context

| Object | Scope | Contains |
|--------|-------|----------|
| **`Clock`** | Whole run | Start, end, timestep duration |
| **`RunContext`** | Whole run | Model id, clock, seed, RNG, unit registry, recorder |
| **`TimestepContext`** | One step | Current time, step index, bound inputs |

Elements receive **`TimestepContext`** in `update()` so they can read inputs and write to the recorder without touching global state.

## Inputs

**`InputManager`** binds named providers to the run. Providers implement **`InputProvider`**:

| Provider | Use case |
|----------|----------|
| **`ConstantInput`** | Fixed value every timestep |
| **`MonthlyLookupInput`** | Month-name → value lookup |
| **`StochasticInput`** | Random draws (seeded via `RunContext.rng`) |

Scenario files declare inputs declaratively — see [Scenarios](scenarios.md). At runtime the controller resolves them through the same provider types.

## Flow solve and mass balance

Watershed adapters own a **NetworkX** graph. The framework **`FlowSolver`** (default **`NetworkXFlowSolver`**) computes flows on that graph each timestep.

**`MassBalanceCheck`** verifies conservation terms reported by elements. Failures raise **`SimulationError`** with structured phase and details — the controller can fail fast or collect errors depending on configuration.

## Scenarios

A **scenario** separates *run settings* from *model topology*:

- **In Python** — elements, catchments, junctions, reservoirs
- **In YAML/JSON** — clock, seed, inputs, per-element parameter overrides

```bash
python examples/run_from_scenario.py scenarios/baseline_watershed.json
```

Loader functions: `load_scenario_file`, `run_scenario`, `load_and_run`.

## Outputs and recording

**`Recorder`** accumulates a wide DataFrame during the run. Column names follow `{element_id}.{variable}` convention. For analysis helpers built on legacy code, see [Results & recording](results-recording.md).

## Units

SHRINE uses **pint** for unit validation at scenario load and exposes a shared registry on **`RunContext`**. Default unit strings ship in `src/data/shrine_units.json`.

## Public API policy

Import from **`shrine.simulation`** only for stable symbols. Submodule paths may change; see [API stability](api-stability.md) and the [API reference](api/index.md).

## Next steps

- [Quickstart](quickstart.md) — hands-on first run
- [Extending elements](extending-elements.md) — add a custom element
- [API reference: shrine.simulation](api/simulation.md) — full symbol list
