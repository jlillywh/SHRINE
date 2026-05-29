# ADR 0001: Units with pint at framework boundaries

## Status

Accepted (2026-05-29)

## Context

SHRINE combines legacy hydrology code that uses **bare floats** with a new simulation framework that records time series, validates scenarios, and may enforce mass balance. We need:

- Consistent validation of unit strings in scenario YAML and recorder metadata
- A shared registry for domain models that return pint `Quantity` (e.g. `RunoffModel`)
- Graceful behaviour when optional deps are missing in minimal installs

Alternatives considered:

- **No units layer** — keep floats everywhere; errors surface only at analysis time
- **Custom unit enum** — lightweight but cannot express compound units (`mm/day`, `m³/s`)
- **pint** — de facto Python units library; already a core dependency in `pyproject.toml`

## Decision

1. Use **pint** via `shrine.units.get_unit_registry()` — one cached `UnitRegistry` per process, optionally extended from `src/data/shrine_units.txt`.
2. Ship **default unit strings** in `src/data/shrine_units.json` for named variables (precipitation, flow, etc.).
3. Validate optional `unit` fields on scenario inputs at **load time** when pint is available; otherwise syntax-check only and emit a warning.
4. Expose the registry on **`RunContext.units_registry`** so elements and recorders share one context.
5. Support **`RunController(strict_units=True)`** so recorder outputs without unit metadata fail fast (`SimulationError`, `phase=record`).

Domain code may still use floats internally during migration; **framework boundaries** (scenario load, recording, typed protocols) are pint-aware.

## Consequences

### Positive

- Scenario and output metadata are self-describing for downstream tools
- `RunoffModel.compute()` returns typed quantities; adapters can convert consistently
- Single registry avoids conflicting definitions mid-run

### Negative / trade-offs

- Legacy modules remain float-heavy until wrapped or refactored
- Tests without pint installed skip semantic unit validation
- Contributors must learn pint unit strings and SHRINE’s default map

### Follow-ups

- Broader enforcement of `strict_units` on framework examples (roadmap **1.12**–**1.14**)
- Document unit conventions per variable in [results-recording.md](../results-recording.md)

## References

- `src/shrine/units.py`, `src/data/shrine_units.json`
- [Concepts — Units](../concepts.md)
- [Scenarios — optional unit fields](../scenarios.md)
