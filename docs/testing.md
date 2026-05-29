# Testing SHRINE

## Quick start

Ubuntu/WSL often blocks `pip install` on the system Python (PEP 668). Use the project venv’s **python3** explicitly (activation alone may still leave `python3` pointing at the system interpreter):

```bash
cd /home/jason/SHRINE
bash scripts/bootstrap_venv.sh    # create .venv + install deps (first time or repair)
bash scripts/run_tests.sh

# Or manually (note: .venv/bin/python3, not bare pip/python3):
python3 -m venv .venv
.venv/bin/python3 -m pip install -U pip
.venv/bin/python3 -m pip install -e ".[dev]"   # or ".[dev,viz,hydrology]" for legacy domain tests — see README
.venv/bin/python3 -c "import pint; print(pint.__version__)"
.venv/bin/python3 -m pytest tests/simulation -v
```

If `source .venv/bin/activate` shows `(.venv)` but `python3 -c "import pint"` fails, your PATH did not switch — use `.venv/bin/python3 -m pip` as above or rerun `bash scripts/bootstrap_venv.sh`.

If you already have `venv/` from older work, either `source venv/bin/activate` or rename it to `.venv`.

**Dependencies:** Scenario unit validation uses **pint** when installed (`pip install -e ".[dev]"` or `pip install -r requirements.txt`). Without pint, only unit syntax is checked and tests that require semantic validation are skipped.

**WSL / Cursor:** If errors reference old line numbers (for example `catchment.py` line 1 importing `Awbm`),
your WSL tree under `~/SHRINE` may still be an old copy. Pull or sync from the machine where you edited
the repo, then reinstall: `pip install -e ".[dev]"`.

## Layout and imports

Installable code lives under **`src/`** (framework and legacy domain packages). Tests, examples, and scenarios stay at the repo root.

**Do not** set `PYTHONPATH=.` or add the repo root to `sys.path`. After `pip install -e ".[dev]"`, imports resolve via the editable install (`src/` packages plus root `examples/` — see `pyproject.toml` → `[tool.setuptools.packages.find]`). Pytest uses `--import-mode=importlib` (no `pythonpath` override).

| Path | Purpose |
|------|---------|
| `src/shrine/simulation/` | Framework package |
| `src/hydrology/`, `src/water_manage/`, … | Legacy domain packages |
| `tests/` | Framework and integration tests |
| `examples/` | Runnable demos |
| `scenarios/` | Bundled scenario YAML/JSON |

## Test modules

| Path | Purpose |
|------|---------|
| `tests/conftest.py` | Shared fixtures (`short_clock`, `two_catchment_watershed`, `SimpleStore`, …) |
| `tests/golden/` | Expected SHA-256 of `result.outputs` for bundled scenarios (see `test_golden_run.py`) |
| `tests/simulation/test_mass_balance_property.py` | Fuzz-light mass balance for `SimpleStore` + `ReservoirElement` (seed `20240528`) |
| `tests/hydrology/` | Phase 2 hydrology contract tests (`RunoffModel`, `RunoffMethod`, graph payloads) |
| `tests/water_manage/` | Phase 2 storage contract tests (`StorageElement`) |
| `tests/simulation/test_clock.py` | Time stepping |
| `tests/simulation/test_model.py` | Model registry & validation |
| `tests/simulation/test_inputs.py` | Input providers |
| `tests/simulation/test_recorder.py` | Output recording |
| `tests/simulation/test_balance.py` | Mass balance |
| `tests/simulation/test_flow.py` | NetworkX flow solver |
| `tests/simulation/test_errors.py` | Structured errors |
| `tests/simulation/test_run_controller.py` | Run loop, fail-fast, climate |
| `tests/simulation/test_adapters.py` | Watershed & reservoir adapters |
| `tests/simulation/test_acceptance.py` | Requirements AT-* checks |
| `tests/simulation/test_scenario.py` | Scenario YAML/JSON load and run |
| `tests/simulation/test_metadata.py` | Run metadata fields and seeded RNG |
| `tests/simulation/test_step_debug.py` | `step()`, `reset()`, `complete()` debugging API |
| `tests/results/test_time_history.py` | `TimeHistory` backed by `Recorder` |
| `tests/simulation/test_custom_element_example.py` | Extension guide `DemandElement` example |

