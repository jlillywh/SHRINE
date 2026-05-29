# Install

SHRINE requires **Python 3.10+**. WSL or Linux is recommended for running the bundled test scripts; Windows works with a normal virtual environment.

## Core install

From a clone of the repository:

```bash
git clone https://github.com/jlillywh/SHRINE.git
cd SHRINE
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

On Ubuntu/WSL, the system Python may block bare `pip install` (PEP 668). Always use the venv interpreter:

```bash
bash scripts/bootstrap_venv.sh     # first-time setup
.venv/bin/python3 -m pip install -e .
```

## Optional extras

Extras are defined in `pyproject.toml` under `[project.optional-dependencies]`.

| Extra | Purpose | Command |
|-------|---------|---------|
| *(none)* | Core runtime | `pip install -e .` |
| `dev` | pytest, coverage, mypy, ruff, pre-commit | `pip install -e ".[dev]"` |
| `docs` | MkDocs Material site (this documentation) | `pip install -e ".[docs]"` |
| `viz` | matplotlib — charts and network drawing | `pip install -e ".[viz]"` |
| `hydrology` | hydrofunctions — USGS NWIS demo | `pip install -e ".[hydrology]"` |

### Recommended profiles

**Contributors** (tests + common legacy tooling):

```bash
pip install -e ".[dev,viz,hydrology]"
```

**Framework CI / quickstart** (matches GitHub Actions):

```bash
pip install -e ".[dev]"
```

**Documentation authors**:

```bash
pip install -e ".[docs,dev]"
```

## Verify the install

```bash
.venv/bin/python3 -c "import shrine; import shrine.simulation as sim; print(shrine.__version__, sim.__api_version__)"
```

Run the test suite:

```bash
./scripts/run_tests.sh
# or: .venv/bin/python3 -m pytest tests/ -q
```

See [Testing & CI](testing.md) for layout, mypy, ruff, and troubleshooting.

## Import rules

After `pip install -e .`, imports resolve through the editable install. **Do not** set `PYTHONPATH=.` or add the repo root to `sys.path`.

```python
from shrine.simulation import Model, RunController
from hydrology.watershed import Watershed
```

Library code lives under `src/`; tests and examples stay at the repo root.

## Next steps

- [Quickstart](quickstart.md) — run your first scenario
- [Concepts](concepts.md) — framework mental model
