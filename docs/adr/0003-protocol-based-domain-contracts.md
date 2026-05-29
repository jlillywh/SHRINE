# ADR 0003: Protocol-based domain contracts

## Status

Accepted (2026-05-29)

## Context

SHRINE grew from legacy modules (`hydrology`, `water_manage`, …) with deep inheritance and implicit interfaces. Phase 2 modernization needs **clear boundaries** so:

- The framework depends on **capabilities**, not concrete legacy classes
- New runoff, storage, and element types can be plugged in without editing core loops
- Static type checkers (mypy) and tests can enforce contracts

Alternatives considered:

- **Abstract base classes only** — requires inheritance; awkward for wrapping existing code
- **Duck typing with no types** — flexible but untestable and undocumented
- **`typing.Protocol` (PEP 544)** — structural typing; `@runtime_checkable` for tests; no inheritance required

## Decision

1. **Framework boundary:** `Simulatable` in `shrine.simulation.protocols` — `initialize` / `update` / `finalize` + `element_type` (ELM-01). Elements register on `Model`; `RunController` drives the lifecycle.
2. **Hydrology boundary:** `RunoffModel` in `hydrology.protocols` — `compute(precip, et) -> Quantity`. `Catchment` accepts injectable models; `RunoffMethod` enum builds defaults; legacy `runoff()` objects wrap via `LegacyRunoffAdapter`.
3. **Storage boundary:** `StorageElement` protocol in hydrology/water_manage contracts (see [hydrology-contracts.md](../hydrology-contracts.md)).
4. **Graph payloads:** typed node payloads on NetworkX nodes (`CatchmentNode`, etc.) instead of parallel registries (roadmap **2.5**–**2.7**).
5. **Stability:** only symbols in `shrine.simulation.__all__` are public API; domain protocols are documented but may evolve until wrapped by stable adapters.

Adapters (`WatershedElement`, `ReservoirElement`, …) are thin **`Simulatable`** wrappers that translate `TimestepContext` ↔ domain calls.

## Consequences

### Positive

- Third-party elements can implement `Simulatable` without subclassing framework classes
- Runoff models swap via injection; tests use fakes and `@runtime_checkable` checks
- Aligns with project principle: **contracts over inheritance** ([roadmap](../modernization-roadmap.md) §1)

### Negative / trade-offs

- Two protocol layers (framework + domain) — contributors must know which side they extend
- Legacy string factories (`runoff_method="Awbm"`) remain deprecated shims
- Full graph migration incomplete; some deprecated properties (`Watershed.catchments`) linger

### Follow-ups

- Plugin entry points for third-party elements (roadmap **4.1**)
- ADRs for specific adapter patterns as new element types land

## References

- `src/shrine/simulation/protocols.py`, `src/hydrology/protocols.py`
- [Hydrology contracts](../hydrology-contracts.md), [Extending elements](../extending-elements.md)
- `tests/hydrology/test_runoff_protocol.py`, `tests/simulation/test_adapters.py`