## Documentation

| Doc | Topic |
|-----|--------|
| [simulation-framework-requirements.md](simulation-framework-requirements.md) | Requirements & phased delivery |
| [extending-elements.md](extending-elements.md) | **Adding new simulation elements** |
| [scenarios.md](scenarios.md) | Scenario YAML/JSON |
| [step-debugging.md](step-debugging.md) | `step()` API |
| [results-recording.md](results-recording.md) | `Recorder` / `TimeHistory` |
| `tests/simulation/test_recorder.py` | Recorder API incl. `from_dataframe` |

Hydrology and water_manage domain tests live under `tests/hydrology/` and `tests/water_manage/` (roadmap **2.8**–**2.9**). Remaining colocated modules under `src/*/test_*.py` emit a **DeprecationWarning** on import (roadmap **2.11**); run the canonical suite only:

```bash
.venv/bin/python3 -m pytest tests/ -q
```

Do **not** add new tests under `src/`. Migrate to `tests/<package>/` and delete the colocated file when parity is reached.

| Package | Colocated (deprecated) | Migrated to |
|---------|------------------------|-------------|
| `hydrology/` | *(removed)* | `tests/hydrology/` |
| `water_manage/` | *(removed)* | `tests/water_manage/` |
| `global_attributes/` | `test_clock.py`, `test_shrine_object.py`, `test_model.py`, `test_suite*.py` | `tests/global_attributes/` (legacy Model/Simulator only) |
| `inputs/`, `geometry/`, `data/`, `hydraulics/`, `controllers/` | `test_*.py` | pending |

Helper: `testing.colocated.deprecate_colocated_module()`.

Pytest uses `--import-mode=importlib` in `addopts` (see `pyproject.toml`) so `inputs/data.py` does not shadow the top-level `data` package when collecting tests from multiple directories.

### Shared fixtures (`tests/conftest.py`)

| Fixture | Use |
|---------|-----|
| `short_clock`, `week_clock`, `month_clock` | `shrine.simulation.Clock` spans |
| `legacy_clock` | `global_attributes.clock.Clock` (WGEN tests) |
| `two_catchment_watershed`, `nested_junction_watershed` | Hydrology demand networks |
| `watershed_gml`, `network_gml` | GML paths under `src/*/test_data/` |
| `bounded_store`, `reservoir`, `standard_allocator`, `flow_network` | Legacy water_manage domain |
| `simple_store`, `watershed_model`, `reservoir_model`, `climate_inputs` | Simulation framework |

Path constants live in `tests/path_fixtures.py` (`WATERSHED_GML`, `NETWORK_GML`, …).

### Type checking (mypy)

Configured in `pyproject.toml` (roadmap **2.12**):

```bash
.venv/bin/mypy src/shrine          # strict (must pass in CI)
.venv/bin/mypy src/hydrology src/water_manage src/geometry src/inputs src/data  # basic domain
```

- **`shrine.*`**: `strict = true`, `follow_imports = silent` (domain imports not checked here)
- **Domain packages**: basic mode with documented `disable_error_code` baseline; all domain modules use `from __future__ import annotations` (**2.13**)

CI: `.github/workflows/typecheck.yml` on every push/PR.

Re-apply the future import after adding new domain modules: `.venv/bin/python3 scripts/add_future_annotations.py`

### Lint and format (ruff)

Configured in `pyproject.toml` (roadmap **2.14**):

```bash
.venv/bin/ruff check src/shrine tests examples scripts   # must pass in CI
.venv/bin/ruff format --check src tests examples scripts
.venv/bin/ruff format src tests examples scripts         # apply formatting locally
.venv/bin/ruff check --fix src/shrine tests examples scripts
```

