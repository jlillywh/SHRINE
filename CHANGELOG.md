# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
for `shrine.__version__`. The simulation public API (`shrine.simulation.__all__`) is
versioned separately as `shrine.simulation.__api_version__`; see [docs/api-stability.md](docs/api-stability.md)
and [docs/releases.md](docs/releases.md).

## [Unreleased]

### Added

- `shrine.elements` plugin entry points for third-party `Simulatable` implementations (`list_element_plugins`, `load_element_plugin`, `create_element_from_plugin`, `Model.register_plugin`); built-in adapters registered in `pyproject.toml` (roadmap **4.1**)

### Changed

- `shrine.simulation.__api_version__` bumped to **1.1** (new plugin discovery API)

## [0.2.0] - 2026-05-30

### Added

- `RunSession` context manager for step-mode runs (`with RunSession(controller):` / `controller.session()`)
- Run manifest on `RunResult` (`manifest`: git commit, scenario hash, element list, timestamps)
- Scenario load-time validation: unknown keys rejected; optional `unit` fields checked with pint
- API stability policy ([docs/api-stability.md](docs/api-stability.md)); `warn_api_deprecated()` helper
- Published public API in `shrine.simulation.__init__` (`__api_version__` = `1.0`)
- MkDocs Material documentation site ([https://jlillywh.github.io/SHRINE/](https://jlillywh.github.io/SHRINE/)); `docs` extra and `docs.yml` CI
- Auto-generated API reference under `docs/api/autogen/` (`scripts/gen_api_reference.py`, mkdocstrings)
- Tutorial: [Build your first watershed model](docs/tutorial/first-watershed-model.md) (`examples/tutorial_watershed.py`, `scenarios/tutorial_watershed.yaml`)
- Architecture and [comparison](docs/comparison.md) pages on the doc site
- Hydrology contracts: `RunoffModel` protocol, `RunoffMethod` enum; `Catchment` accepts injectable runoff models
- Water-management contracts: `StorageElement` protocol; typed graph node payloads; `GraphNodeType` enum
- Domain tests under `tests/hydrology/` and `tests/water_manage/` (pytest; colocated `src/*/test_*.py` deprecated)
- CI: mypy strict on `src/shrine/`, Ruff lint/format, Codecov coverage, cross-platform package smoke install (`package.yml`)
- Versioning and release policy ([docs/releases.md](docs/releases.md))
- PyPI packaging and publish on GitHub Release ([docs/pypi.md](docs/pypi.md), `publish.yml`; first public upload **0.2.0**)
- Contributor guide ([CONTRIBUTING.md](CONTRIBUTING.md)), [Code of Conduct](CODE_OF_CONDUCT.md), and GitHub issue templates (roadmap 3.11)
- Architecture Decision Records under [docs/adr/](docs/adr/) — units (pint), NetworkX flow solver, protocol-based domain contracts (roadmap 3.12)
- CSV + JSON export for run results via `export_run_result()` (roadmap 3.13)
- CSV time-series import: `TimeSeriesCsvInput`, `load_csv_timeseries()`, `bind_csv_columns()`, scenario `type: csv` (roadmap 3.14)
- [GOVERNANCE.md](GOVERNANCE.md) — maintainer, release manager, lazy consensus (roadmap 3.17)
- [SECURITY.md](SECURITY.md) — vulnerability reporting and supported versions (roadmap 3.18)
- PyPI publish workflow (`publish.yml`), TestPyPI dry run, release version check, post-upload install matrix (roadmap 3.6 part 2)

### Changed

- `Watershed` catchments live on NetworkX graph nodes (single source of truth; migrates parallel dict)
- `flow_network` node types use `GraphNodeType` instead of raw strings
- Project license changed from GPL v3 to **MIT** (roadmap 3.16, [ADR-0004](docs/adr/0004-mit-license.md))

### Removed

- `global_attributes.Simulator` broken prototype — use `shrine.simulation.RunController` (import stub raises with `DeprecationWarning`)

### Deprecated

- `global_attributes.Model` — use `LegacyModel` or `shrine.simulation.Model` (warns on `Model()`)
- `global_attributes.Clock` — use `LegacyClock` or `shrine.simulation.Clock` (when alias exists)
- String-based runoff factory on `Catchment` — prefer `RunoffMethod` or a `RunoffModel` instance

## [0.1.0] - 2026-05-25

Initial alpha release of the simulation framework.

### Added

- `shrine.simulation` framework: `Model`, `RunController`, inputs, recorder, scenarios, adapters
- Examples under `examples/` and framework tests under `tests/simulation/`
- Golden-run regression tests (`tests/golden/`)

[Unreleased]: https://github.com/jlillywh/SHRINE/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/jlillywh/SHRINE/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jlillywh/SHRINE/releases/tag/v0.1.0
