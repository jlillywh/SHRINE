# Install

SHRINE requires **Python 3.10+**. Use a **virtual environment** on Ubuntu/WSL (PEP 668 blocks system-wide `pip install`).

**Today:** install from a **Git clone** (editable). **After roadmap 3.6 part 2:** `pip install shrine` from PyPI — same extras names, same import path (`import shrine`).

---

## Choose your path

| Goal | Command | Notes |
|------|---------|--------|
| **Develop or run tutorials** (recommended) | `git clone` + `pip install -e ".[dev,viz,hydrology]"` | Full repo: `scenarios/`, `tests/`, `./scripts/run_tests.sh` |
| **Framework tests only** | `pip install -e ".[dev]"` | Matches GitHub Actions |
| **Library use from PyPI** *(future)* | `pip install shrine` or `pip install "shrine[viz]"` | Wheel ships Python packages + `examples/`; **no** bundled `scenarios/` — clone repo or ship your own YAML/JSON |

Online docs: [https://jlillywh.github.io/SHRINE/install/](https://jlillywh.github.io/SHRINE/install/)

---

## Virtual environment (PEP 668)

On Ubuntu, Debian, and many WSL images, the system Python is **externally managed**. Bare `pip install` fails with `externally-managed-environment`.

**Always** use the project venv interpreter — activation alone may not switch `python3` on PATH:

```bash
cd SHRINE
bash scripts/bootstrap_venv.sh          # creates .venv + pip install -e ".[dev]"
.venv/bin/python3 -m pytest tests/ -q   # explicit venv python
```

Manual setup:

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install -U pip
.venv/bin/python3 -m pip install -e ".[dev,viz,hydrology]"
```

If `source .venv/bin/activate` shows `(.venv)` but `python3 -c "import hydrology"` fails, use `.venv/bin/python3` explicitly or rerun `bootstrap_venv.sh`. See [Testing & CI](testing.md#quick-start).

---

## Install from source *(current)*

```bash
git clone https://github.com/jlillywh/SHRINE.git
cd SHRINE
bash scripts/bootstrap_venv.sh
# or: python3 -m venv .venv && .venv/bin/python3 -m pip install -U pip && .venv/bin/python3 -m pip install -e ".[dev,viz,hydrology]"
```

Verify:

```bash
.venv/bin/python3 -c "import shrine; import hydrology; print(shrine.__version__)"
./scripts/run_tests.sh
```

---

## Install from PyPI *(when 3.6 part 2 ships)*

SHRINE is **not on PyPI yet**. When the first release is published, installs will look like:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install shrine
pip install "shrine[dev,viz,hydrology]"   # contributors + plotting + NWIS demo
```

Maintainer steps: [PyPI publishing](pypi.md).

---

## Optional extras

Defined in `pyproject.toml` → `[project.optional-dependencies]`. Combine extras with commas inside the brackets.

| Extra | Purpose | From source (today) | From PyPI *(future)* |
|-------|---------|---------------------|----------------------|
| *(none)* | Core runtime (`numpy`, `pandas`, `pint`, domain packages) | `pip install -e .` | `pip install shrine` |
| `dev` | pytest, coverage, mypy, ruff, pre-commit | `pip install -e ".[dev]"` | `pip install "shrine[dev]"` |
| `docs` | MkDocs Material site | `pip install -e ".[docs]"` | `pip install "shrine[docs]"` |
| `viz` | matplotlib — charts, `flow_network.draw` | `pip install -e ".[viz]"` | `pip install "shrine[viz]"` |
| `hydrology` | hydrofunctions — `examples/nwis_streamflow.py` | `pip install -e ".[hydrology]"` | `pip install "shrine[hydrology]"` |

### Recommended profiles

| Profile | Source command | PyPI command *(future)* |
|---------|----------------|-------------------------|
| **Contributors** (tests + legacy tooling) | `pip install -e ".[dev,viz,hydrology]"` | `pip install "shrine[dev,viz,hydrology]"` |
| **Framework CI** (matches GitHub Actions) | `pip install -e ".[dev]"` | `pip install "shrine[dev]"` |
| **Docs authors** | `pip install -e ".[docs,dev]"` | `pip install "shrine[docs,dev]"` |
| **Plotting, no NWIS** | `pip install -e ".[dev,viz]"` | `pip install "shrine[dev,viz]"` |

Upgrade extras after pulling new commits:

```bash
.venv/bin/python3 -m pip install -e ".[dev,viz,hydrology]"
```

---

## Wheel vs Git clone — what you get

| Included | Editable clone | PyPI wheel *(future)* |
|----------|----------------|------------------------|
| `shrine`, `hydrology`, `water_manage`, … under `src/` | Yes | Yes |
| `examples/` scripts | Yes (repo root) | Yes (packaged) |
| `scenarios/` (tutorial + baseline YAML/JSON) | Yes (repo root) | **No** — clone repo or copy scenario files |
| `tests/`, `scripts/run_tests.sh` | Yes | **No** — clone for development |
| `docs/` source, MkDocs site build | Yes | **No** — use [GitHub Pages](https://jlillywh.github.io/SHRINE/) |

**Tutorial and quickstart** paths such as `scenarios/baseline_watershed.json` and `scenarios/tutorial_watershed.yaml` require a **repository clone** today and after the first PyPI release unless you provide your own scenario files.

Example after PyPI-only install:

```bash
git clone https://github.com/jlillywh/SHRINE.git shrine-scenarios
cd shrine-scenarios
python examples/run_from_scenario.py scenarios/baseline_watershed.json
# (uses shrine imported from site-packages)
```

---

## Import rules

After `pip install -e .` or `pip install shrine`, imports resolve through the installed package. **Do not** set `PYTHONPATH=.` or add the repo root to `sys.path`.

```python
from shrine.simulation import Model, RunController
from hydrology.watershed import Watershed
```

Library code lives under `src/`; tests and scenarios stay at the repo root (clone only).

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `No module named 'hydrology'` | Editable install missing — run `.venv/bin/python3 -m pip install -e ".[dev]"` |
| `externally-managed-environment` | Use `.venv/bin/python3 -m pip`, not system `pip` |
| Tests fail on `framework_version` | Reinstall after version bump: `pip install -e ".[dev]"` |
| Scenario file not found | Clone repo for `scenarios/` or pass an absolute path to your YAML/JSON |

More detail: [Testing & CI](testing.md).

---

## Next steps

- [Quickstart](quickstart.md) — run your first scenario
- [Build your first watershed model](tutorial/first-watershed-model.md) — tutorial + plot
- [Concepts](concepts.md) — framework mental model
