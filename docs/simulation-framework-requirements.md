# Aegis Simulation Framework — Requirements (Draft)

**Status:** Draft — architecture decisions recorded  
**Author:** Jason  
**Last updated:** 2026-05-25  
**Scope:** Simulation engine only (not web UI, not full hydrology/hydraulics physics specs)

---

## 1. Purpose

Define requirements for the **Aegis simulation framework**: the layer that advances time, binds components into a model, supplies inputs, records outputs, and runs repeatable experiments. Physics modules (catchments, reservoirs, pipes, etc.) remain separate; the framework orchestrates them.

**Strategic goal:** Everything else in Aegis (networks, allocation, stochastic weather, future web platform) should plug into this layer. A stable framework reduces rework when adding new element types or deployment targets.

---

## 2. Background & current state

### 2.1 What exists today

| Piece | Location | Role today |
|-------|----------|------------|
| `Aegis` | `global_attributes/aegis.py` | Base object: id, name, description, metadata |
| `Clock` | `global_attributes/clock.py` | Calendar time stepping (`start_date`, `end_date`, `time_step`, `advance`, `reset`) |
| `Simulator` | `global_attributes/simulator.py` | Prototype loop; references undefined `self.r`, `self.w`; placeholder ET |
| `Model` | `global_attributes/model.py` | Thin holder for clock, simulator, file loading |
| `TimeHistory` | `results/time_history.py` | Output storage aligned to clock index |
| Ad-hoc script | `global_attributes/test_model.py` | Manual loop: clock + inputs + append series (closest to intended pattern) |
| Domain elements | `hydrology/`, `water_manage/`, etc. | Called directly; no common simulation contract |

### 2.2 Known gaps

- No single **model assembly** API (register components, wire topology, configure run).
- No **component protocol** (`update`, inputs/outputs) enforced across modules.
- **Simulator** and **Clock** are loosely coupled; clock `update()` is unused in `Simulator.run()`.
- **Execution order** for networked elements (upstream → downstream) is implicit or missing.
- **Inputs** (tables, time series, stochastic generators) are not bound to the clock in a uniform way.
- **Outputs** are ad hoc (`pandas.Series`, `TimeHistory`); no run manifest or structured results.
- **Units** (`aegis_units.json`, pint in places) are not enforced at the framework boundary.
- **Reproducibility** (seeds, run metadata) not specified.

### 2.3 Reference pattern (target mental model)

`test_model.py` demonstrates the desired user experience:

1. Create a clock and define the run window.
2. Load or define inputs indexed by simulation time.
3. Each timestep: read inputs → update state → record outputs → advance clock.
4. After the run: inspect or plot time histories.

The framework should make this pattern **declarative and reusable**, not copy-pasted per model.

---

## 3. Vision statement

> The Aegis simulation framework provides a **deterministic, testable time-stepping engine** that composes hydrologic, hydraulic, and water-management elements into models of arbitrary topology, with explicit time, inputs, state, and outputs suitable for later exposure via APIs and a web UI.

---

## 4. Goals and non-goals

### 4.1 Goals (in scope)

- Unified **run lifecycle**: configure → validate → execute → finalize → access results.
- **Calendar-based** simulation (primary); support for **elapsed-time** index as a secondary mode.
- **Composable models**: register elements (including **multiple watersheds**) without modifying framework code.
- **Scheduled execution** of top-level elements; **graphs owned by watersheds**, not centralized in `Model`.
- **Implicit flow allocation** per timestep via network solvers (max-flow / min-cost; LP later).
- **Mass balance verification** each timestep with fail-fast on violation.
- **Input binding**: map external data and generators to elements per timestep.
- **Output recording**: named time series with units and metadata.
- **Reset and rerun** the same model with different parameters or seeds.
- **Testability**: headless runs, golden-run comparison, no GUI required for core tests.

### 4.2 Non-goals (out of scope for v1)

- Web server, REST API, authentication, multi-tenant storage.
- Distributed / HPC parallel execution.
- Real-time streaming or sub-minute operational forecasting.
- Automatic calibration / optimization (may consume framework later).
- Full migration of every legacy class in one release.
- Replacing NetworkX or rewriting Sacramento/AWBM physics.
- **Nested sub-stepping** (e.g. hourly routing inside daily hydrology) — v1 uses a single clock only (D4).
- **Backward compatibility** with `Simulator` / `global_attributes` import paths (D7).

---

## 5. Stakeholders & users

