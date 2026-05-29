# ADR 0002: NetworkX max-flow for network routing

## Status

Accepted (2026-05-29)

## Context

Watershed and water-allocation models route supply through **directed graphs** (catchments → junctions → sink). The framework must:

- Solve feasible flows given node **capacities** updated each timestep
- Stay composable: domain packages **own** the graph; the framework dispatches the solver
- Avoid maintaining a bespoke graph + max-flow implementation

Alternatives considered:

- **Hand-rolled routing** — simple for trees but fragile for parallel branches and future constraints
- **LP / optimization library** (e.g. PuLP, OR-Tools) — flexible for min-cost and rules; heavier dependency and setup
- **NetworkX** — already used for topology in `hydrology.Watershed` and `water_manage.Network`; provides `maximum_flow` and `min_cost_flow`

## Decision

1. Domain networks remain **NetworkX `DiGraph` instances** owned by watershed / flow-network objects (see [architecture.md](../architecture.md)).
2. The framework exposes **`FlowSolver`** with default implementation **`NetworkXFlowSolver`** in `shrine.simulation.flow`.
3. Default method is **`maximum_flow`** (`nx.maximum_flow`) using edge attribute **`capacity`**, matching how adapters call `update_capacity` before `outflow()`.
4. Optional **`min_cost`** mode uses NetworkX min-cost flow for future allocation problems.
5. **`WatershedElement`** (and similar adapters) invoke the solver during `update`; the framework does not mutate domain graphs directly.

Flow failures raise **`SimulationError`** with `phase=FLOW_SOLVE` and structured `details` (source, sink, method).

## Consequences

### Positive

- Reuses a well-tested library; graph visualization and inspection align with NetworkX tooling
- Clear split: topology + physics in domain, dispatch + error policy in framework
- Min-cost path available without new dependency

### Negative / trade-offs

- Very large networks may need profiling; NetworkX is pure Python
- Capacity semantics must stay consistent across domain `update_capacity` and solver expectations
- Not a full water-rights / rule engine — operating rules stay in domain or future elements

### Follow-ups

- Benchmark routing on reference scenarios ([reference-models.md](../reference-models.md))
- Document adapter contract in [extending-elements.md](../extending-elements.md) §8

## References

- `src/shrine/simulation/flow.py`, `src/water_manage/flow_network.py`
- `tests/simulation/test_flow.py`
- Requirements FLW-* in [simulation-framework-requirements.md](../simulation-framework-requirements.md)
