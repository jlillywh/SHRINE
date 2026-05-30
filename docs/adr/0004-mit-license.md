# ADR 0004: MIT license for library distribution

## Status

Accepted (2026-05-30)

## Context

SHRINE shipped under **GNU GPL v3.0 or later** from early open-source polish (roadmap Phase 3). The project is a **Python simulation library** (`shrine.simulation`) intended for:

- `pip install` from PyPI (roadmap **3.6** part 2)
- Third-party `Simulatable` elements and plugin entry points (Phase **4.1**)
- Integration in consultant workflows, agency tools, and research code that may not be open source

Roadmap **3.16** asked us to confirm GPL fits contributor and user expectations, or document why not LGPL/MIT.

Alternatives considered:

| License | Pros | Cons for SHRINE |
|---------|------|-------------------|
| **GPL v3** (status quo) | Strong copyleft; derivatives stay open | Friction for proprietary apps, client deliverables, and closed-source plugins |
| **LGPL v3** | Slightly weaker copyleft for libraries | Unclear benefit in Python (import ≈ link); still unfamiliar to many reviewers |
| **Apache-2.0** | Patent grant; common in infra | Longer text; patent clause unnecessary for current scope |
| **MIT** | Simple; matches NumPy/Pandas/NetworkX norms; easy legal review | No requirement that improvements be open-sourced |

All core dependencies (NumPy, Pandas, NetworkX, Pint, etc.) use permissive licenses. No upstream license blocked relicensing; all commits to date are from the maintainer team.

## Decision

Relicense SHRINE under the **MIT License**, effective from the merge of this ADR and updated `LICENSE` file.

- Replace `LICENSE` (GPL v3 full text) with standard MIT text.
- Set `license = "MIT"` in `pyproject.toml`.
- Update contributor and documentation references (README, CONTRIBUTING, docs site copyright).

**GPL v3 is superseded** for new downloads and contributions after the change. Historical releases tagged before this change remain under GPL v3 unless explicitly re-published.

## Consequences

### Positive

- Lower barrier for consultancies, utilities, and researchers embedding SHRINE in mixed open/proprietary stacks
- Aligns with scientific Python ecosystem defaults and Phase 4 extensibility goals
- Simpler contributor onboarding (same license as most dependencies)

### Negative / trade-offs

- Forks and proprietary derivatives are allowed without source release
- Users must not assume copyleft protection when choosing SHRINE over GPL tools

### Follow-ups

- First PyPI release (**3.6** part 2) ships under MIT
- Optional: add a license badge to README after PyPI publish

## References

- [LICENSE](https://github.com/jlillywh/SHRINE/blob/master/LICENSE)
- [CONTRIBUTING.md](https://github.com/jlillywh/SHRINE/blob/master/CONTRIBUTING.md)
- Roadmap **3.16** — [modernization-roadmap.md](../modernization-roadmap.md)
