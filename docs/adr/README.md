# Architecture Decision Records (ADRs)

Major technical decisions for SHRINE are recorded here using a lightweight [ADR](https://adr.github.io/) format (roadmap **3.12**). Each record is immutable once **Accepted**; superseded decisions get a new ADR and a status update on the old one.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-units-with-pint-at-boundaries.md) | Units with pint at framework boundaries | Accepted |
| [0002](0002-networkx-flow-solver.md) | NetworkX max-flow for network routing | Accepted |
| [0003](0003-protocol-based-domain-contracts.md) | Protocol-based domain contracts | Accepted |
| [0004](0004-mit-license.md) | MIT license for library distribution | Accepted |

## When to write an ADR

Add an ADR when a change is **hard to reverse** or **cross-cutting**, for example:

- New public framework API or stability policy change
- Choice of library for core behaviour (solver, units, I/O)
- Domain boundary contracts (`Protocol`, adapter patterns)
- Data model changes that affect multiple packages

Skip ADRs for routine bug fixes, test-only changes, or documentation typos.

## Format

Copy [template.md](template.md). Files are named `NNNN-short-title.md` (four-digit sequence). Sections:

1. **Status** — Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
2. **Context** — problem and constraints
3. **Decision** — what we chose
4. **Consequences** — trade-offs, follow-ups

Link new ADRs from [architecture.md](../architecture.md) or the relevant guide when the decision affects contributors.

## Related docs

- [Architecture](../architecture.md) — framework / domain / adapters
- [API stability](../api-stability.md) — public surface versioning
- [Hydrology contracts](../hydrology-contracts.md) — Phase 2 domain protocols
- [CONTRIBUTING.md](https://github.com/jlillywh/SHRINE/blob/master/CONTRIBUTING.md) — propose ADRs in PRs for major design work