| User | Need |
|------|------|
| You (developer) | Fast iteration, clear extension points, good tests |
| Future you (platform) | Stable run contract for API wrapping |
| Future collaborators | Documented lifecycle and element interface |
| Future end users (indirect) | Reproducible runs and understandable results |

---

## 6. Definitions

| Term | Definition |
|------|------------|
| **Framework** | Clock, model container, scheduler, I/O binding, run controller |
| **Model** | Named collection of elements, topology, parameters, and run configuration |
| **Element** | Any simulatable object (catchment, reservoir, junction, controller, etc.) |
| **State** | Values that persist across timesteps and define continued behavior |
| **Input** | Exogenous or scheduled value for a timestep (climate, demand, rule set) |
| **Output** | Value recorded each timestep (flow, storage, allocation) |
| **Run** | One complete execution from initial time to end time |
| **Scenario** | A model plus a specific input set and parameter overrides |
| **Timestep** | One advancement of `Clock` by `time_step` |
| **Watershed** | Domain element that **owns** its NetworkX graph (catchments, junctions, capacities); may exist multiple times per project model |
| **Flow solve** | Timestep-level global allocation of flows on a network (e.g. max-flow, min-cost flow; future LP) — flows are **implicit**, not passed hand-to-hand between `update` calls |

---

## 7. Architecture decisions (resolved)

These decisions supersede §12 (formerly open questions). Implementation MUST follow them unless explicitly revised.

| # | Topic | Decision |
|---|--------|----------|
| D1 | **Package** | Introduce **`aegis.simulation`** for the framework (`Clock`, `Model`, `RunController`, scheduler, recorder, validation). Legacy `global_attributes` may be migrated incrementally; new code lives under `aegis`. |
| D2 | **Graph ownership** | **`Watershed` (and similar network elements) own their graphs.** The framework registers and schedules them; it does not centralize all topology in `Model`. A single project `Model` MAY contain **multiple watersheds** (and other elements) as peers. |
| D3 | **Flow coupling** | **Implicit / global solve per timestep.** Elements contribute supplies, demands, and edge capacities (and eventually costs/constraints). A **flow solver** (initially NetworkX max-flow / min-cost; later LP/MIP as needed) assigns flows on the graph. Flows are NOT passed as explicit arguments along edges in v1. |
| D4 | **Sub-stepping** | **Not in v1.** One model clock, one `time_step` for all elements. No nested hourly-inside-daily loops in the framework. |
| D5 | **Mass balance** | **Framework enforces mass balance** at the end of each timestep (within documented numerical tolerance). Fail the step if closure cannot be achieved or verified. |
| D6 | **Failure policy** | **Fail-fast** with **structured diagnostics** (timestep, element id, solver status, constraint/balance residuals). No collect-and-continue — LP/network solves are hard enough to debug without partial state. |
| D7 | **Backward compatibility** | **None required** (pre-production). Remove `Simulator` prototype; replace with `RunController`. No deprecation aliases. |

### 7.0 Implications for the timestep loop

Each timestep, at a high level:

1. **Inputs** — bind climate, demands, rules from `InputManager`.
2. **Local updates** — elements compute local state (e.g. catchment runoff, reservoir stage) and publish **capacities/supplies/demands** to their owned graph.
3. **Flow solve** — for each network element (e.g. `Watershed`), run the configured solver on that graph (implicit flows).
4. **Post-solve updates** — apply solved flows to storage elements, allocators, etc.
5. **Mass balance check** — framework verifies closure for the model (and per registered network where applicable).
6. **Record outputs** — commit timestep results to `Recorder`.
7. **Advance clock**.

---

## 8. Functional requirements

Requirements use **MUST** / **SHOULD** / **MAY** (RFC 2119 style).

### 8.1 Time (`Clock` evolution)

| ID | Requirement | Priority |
|----|-------------|----------|
| CLK-01 | The framework MUST expose a single authoritative time object per run. | P0 |
| CLK-02 | The clock MUST support configurable `start`, `end` (or duration), and `time_step` as `pandas.Timedelta` or parseable strings. | P0 |
| CLK-03 | The clock MUST provide read-only access each timestep to: current timestamp, timestep index, day-of-year, calendar month/year. | P0 |
| CLK-04 | The clock MUST support `reset()` to initial conditions for repeated runs. | P0 |
| CLK-05 | The clock SHOULD support sub-daily steps (hourly) without API changes. | P1 |
| CLK-06 | The framework MAY support an **elapsed-time** mode (integer step index only) for abstract or unit tests. | P2 |
| CLK-07 | Changing `time_step` after elements are registered SHOULD trigger validation warnings if element internal state assumes a fixed step. | P2 |
| CLK-08 | v1 MUST NOT support nested or element-specific sub-timesteps (see D4). | P0 |

