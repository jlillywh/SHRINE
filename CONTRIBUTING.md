# Contributing to SHRINE

Thank you for helping improve **SHRINE** (Simulation of Hydrology, Reservoirs, and Integrated Network Environments). This guide covers setup, workflow, and review expectations.

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

---

## Ways to contribute

- **Bug reports** and **feature requests** — [open an issue](https://github.com/jlillywh/SHRINE/issues/new/choose)
- **Documentation** — fixes and guides under `docs/` (MkDocs site)
- **Framework code** — `src/shrine/simulation/` (preferred path for new work)
- **Domain adapters & legacy modules** — `src/hydrology/`, `src/water_manage/`, … (follow [modernization roadmap](docs/modernization-roadmap.md))
- **Tests & scenarios** — `tests/`, `scenarios/`, golden/benchmark/reference fixtures
- **Examples** — `examples/`

Unsure where to start? Check [good first issues](https://github.com/jlillywh/SHRINE/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) or ask in a new issue.

---

## Development setup

**Requirements:** Python 3.10+, Git. WSL/Linux is the primary dev environment; Windows + WSL works well.

```bash
git clone https://github.com/jlillywh/SHRINE.git
cd SHRINE
bash scripts/bootstrap_venv.sh
```

**Recommended extras for contributors:**

```bash
.venv/bin/python3 -m pip install -e ".[dev,viz,hydrology]"
```

On Ubuntu/WSL, always use `.venv/bin/python3` and `.venv/bin/pip` — system-wide install is blocked (PEP 668). Details: [docs/install.md](docs/install.md).

**Optional — pre-commit (secret scanning):**

```bash
.venv/bin/pre-commit install
```

Runs [gitleaks](https://github.com/gitleaks/gitleaks) on staged files. See [docs/secrets-and-repo-hygiene.md](docs/secrets-and-repo-hygiene.md).

---

## Branch and pull request workflow

1. **Fork** the repository (or branch in-repo if you are a maintainer).
2. Create a **feature branch** from `master`:
   ```bash
   git checkout master
   git pull origin master
   git checkout -b your-name/short-description
   ```
3. Make focused changes; keep PRs **small and reviewable** when possible.
4. Run checks locally (see below).
5. **Push** and open a **pull request** against `master`.
6. Fill in the PR description: what changed, why, and how you tested it.
7. Address review feedback; maintainers merge when CI is green.

We use **lazy consensus** on non-controversial fixes; larger design changes should reference the [roadmap](docs/modernization-roadmap.md) or add an [ADR](docs/adr/README.md) (roadmap **3.12**).

---

## Running checks locally

Match CI before opening a PR:

| Check | Command |
|-------|---------|
| **Tests + coverage** | `./scripts/run_tests.sh` or `.venv/bin/python3 -m pytest tests/ --cov=shrine` |
| **Lint** | `.venv/bin/ruff check src tests examples scripts` |
| **Typecheck** | `.venv/bin/mypy src/shrine` |
| **Docs (strict)** | `pip install -e ".[docs]" && bash scripts/build_docs.sh` |

Full testing guide: [docs/testing.md](docs/testing.md).

**Coverage:** project floor is **80%** on `shrine` (`pyproject.toml`). New framework code should include tests.

**Regression fixtures** — if you change simulation outputs intentionally:

```bash
.venv/bin/python3 scripts/update_golden_outputs.py
.venv/bin/python3 scripts/update_benchmark_baseline.py              # local perf baseline
.venv/bin/python3 scripts/update_benchmark_baseline.py --target ci  # GitHub Actions baseline
```

If your PR changes reference scenarios under `scenarios/reference/`, also run `scripts/update_reference_golden.py` when that library is present in your branch.

Commit updated hash/timing files with the same PR.

**API docs** — after changing public `shrine.simulation` docstrings:

```bash
.venv/bin/python3 scripts/gen_api_reference.py
```

---

## Code guidelines

- **Public API:** import from `shrine.simulation` only for stable symbols (`__all__`). See [docs/api-stability.md](docs/api-stability.md).
- **Style:** [Ruff](https://docs.astral.sh/ruff/) (CI enforces). Run `ruff check --fix` before commit.
- **Types:** mypy on `src/shrine`; add annotations for new framework code.
- **Scope:** prefer minimal diffs; do not reformat unrelated files.
- **Legacy code:** `src/global_attributes/` and colocated tests are shrinking — prefer `tests/` and `shrine.simulation` for new work.
- **Secrets:** never commit API keys, tokens, or `.env` files. Pre-commit gitleaks helps catch accidents.

---

## Commit messages

Write clear, imperative subject lines:

```
Add reference golden test for nested junction scenario.

Explain non-obvious behavior in the body when needed.
```

For user-visible changes, add an entry under **`[Unreleased]`** in [CHANGELOG.md](CHANGELOG.md) ([Keep a Changelog](https://keepachangelog.com/) format).

Release/version bumps are maintainer-driven — see [docs/releases.md](docs/releases.md).

---

## Reporting security issues

Do **not** open public issues for undisclosed security vulnerabilities. A formal [SECURITY.md](SECURITY.md) policy is planned (roadmap **3.18**). Until then, contact maintainers privately via GitHub (repository owner) with details and reproduction steps.

---

## License

Contributions are licensed under the same terms as the project: **GNU General Public License v3.0 or later**. See [LICENSE](LICENSE). You must have the right to submit your work under this license.

---

## Getting help

- **Documentation:** https://jlillywh.github.io/SHRINE/
- **Issues:** https://github.com/jlillywh/SHRINE/issues
- **Architecture & concepts:** [docs/architecture.md](docs/architecture.md), [docs/concepts.md](docs/concepts.md)

Maintainers appreciate patience — this is an alpha research/engineering codebase moving toward OSS best practices on the [modernization roadmap](docs/modernization-roadmap.md).
