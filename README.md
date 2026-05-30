[![PyPI version](https://img.shields.io/pypi/v/shrine?logo=pypi&logoColor=white&label=version&v=0.2.0)](https://pypi.org/project/shrine/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

# SHRINE

**S**imulation of **H**ydrology, **R**eservoirs, and **I**ntegrated **N**etwork **E**nvironments..

Open-source integrated water-resources modeling library (Python). SHRINE combines legacy domain modules (hydrology, storage, flow networks) with **`shrine.simulation`** for calendar-driven runs, mass balance, scenario files, and structured outputs.

Naming details: [docs/project-name.md](docs/project-name.md).

## Simulation framework (`shrine.simulation`)

The framework is the **only supported path** for new model runs. Import from the package root:

```python
import shrine.simulation as sim
# or
from shrine.simulation import Model, RunController, Clock, WatershedElement
```

**Package versions:** `shrine.__version__` (distribution) and `shrine.simulation.__api_version__` (stable simulation API surface, currently **1.1**). Stability and deprecation rules: [docs/api-stability.md](docs/api-stability.md). Release history: [CHANGELOG.md](CHANGELOG.md); SemVer and maintainer checklist: [docs/releases.md](docs/releases.md). Submodules outside `__all__` are internal unless noted in [extending-elements.md](docs/extending-elements.md).

### Public API

| Category | Symbols |
|----------|---------|
| **Run** | `Model`, `RegisteredElement`, `RunController`, `RunResult`, `RunSession`, `StepResult`, `ElementScheduler` |
| **Time** | `Clock`, `RunContext`, `TimestepContext` |
| **Elements** | `Simulatable`, `WatershedElement`, `CatchmentElement`, `ReservoirElement`, `ClimateRecorderElement`, `StorageLike` |
| **Plugins** | `list_element_plugins`, `load_element_plugin`, `create_element_from_plugin` (`shrine.elements` entry points) |
| **Inputs** | `InputManager`, `InputProvider`, `ConstantInput`, `MonthlyLookupInput`, `StochasticInput` |
| **Flow / balance** | `FlowSolver`, `NetworkXFlowSolver`, `FlowSolveResult`, `MassBalanceCheck`, `MassBalanceReport`, `MassBalanceTerm` |
| **Outputs / scenarios** | `Recorder`, `ScenarioConfig`, `load_scenario_file`, `run_scenario`, `run_scenarios`, `load_and_run` |
| **Metadata / RNG** | `build_run_metadata`, `enrich_run_metadata`, `RunTimer`, `make_rng` |
| **Deprecation** | `warn_api_deprecated` |
| **Errors** | `SimulationError`, `SimulationPhase` |

Capabilities:

- **`Model`** — register elements (watersheds, reservoirs, custom types) with a shared `Clock`
- **`RunController`** — validate → initialize → timestep loop → finalize
- **`InputManager`** — constant, monthly, and stochastic inputs bound by name
- **`Recorder`** — wide `pandas` DataFrame outputs per run
- **Scenarios** — YAML/JSON clock, inputs, and parameter overrides
- **Flow solve** — NetworkX max-flow on graphs owned by `Watershed` adapters
- **Mass balance** — per-timestep verification with `SimulationError` diagnostics

Requirements and phased delivery: [docs/simulation-framework-requirements.md](docs/simulation-framework-requirements.md). Layer diagram: [docs/architecture.md](docs/architecture.md).

## Project layout

| Area | Description |
|------|-------------|
| `src/shrine/simulation/` | Framework: clock, model, run controller, inputs, recorder, scenarios |
| `src/hydrology/` | Catchments, watersheds, networks |
| `src/water_manage/` | Storage, flow networks, operating rules |
| `src/inputs/`, `src/results/` | Tables, time series, `TimeHistory`, charts |
| `examples/` | Runnable demos (climate, watershed, scenarios, stepping) |
| `shrine-element-cookiecutter/` | Cookiecutter template for third-party `shrine.elements` plugins ([guide](docs/cookiecutter-element.md)) |
| `tests/simulation/` | Framework unit and acceptance tests |
| `docs/` | Guides (see below) |

Library code is under `src/`; run `pip install -e ".[dev]"` before tests or scripts (see [docs/testing.md](docs/testing.md)).

## Prerequisites

- Python **3.10+**
- WSL/Linux or Windows with WSL recommended for `./scripts/run_tests.sh`

## Install

**PyPI:** `pip install shrine` — see [docs/install.md](docs/install.md) (extras, PEP 668, wheel vs clone). **Development:** clone + editable install below.

### From PyPI

```bash
pip install shrine
pip install "shrine[dev,viz,hydrology]"
```

The PyPI wheel includes Python packages and `examples/`; **clone the repo** for bundled `scenarios/` and `./scripts/run_tests.sh`.

### From source *(development)*

```bash
git clone https://github.com/jlillywh/SHRINE.git
cd SHRINE
bash scripts/bootstrap_venv.sh    # .venv + pip install -e ".[dev]"
```

Contributors (tests + plotting + NWIS demo):

```bash
.venv/bin/python3 -m pip install -e ".[dev,viz,hydrology]"
```

On Ubuntu/WSL, use `.venv/bin/python3` and `.venv/bin/pip` — system `pip install` is blocked (PEP 668). See [docs/install.md](docs/install.md).

### Optional dependency extras

Defined in `pyproject.toml` under `[project.optional-dependencies]`. Same extra names for source and PyPI.

| Extra | Purpose | Source | PyPI |
|-------|---------|--------|------|
| *(none)* | Core runtime | `pip install -e .` | `pip install shrine` |
| `dev` | pytest, mypy, ruff, pre-commit | `pip install -e ".[dev]"` | `pip install "shrine[dev]"` |
| `docs` | MkDocs site | `pip install -e ".[docs]"` | `pip install "shrine[docs]"` |
| `viz` | matplotlib | `pip install -e ".[viz]"` | `pip install "shrine[viz]"` |
| `hydrology` | NWIS demo (`examples/nwis_streamflow.py`) | `pip install -e ".[hydrology]"` | `pip install "shrine[hydrology]"` |

**Recommended for contributors:**

```bash
pip install -e ".[dev,viz,hydrology]"
```

**Framework-only CI** (matches `./scripts/run_tests.sh`):

```bash
pip install -e ".[dev]"
```

## Run tests

```bash
./scripts/run_tests.sh
```

Or manually:

```bash
pytest tests/ -v
pytest tests/simulation --cov=shrine.simulation --cov-report=term-missing
```

See [docs/testing.md](docs/testing.md) for layout and troubleshooting (WSL sync, venv, etc.).

## Secrets and credentials

Do **not** commit API keys or `.env` files. Use `GOOGLE_MAPS_API_KEY` for the optional Maps demo, or a local gitignored `data_external/apikey.txt` (see `data_external/apikey.txt.example`). Full guidance: **[docs/secrets-and-repo-hygiene.md](docs/secrets-and-repo-hygiene.md)**. Optional local hook (with venv activated): `pip install -e ".[dev]" && pre-commit install` — gitleaks on commit; CI runs the same scan on push/PR.

## Examples

From the repo root with the venv activated:

```bash
# Climate inputs via framework (no Excel)
python examples/climate_loop.py

# Two catchments → junction → flow solve
python examples/watershed_run.py

# Single catchment, rational runoff (no network)
python examples/catchment_run.py

# Scenario file (JSON/YAML)
python examples/run_from_scenario.py scenarios/baseline_watershed.json

# Tutorial: watershed + monthly scenario + plot (roadmap 3.3)
python examples/tutorial_watershed.py --no-show --output tutorial_plot.png

# Single-timestep debugging
python examples/step_debug.py

# Minimal custom element
python examples/custom_element.py

# USGS NWIS fetch (optional: pip install -e ".[hydrology]")
python examples/nwis_streamflow.py
```

Bundled scenarios: `scenarios/baseline_watershed.json`, `scenarios/wet_year.yaml`.

## Documentation

**Online docs:** [https://jlillywh.github.io/SHRINE/](https://jlillywh.github.io/SHRINE/) (GitHub Pages — enable *Settings → Pages → GitHub Actions* after the first `Docs` workflow run on `master`).

Build locally:

```bash
pip install -e ".[docs]"
mkdocs serve          # http://127.0.0.1:8000
# or: ./scripts/build_docs.sh
```

| Guide | Topic |
|-------|--------|
| [Architecture](https://jlillywh.github.io/SHRINE/architecture/) | **Framework vs domain vs adapters** (diagrams) |
| [Comparison with other tools](https://jlillywh.github.io/SHRINE/comparison/) | SHRINE vs PySWMM, WEAP, ResSim, Spotpy, … (honest scope) |
| [docs/project-name.md](docs/project-name.md) | **SHRINE** naming and acronym |
| [docs/modernization-roadmap.md](docs/modernization-roadmap.md) | Strategic checklist: pythonic OOP, OSS excellence |
| [docs/api-stability.md](docs/api-stability.md) | SemVer, deprecation cycle, public API policy |
| [CHANGELOG.md](CHANGELOG.md) | Release history ([Keep a Changelog](https://keepachangelog.com/)) |
| [GOVERNANCE.md](GOVERNANCE.md) | Maintainer, release manager, lazy consensus |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting and supported versions |
| [docs/releases.md](docs/releases.md) | Versioning policy and maintainer release checklist |
| [docs/simulation-framework-requirements.md](docs/simulation-framework-requirements.md) | Architecture decisions and requirements |
| [docs/extending-elements.md](docs/extending-elements.md) | Adding new `Simulatable` elements |
| [docs/cookiecutter-element.md](docs/cookiecutter-element.md) | Cookiecutter template for plugin packages |
| [docs/scenarios.md](docs/scenarios.md) | Scenario YAML/JSON |
| [docs/step-debugging.md](docs/step-debugging.md) | `RunController.step()` API |
| [docs/results-recording.md](docs/results-recording.md) | `Recorder` and `TimeHistory` |
| [docs/install.md](docs/install.md) | **Install** — source vs PyPI, extras, PEP 668, wheel vs clone |
| [docs/testing.md](docs/testing.md) | Test suite and CI-style local runs |
| [docs/secrets-and-repo-hygiene.md](docs/secrets-and-repo-hygiene.md) | API keys, `.env`, history purge if a secret was committed |

## Quick API sketch

```python
from shrine.simulation import (
    Clock,
    ConstantInput,
    InputManager,
    Model,
    RunController,
    WatershedElement,
)
from hydrology.watershed import Watershed

ws = Watershed()
ws.add_junction("J1", "sink")
ws.link_catchment("C1", "J1")

model = Model(clock=Clock("1/1/2019", "1/15/2019"))
model.register_watershed("basin", WatershedElement(ws, element_id="basin"))

inputs = InputManager()
inputs.bind("precipitation", ConstantInput(10.0))
inputs.bind("evaporation", ConstantInput(1.0))

result = RunController(model, input_manager=inputs, seed=42).run()
print(result.outputs.head())
```

Legacy scripts (e.g. `global_attributes/test_model.py`) remain for reference; prefer `examples/climate_loop.py` and the framework APIs for new work.

## Community

| Need | Where |
|------|-------|
| **Questions**, ideas, show-and-tell | [GitHub Discussions](https://github.com/jlillywh/SHRINE/discussions) |
| **Bugs** and **feature requests** | [Issues](https://github.com/jlillywh/SHRINE/issues/new/choose) |
| **Security** vulnerabilities | [SECURITY.md](SECURITY.md) (private reporting — do not open a public issue) |

When you [start a discussion](https://github.com/jlillywh/SHRINE/discussions/new/choose), choose a category:

- **Q&A** — how-to questions, troubleshooting, API usage
- **Ideas** — feature proposals before they become issues
- **Show and tell** — scenarios, plugins, teaching examples, integrations

**Announcements** are for maintainer updates (for example the welcome thread). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Contributing

We welcome pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, tests, and PR workflow. For questions, use [Discussions](https://github.com/jlillywh/SHRINE/discussions) (table above).

## License

MIT License — see [LICENSE](LICENSE).