### 8.2 Model assembly

| ID | Requirement | Priority |
|----|-------------|----------|
| MDL-01 | The framework MUST provide a `Model` (or equivalent) that owns the clock, element registry, and run configuration. | P0 |
| MDL-02 | Elements MUST be registrable by unique string id within a model. | P0 |
| MDL-03 | The model MUST support attaching arbitrary metadata per element (tags, type, display name). | P1 |
| MDL-04 | The model SHOULD support grouping elements (e.g. `watershed`, `reservoir_system`) for ordered execution and output namespacing. | P1 |
| MDL-05 | The model MUST validate before run: duplicate ids, dangling references, missing required parameters. | P0 |
| MDL-06 | The model SHOULD support serialization/deserialization of structure (ids, types, parameters) independent of a full run — format TBD (JSON/YAML). | P2 |
| MDL-07 | The model MUST allow registering **multiple** network-owning elements (e.g. several `Watershed` instances) with unique ids (see D2). | P0 |
| MDL-08 | The model MUST NOT require a single project-wide NetworkX graph; topology stays with domain elements. | P0 |

### 8.3 Element interface (simulation contract)

| ID | Requirement | Priority |
|----|-------------|----------|
| ELM-01 | Every simulatable element MUST implement a documented lifecycle: at minimum `initialize(run_context)` and `update(timestep_context)`. | P0 |
| ELM-02 | `update` MUST be side-effecting only on element state and declared outputs; it MUST NOT advance global time. | P0 |
| ELM-03 | Elements SHOULD declare: `element_type`, `inputs` (names), `outputs` (names), `state_variables` (names). | P1 |
| ELM-04 | Elements MAY implement `finalize(run_context)` for post-run summaries. | P2 |
| ELM-05 | Legacy classes (e.g. `Catchment`, `Reservoir`, `Watershed`) SHOULD be wrappable via thin adapters rather than rewritten immediately. | P0 |
| ELM-06 | Elements that cannot run at the current timestep (e.g. monthly data on daily step) MUST receive interpolated or aggregated values via the input layer, not ad hoc logic inside each element. | P1 |
| ELM-07 | Network-owning elements MUST expose a hook to run or participate in the **flow solve** after local updates (see D3). | P0 |

### 8.4 Topology, scheduling & flow solve

| ID | Requirement | Priority |
|----|-------------|----------|
| TOP-01 | The framework MUST schedule **element execution order** among registered top-level elements (e.g. inputs → watersheds → reservoirs → controllers). | P0 |
| TOP-02 | **Graph topology** MUST remain owned by domain types (e.g. `Watershed`); the framework schedules when those elements run and when their solver executes (see D2). | P0 |
| TOP-03 | Cyclic dependencies between top-level elements (e.g. feedback) SHOULD be detected at validate time or handled via explicit “solved” groups (future). | P2 |
| TOP-04 | `Watershed` / `Network` integration MUST use an adapter implementing `Simulatable` without moving the DiGraph into `Model`. | P0 |
| TOP-05 | A single timestep MUST complete local updates, flow solve, mass balance, and recording before the clock advances (atomic step semantics). | P0 |
| FLW-01 | Each timestep, network elements MUST resolve flows via a **global solver** on their graph (max-flow, min-cost, or documented successor), not by passing flow scalars into downstream `update` arguments (see D3). | P0 |
| FLW-02 | The framework MUST define a `FlowSolveResult` (or equivalent) capturing success, method, residual, and per-edge flows for diagnostics. | P0 |
| FLW-03 | Solver failure MUST fail-fast with context: watershed id, solver method, infeasibility/unbounded hints if available (see D6). | P0 |
| FLW-04 | The initial implementation SHOULD use existing NetworkX (`maximum_flow`, `network_simplex`) where applicable; LP/MIP MAY be introduced when min-cost or allocation rules exceed graph algorithms. | P1 |

### 8.5 Mass balance

