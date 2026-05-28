# SHRINE

**S**imulation of **H**ydrology, **R**eservoirs, and **I**ntegrated **N**etwork **E**nvironments..

![Athena's aegis (mythology)](https://upload.wikimedia.org/wikipedia/en/thumb/d/d6/Douriscup_83d40m_Athene_aegisWingedLionessOwl_pythonVomitsJason_fleeceInTree_Vatican.jpg/330px-Douriscup_83d40m_Athene_aegisWingedLionessOwl_pythonVomitsJason_fleeceInTree_Vatican.jpg)

Open-source integrated water-resources modeling library (Python). SHRINE combines legacy domain modules (hydrology, storage, flow networks) with **`shrine.simulation`** for calendar-driven runs, mass balance, scenario files, and structured outputs.

Naming details: [docs/project-name.md](docs/project-name.md).

## Simulation framework (`shrine.simulation`)

The framework is the **only supported path** for new model runs. Import from the package root:

```python
import shrine.simulation as sim
# or
from shrine.simulation import Model, RunController, Clock, WatershedElement
```

**Package versions:** `shrine.__version__` (distribution) and `shrine.simulation.__api_version__` (stable simulation API surface, currently **1.0**). Stability and deprecation rules: [docs/api-stability.md](docs/api-stability.md). Submodules outside `__all__` are internal unless noted in [extending-elements.md](docs/extending-elements.md).

### Public API

| Category | Symbols |
|----------|---------|
| **Run** | `Model`, `RegisteredElement`, `RunController`, `RunResult`, `RunSession`, `StepResult`, `ElementScheduler` |
| **Time** | `Clock`, `RunContext`, `TimestepContext` |
| **Elements** | `Simulatable`, `WatershedElement`, `CatchmentElement`, `ReservoirElement`, `ClimateRecorderElement`, `StorageLike` |
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
| `tests/simulation/` | Framework unit and acceptance tests |
| `docs/` | Guides (see below) |

Library code is under `src/`; run `pip install -e ".[dev]"` before tests or scripts (see [docs/testing.md](docs/testing.md)).

## Prerequisites

- Python **3.10+**
- WSL/Linux or Windows with WSL recommended for `./scripts/run_tests.sh`

## Install

```bash
cd SHRINE   # or your clone directory (GitHub repo may still be named Aegis)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Optional dependency extras

Defined in `pyproject.toml` under `[project.optional-dependencies]`. Combine extras in one install (comma-separated inside the brackets).

| Extra | Purpose | Typical command |
|-------|---------|-----------------|
| *(none)* | Core runtime: `shrine`, domain packages, scenarios (`numpy`, `pandas`, `pint`, …) | `pip install -e .` |
| `dev` | `pytest`, coverage, `pre-commit` | `pip install -e ".[dev]"` |
| `viz` | `matplotlib` — legacy charts, `flow_network.draw`, `inputs.table` plots | `pip install -e ".[viz]"` |
| `hydrology` | `hydrofunctions` — USGS NWIS demo (`examples/nwis_streamflow.py`) | `pip install -e ".[hydrology]"` |

**Recommended for contributors** (framework tests + common legacy tooling):

```bash
pip install -e ".[dev,viz,hydrology]"
```

**Framework-only CI / quickstart** (matches `./scripts/run_tests.sh`):

```bash
pip install -e ".[dev]"
```

Plotting without NWIS:

```bash
pip install -e ".[dev,viz]"
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

# Single-timestep debugging
python examples/step_debug.py

# Minimal custom element
python examples/custom_element.py

# USGS NWIS fetch (optional: pip install -e ".[hydrology]")
python examples/nwis_streamflow.py
```

Bundled scenarios: `scenarios/baseline_watershed.json`, `scenarios/wet_year.yaml`.

## Documentation

| Guide | Topic |
|-------|--------|
| [docs/project-name.md](docs/project-name.md) | **SHRINE** naming and acronym |
| [docs/modernization-roadmap.md](docs/modernization-roadmap.md) | Strategic checklist: pythonic OOP, OSS excellence |
| [docs/api-stability.md](docs/api-stability.md) | SemVer, deprecation cycle, public API policy |
| [docs/architecture.md](docs/architecture.md) | Framework vs domain vs adapters (diagrams) |
| [docs/simulation-framework-requirements.md](docs/simulation-framework-requirements.md) | Architecture decisions and requirements |
| [docs/extending-elements.md](docs/extending-elements.md) | Adding new `Simulatable` elements |
| [docs/scenarios.md](docs/scenarios.md) | Scenario YAML/JSON |
| [docs/step-debugging.md](docs/step-debugging.md) | `RunController.step()` API |
| [docs/results-recording.md](docs/results-recording.md) | `Recorder` and `TimeHistory` |
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

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
