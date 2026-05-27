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
.venv/bin/python3 -m pip install -e ".[dev]"
.venv/bin/python3 -c "import pint; print(pint.__version__)"
.venv/bin/python3 -m pytest tests/simulation -v
```

If `source .venv/bin/activate` shows `(.venv)` but `python3 -c "import pint"` fails, your PATH did not switch — use `.venv/bin/python3 -m pip` as above or rerun `bash scripts/bootstrap_venv.sh`.

If you already have `venv/` from older work, either `source venv/bin/activate` or rename it to `.venv`.

**Dependencies:** Scenario unit validation uses **pint** when installed (`pip install -e ".[dev]"` or `pip install -r requirements.txt`). Without pint, only unit syntax is checked and tests that require semantic validation are skipped.

**WSL / Cursor:** If errors reference old line numbers (for example `catchment.py` line 1 importing `Awbm`),
your WSL tree under `~/SHRINE` may still be an old copy. Pull or sync from the machine where you edited
the repo, then ensure `validation/__init__.py` exists at the project root.

## Layout

| Path | Purpose |
|------|---------|
| `tests/conftest.py` | Shared fixtures (`short_clock`, `two_catchment_watershed`, `SimpleStore`, …) |
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

Legacy domain tests (hydrology, `water_manage`, etc.) live beside their modules (`hydrology/test_*.py`). Install project deps first (`pip install -e ".[dev]"`), then run:

```bash
python3 -m pytest hydrology/ water_manage/ data/ inputs/ -q
```

Pytest uses `--import-mode=importlib` in `addopts` (see `pyproject.toml`) so `inputs/data.py` does not shadow the top-level `data/` package when collecting tests from multiple directories.

## Coverage expectations

- **`shrine.simulation`**: target **≥ 85%** line coverage before merging simulation work.
- New framework code should include unit tests; integration behavior should map to an AT-* test when applicable.

## CI (future)

```yaml
# Example GitHub Actions step
- run: pip install -e ".[dev]"
- run: pytest tests/simulation --cov=shrine.simulation --cov-fail-under=85
```

## Commit checklist

1. `./scripts/run_tests.sh --cov=shrine.simulation --cov-report=term-missing` (creates `.venv` on first run)
2. Confirm `.gitignore` excludes `venv/`, `*.egg-info/`, `.pytest_cache/`, `htmlcov/`
3. Stage simulation work only (see suggested commit below)

### Suggested first commit (simulation framework)

```bash
git status
git add .gitignore pyproject.toml shrine/ tests/ examples/ docs/simulation-framework-requirements.md docs/testing.md scripts/run_tests.sh
git add global_attributes/simulator.py global_attributes/test_legacy_simulator.py
git add -u global_attributes/model.py         # if modified
git commit -m "Add shrine.simulation framework with tests and examples.

Introduce the simulation package (clock, model, run controller, flow solve,
watershed/reservoir adapters, mass balance). Includes Phase 0–1 examples,
structured pytest suite, coverage config, and requirements documentation.
Removes the broken Simulator prototype."
```

Do **not** commit `venv/` or any `apikey.txt` file. See **[secrets-and-repo-hygiene.md](secrets-and-repo-hygiene.md)** for API keys, `.env` files, and what to do if a credential was committed.