| ID | Requirement | Priority |
|----|-------------|----------|
| MB-01 | At the end of each timestep, the framework MUST verify **mass balance** for the model within a configurable tolerance (see D5). | P0 |
| MB-02 | Balance checks MUST include: total external inflows + storage deltas − outflows − losses ≈ 0 (terms defined per registered element contributions). | P0 |
| MB-03 | Mass balance violation MUST abort the run with a structured error reporting timestep, imbalance magnitude, and contributing elements. | P0 |
| MB-04 | Per-watershed balance MAY be reported as diagnostics even when a project contains multiple watersheds. | P1 |

### 8.6 Inputs

| ID | Requirement | Priority |
|----|-------------|----------|
| INP-01 | The framework MUST bind named inputs to elements or global scope for each timestep. | P0 |
| INP-02 | Input providers MUST include at least: constant, tabular lookup (`Vector` / `Table`), and time-indexed series (`TimeSeries` / CSV). | P0 |
| INP-03 | Input lookup MUST use the clock’s current time (calendar) as the primary key. | P0 |
| INP-04 | The framework SHOULD support stochastic inputs with explicit random seed stored in run metadata. | P1 |
| INP-05 | Unit conversion at the framework boundary SHOULD be applied when provider unit differs from element expected unit (pint-based). | P2 |

### 8.7 Outputs & recording

| ID | Requirement | Priority |
|----|-------------|----------|
| OUT-01 | The framework MUST allow registration of output variables (element id + name) before the run. | P0 |
| OUT-02 | Each recorded output MUST store: timestep index, timestamp, value, unit (if known). | P0 |
| OUT-03 | Results MUST be retrievable as `pandas.DataFrame` (wide: time × variables) after the run. | P0 |
| OUT-04 | `TimeHistory` SHOULD be refactored to implement a framework `Recorder` interface rather than owning its own clock copy. | P1 |
| OUT-05 | The framework SHOULD support optional in-memory ring buffer vs full history for long runs. | P2 |
| OUT-06 | Plotting (`matplotlib`) MUST remain optional and outside the core run path. | P0 |

### 8.8 Run control (`RunController`)

| ID | Requirement | Priority |
|----|-------------|----------|
| RUN-01 | `aegis.simulation.RunController` MUST expose `run()` that executes: validate → initialize → loop(timestep) → finalize. | P0 |
| RUN-02 | Each loop iteration MUST follow §7.0: inputs → local updates → flow solve → post-solve updates → mass balance → record → advance clock. | P0 |
| RUN-03 | `run()` MUST return a structured `RunResult` (success, warnings, timing, output handles, last error if failed). | P0 |
| RUN-04 | The framework SHOULD support `step()` for single-timestep debugging. | P1 |
| RUN-05 | The framework SHOULD support `pause` / `resume` hooks for future UI (no UI required in v1). | P2 |
| RUN-06 | Any exception or solver/balance failure MUST **fail-fast**; no partial timestep commit (see D6). | P0 |
| RUN-07 | Errors MUST be **structured** (timestep index, timestamp, element id, phase: input / update / flow_solve / balance / record, message, optional solver diagnostics). | P0 |
| RUN-08 | The legacy `Simulator` class MUST be removed or replaced; no compatibility shim (see D7). | P0 |

### 8.9 Scenarios & experiments

| ID | Requirement | Priority |
|----|-------------|----------|
| SCN-01 | A scenario MUST be definable as: base model + parameter overrides + input source references. | P1 |
| SCN-02 | The framework SHOULD support running multiple scenarios sequentially with isolated run state. | P1 |
| SCN-03 | Run metadata MUST include: scenario name, start/end, time_step, seed (if any), framework version, timestamp. | P1 |

### 8.10 Controllers & rules

| ID | Requirement | Priority |
|----|-------------|----------|
| CTL-01 | Controllers (e.g. `OnOff`) SHOULD be schedulable elements that write to other elements’ inputs or requests each timestep. | P1 |
| CTL-02 | Operating rules (reservoir releases, demands) SHOULD be expressible as elements or input bindings, not hard-coded in `RunController`. | P1 |

---

## 9. Non-functional requirements

