# SHRINE governance

How the project is led, how decisions are made, and who cuts releases. This document satisfies roadmap **3.17** and complements [CONTRIBUTING.md](CONTRIBUTING.md), [docs/releases.md](docs/releases.md), and [docs/adr/README.md](docs/adr/README.md).

SHRINE is an alpha open-source library. Roles below reflect **current practice**; they will expand as more contributors join.

---

## Roles

### Maintainer

The **maintainer** stewards the codebase and community:

- Sets technical direction with contributors (see [Decision-making](#decision-making))
- Reviews and merges pull requests when [CI](docs/testing.md) is green
- Triage issues and labels (`good first issue`, `help wanted`, etc.)
- Accepts or requests [Architecture Decision Records](docs/adr/README.md) for cross-cutting changes
- Enforces the [Code of Conduct](CODE_OF_CONDUCT.md)

**Current maintainer:** [Jason Lillywhite](https://github.com/jlillywh) (`@jlillywh`)

Contact: open a [GitHub issue](https://github.com/jlillywh/SHRINE/issues) for public matters; use [private vulnerability reporting](SECURITY.md#reporting-a-vulnerability) for security issues.

### Release manager

The **release manager** publishes versioned releases:

- Owns the [release checklist](docs/releases.md#release-checklist-maintainers) (changelog, version bump, tag, GitHub Release)
- Ensures `pytest`, docs build, and packaging smoke tests pass before tagging
- Coordinates PyPI upload when [roadmap 3.6 part 2](docs/modernization-roadmap.md) ships ([docs/pypi.md](docs/pypi.md))

**Current release manager:** Jason Lillywhite (same person as maintainer until the team grows)

When the project adds maintainers, the release manager may be a dedicated role or rotate per release — announce changes here and in release notes.

---

## Decision-making

SHRINE uses **lazy consensus** for most changes:

1. **Propose** — open an issue or draft PR describing the problem, options, and recommendation.
2. **Discuss** — maintainers and contributors comment. Substantive objections should include rationale and, when possible, an alternative.
3. **Wait** — allow **seven calendar days** on `master`-bound proposals that affect public API, scenario schema, or governance. Bug fixes, docs typos, and test-only changes may merge sooner.
4. **Resolve** — if no unresolved substantive objection remains, the proposal is **accepted** (silence counts as assent). The maintainer merges or closes accordingly.
5. **Escalate** — if consensus fails, the maintainer decides after summarizing trade-offs in the issue/PR, or the proposer may fork under the [MIT License](LICENSE).

### What needs lazy consensus

| Change | Process |
|--------|---------|
| Bug fix, docs, tests, internal refactor | Normal PR review; no waiting period required |
| New feature in `shrine.simulation.__all__` | PR + changelog; **7-day** lazy consensus if API or scenario-facing |
| Breaking API change | [Deprecation cycle](docs/api-stability.md) **and** ADR or issue with lazy consensus |
| New ADR (architecture, dependencies) | PR adding `docs/adr/NNNN-*.md`; lazy consensus before **Accepted** |
| Governance / license / release policy | PR updating this file or linked docs; lazy consensus |

### Hard reversals

Decisions recorded as **Accepted** ADRs stay in place until a new ADR supersedes them. Governance changes merge like any other doc but should note effective date in the PR.

---

## Adding maintainers

New maintainers are added by **lazy consensus** among existing maintainers (today: proposal by Jason Lillywhite, documented in a PR updating this file).

Expectations:

- Sustained, quality contributions (code, docs, review, issue triage)
- Agreement with [Code of Conduct](CODE_OF_CONDUCT.md) and this governance model
- Willingness to follow the release checklist when acting as release manager

Removing a maintainer for inactivity is at the discretion of remaining maintainers; removal for conduct follows the Code of Conduct enforcement path.

---

## Related documents

| Document | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Dev setup, PR workflow, tests |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards |
| [docs/releases.md](docs/releases.md) | SemVer, changelog, release checklist |
| [docs/api-stability.md](docs/api-stability.md) | Public API and deprecation |
| [docs/adr/README.md](docs/adr/README.md) | Architecture decisions |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |
| [docs/modernization-roadmap.md](docs/modernization-roadmap.md) | Strategic checklist |

---

## Revision history

| Date | Change |
|------|--------|
| 2026-05-30 | Initial governance (roadmap 3.17): maintainer, release manager, lazy consensus |