- **Lint scope**: `src/shrine`, `tests`, `examples`, `scripts` (legacy domain lint debt ~120 issues — run `ruff check src` locally when tightening)
- **Format scope**: all of `src/` plus tests, examples, and scripts

CI: `.github/workflows/lint.yml` on every push/PR.

### Documentation site (MkDocs)

Configured in `mkdocs.yml` (roadmap **3.1**–**3.2**):

```bash
pip install -e ".[docs]"
python scripts/gen_api_reference.py   # regenerate API pages from docstrings
mkdocs serve                          # http://127.0.0.1:8000
./scripts/build_docs.sh               # gen + strict build to site/
```

API reference pages under `docs/api/autogen/` are generated from `shrine.simulation.__all__`; do not edit by hand.

CI: `.github/workflows/docs.yml` builds on every PR; deploys to GitHub Pages on push to `master`.

### PyPI package (roadmap **3.6**)

| Workflow | Purpose |
|----------|---------|
| `.github/workflows/package.yml` | Build wheel/sdist; smoke install on Ubuntu, Windows, macOS |
| `.github/workflows/publish.yml` | Upload to PyPI when a GitHub Release is published |

See [PyPI & releases](pypi.md) for `pip install shrine` and maintainer trusted-publisher setup.

## Coverage expectations

- **`shrine.simulation`**: target **≥ 85%** line coverage before merging simulation work.
- New framework code should include unit tests; integration behavior should map to an AT-* test when applicable.

## CI

GitHub Actions (`.github/workflows/test.yml`) on every push/PR to `master`:

- `pip install -e ".[dev]"`
- `pytest tests/ --cov=shrine --cov-report=xml` (80% floor from `pyproject.toml`)
- Upload `coverage.xml` to Codecov (`CODECOV_TOKEN` repository secret)

### Codecov on pull requests

`codecov.yml` enables **blocking** status checks on each PR:

| Check | Meaning |
|-------|---------|
| `codecov/project` | Overall `shrine` coverage vs 80% target (2% threshold) |
| `codecov/patch` | Coverage on lines changed in the PR (80% target, 5% threshold) |

**One-time setup (repo admin):**

1. Add repository secret **`CODECOV_TOKEN`** from [Codecov → SHRINE → Settings](https://app.codecov.io).
2. Install the **[Codecov GitHub App](https://github.com/apps/codecov)** on `jlillywh/SHRINE` (needed for check runs and PR comments).
3. Under **Settings → Branches → `master` → Branch protection**, require status checks:
   - `pytest` (GitHub Actions job name)
   - `mypy`, `ruff` (typecheck and lint workflows)
   - `codecov/project`
   - `codecov/patch`

Until the token and app are configured, the upload step fails CI (`fail_ci_if_error: true`).

## Commit checklist

1. `./scripts/run_tests.sh --cov=shrine.simulation --cov-report=term-missing` (creates `.venv` on first run)
2. Confirm `.gitignore` excludes `venv/`, `*.egg-info/`, `.pytest_cache/`, `htmlcov/`
3. Stage simulation work only (see suggested commit below)

### Suggested first commit (simulation framework)

```bash
git status
git add .gitignore pyproject.toml src/ tests/ examples/ docs/simulation-framework-requirements.md docs/testing.md scripts/run_tests.sh
git add src/global_attributes/simulator.py src/global_attributes/test_legacy_simulator.py
git add -u src/global_attributes/model.py         # if modified
git commit -m "Add shrine.simulation framework with tests and examples.

Introduce the simulation package (clock, model, run controller, flow solve,
watershed/reservoir adapters, mass balance). Includes Phase 0–1 examples,
structured pytest suite, coverage config, and requirements documentation.
Removes the broken Simulator prototype."
```

Do **not** commit `venv/` or any `apikey.txt` file. See **[secrets-and-repo-hygiene.md](secrets-and-repo-hygiene.md)** for API keys, `.env` files, and what to do if a credential was committed.