| ID | Category | Requirement | Priority |
|----|----------|-------------|----------|
| NFR-01 | Correctness | Golden-path integration test: known inputs → known outputs within tolerance. | P0 |
| NFR-02 | Determinism | Same model + inputs + seed ⇒ identical results (floating-point tolerance documented). | P0 |
| NFR-03 | Performance | Daily timestep, 10-year, ≤20 elements: complete in &lt;10s on developer laptop (guideline). | P1 |
| NFR-04 | Testability | Core framework runnable without GUI, network, or Excel files. | P0 |
| NFR-05 | Maintainability | New element type addable without editing framework internals (registry + adapter). | P0 |
| NFR-06 | Documentation | Public docstrings for lifecycle, one tutorial script, architecture diagram in docs. | P1 |
| NFR-07 | Packaging | Framework code importable as **`aegis.simulation`** (see D1); no implicit `sys.path` hacks. | P0 |
| NFR-09 | Diagnostics | Solver and balance failures MUST produce logs/errors sufficient to debug without attaching a debugger. | P0 |
| NFR-08 | Extensibility | Clear extension points documented; breaking changes versioned once semver adopted. | P2 |

---

## 10. Proposed architecture (conceptual)

```
┌──────────────────────────────────────────────────────────────────┐
│  aegis.simulation.Model                                           │
│  ┌─────────┐  ┌────────────────┐  ┌──────────────────────────┐  │
│  │  Clock  │  │ ElementScheduler│  │  InputManager            │  │
│  └────┬────┘  │ (top-level order)│  │  (providers/bind)      │  │
│       │       └────────┬─────────┘  └────────────┬─────────────┘  │
│       │                │                         │                │
│       └────────────────┼─────────────────────────┘                │
│                        ▼                                          │
│               ┌─────────────────┐                                 │
│               │  RunController   │  run(), step(), reset           │
│               └────────┬────────┘                                 │
│                        │ each timestep (§7.0)                     │
│     ┌──────────────────┼──────────────────┐                       │
│     ▼                  ▼                  ▼                       │
│  Watershed A      Reservoir R       Controller C   (adapters)     │
│  [owns DiGraph]         │                                           │
│     │                   │                                           │
│     ▼                   │                                           │
│  FlowSolver ────────────┘  (max-flow / min-cost / future LP)      │
│     │                                                               │
│     ▼                                                               │
│  MassBalanceCheck ──► Recorder ──► RunResult                        │
└──────────────────────────────────────────────────────────────────┘
```

### 10.1 Core types (suggested)

| Type | Package | Role |
|------|---------|------|
| `RunContext` | `aegis.simulation` | Clock, model id, scenario metadata, random generator |
| `TimestepContext` | `aegis.simulation` | Current time, index, dt, input snapshot |
| `Simulatable` | `aegis.simulation` | Protocol: `initialize`, `update`, optional `finalize` |
| `ElementAdapter` | `aegis.simulation` | Wraps legacy `Catchment`, `Reservoir`, `Watershed`, etc. |
| `InputProvider` | `aegis.simulation` | `value_at(timestep_context) -> float \| dict` |
| `FlowSolveResult` | `aegis.simulation` | Solver status, edge flows, diagnostics |
| `MassBalanceReport` | `aegis.simulation` | Residuals, pass/fail, contributors |
| `SimulationError` | `aegis.simulation` | Structured fail-fast exception |
| `Recorder` | `aegis.simulation` | `record(name, value, unit, context)` |
| `RunResult` | `aegis.simulation` | Status, warnings, `outputs: DataFrame`, metadata |

### 10.2 Relationship to existing classes

| Existing | Framework role |
|----------|----------------|
| `Clock` | Move or re-export from `aegis.simulation.clock` |
| `Simulator` | **Removed** — replaced by `RunController` (D7) |
| `Model` | `aegis.simulation.Model` — registry, validate, run config; does **not** own watershed graphs |
| `TimeHistory` | Implements `Recorder` or wraps it |
| `Watershed` | Owns DiGraph; adapter runs local update + invokes flow solver |
| `Network` | Used inside `Watershed`; not duplicated at model level |
| `test_model.py` | Becomes `examples/climate_loop.py` |

### 10.3 Suggested package layout

```
aegis/
  __init__.py
  simulation/
    __init__.py
    clock.py
    model.py
    run_controller.py
    context.py          # RunContext, TimestepContext
    protocols.py        # Simulatable
    scheduler.py
    inputs.py
    recorder.py
    flow.py             # FlowSolveResult, solver dispatch
    balance.py          # MassBalanceCheck
    errors.py           # SimulationError
    adapters/           # watershed, reservoir, ...
```

**Extending the framework:** see [extending-elements.md](extending-elements.md) for adding new `Simulatable` elements and adapters.

---

## 11. Phased delivery

### Phase 0 — Foundation (MVP)

**Exit criteria:** One scripted model runs headlessly with tests.

- [x] Create `aegis/simulation/` package (D1)
- [x] Define `Simulatable`, `TimestepContext`, `RunContext`, `SimulationError`
- [x] Implement `Model`: register elements (incl. multiple watersheds), validate, hold clock
- [x] Implement `RunController.run()` per §7.0 and RUN-01/02 (Phase 0 subset; flow solve Phase 1)
- [x] Implement `Recorder` → DataFrame
- [x] Port `test_model.py` to framework API → `examples/climate_loop.py`
- [x] Remove `Simulator` prototype (D7)
- [x] Unit tests: clock, dummy element, record outputs, fail-fast error shape

### Phase 1 — Domain integration

**Exit criteria:** Watershed + one reservoir runs for 30 daily steps.

- [x] `ElementAdapter` for `Watershed` (owns graph; FLW-01 via NetworkX)
- [x] `ElementAdapter` for `Reservoir` / `Store`
- [x] `FlowSolveResult` + solver failure diagnostics (FLW-02/03)
- [x] `MassBalanceCheck` per timestep (MB-01–03)
- [x] Input binding for precip/ET from table or series
- [x] Integration test: two catchments → junction; outflow + mass balance
- [x] Integration test: two watersheds in one model (MDL-07)

### Phase 2 — Scenarios & quality

- [x] Scenario config (YAML/JSON)
- [x] Run metadata and reproducible seeds
- [x] `step()` debugging API
- [x] Refactor `TimeHistory` to recorder pattern
- [x] Document extension guide for new elements

### Phase 3 — Platform readiness (later)

- [ ] Serialize model structure
- [ ] Hook points for API/job queue
- [ ] Performance profiling on 100+ element graphs

---

## 12. Acceptance tests (high level)

| Test | Description |
|------|-------------|
| AT-01 | Empty model with clock only advances correct number of steps. |
| AT-02 | Dummy element increments state; output series matches analytical expectation. |
| AT-03 | Climate replay (`test_model` equivalent) reproduces evap/precip series. |
| AT-04 | Two catchments → junction → sink: solved outflow equals sum of supplies (FLW-01). |
| AT-05 | Reservoir with inflow series: mass balance closure within tolerance per step (MB-01). |
| AT-06 | Invalid model (duplicate id) fails at validate with clear error. |
| AT-07 | Reset and second run produces identical results with same seed. |
| AT-08 | Solver infeasible configuration fails-fast with `SimulationError` including watershed id and phase `flow_solve`. |
| AT-09 | Mass balance violation fails-fast with imbalance magnitude and timestep (MB-03). |
| AT-10 | Model with two watersheds runs independently without shared graph state bleed. |

---

## 13. Success metrics

The simulation framework v1 is successful when:

1. You can build the `test_model.py` climate loop **without** hand-writing a `while c.running` loop.
2. You can run a **watershed + reservoir** model for at least one year daily with recorded storage and outflow.
3. A new collaborator can add a dummy element by implementing the protocol and registering it — without reading the entire codebase.
4. All Phase 0 acceptance tests pass in CI (once CI exists).

---

## 14. Appendix: traceability to current code

| Requirement area | Primary existing modules | Target |
|------------------|-------------------------|--------|
| Time | `global_attributes/clock.py` | `aegis/simulation/clock.py` |
| Run loop | `test_model.py` | `aegis/simulation/run_controller.py` |
| Model shell | `global_attributes/model.py` | `aegis/simulation/model.py` |
| Flow solve | `water_manage/flow_network.py` | `Watershed` + `aegis/simulation/flow.py` |
| Outputs | `results/time_history.py` |
| Inputs | `inputs/data.py`, `inputs/table.py`, `inputs/time_series.py` |
| Topology | `water_manage/flow_network.py`, `hydrology/watershed.py` |
| Storage ops | `water_manage/store.py`, `reservoir.py`, `allocator.py` |
| Base object | `global_attributes/aegis.py` |

---

## Revision history

| Version | Date | Notes |
|---------|------|-------|
| 0.1 | 2026-05-25 | Initial draft |
| 0.2 | 2026-05-25 | Architecture decisions D1–D7; flow solve, mass balance, package layout |
| 0.3 | 2026-05-25 | Phase 0 complete: RunController, Recorder, climate example, tests |
| 0.4 | 2026-05-25 | Phase 1: watershed/reservoir adapters, NetworkX flow solve, mass balance |
| 0.5 | 2026-05-25 | Pytest suite under `tests/simulation/`; see `docs/testing.md` |
