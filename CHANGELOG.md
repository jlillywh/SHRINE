# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
for `shrine.__version__`. The simulation public API (`shrine.simulation.__all__`) is
versioned separately as `shrine.simulation.__api_version__`; see [docs/api-stability.md](docs/api-stability.md).

## [Unreleased]

### Added

- `RunSession` context manager for step-mode runs (`with RunSession(controller):` / `controller.session()`)
- Run manifest on `RunResult` (`manifest` field: git commit, scenario hash, element list, timestamps)
- Scenario load-time validation: unknown keys rejected; optional `unit` fields checked with pint (`scenario.py`)
- API stability policy ([docs/api-stability.md](docs/api-stability.md))
- `warn_api_deprecated()` helper in `shrine.simulation`
- Published public API in `shrine.simulation.__init__` (`__api_version__` = `1.0`)

### Removed

- `global_attributes.Simulator` broken prototype — use `shrine.simulation.RunController` (import stub raises with `DeprecationWarning`)

### Deprecated

- `global_attributes.Model` — use `LegacyModel` or `shrine.simulation.Model` (warns on `Model()`)
- `global_attributes.Clock` — use `LegacyClock` or `shrine.simulation.Clock` (when alias exists)

## [0.1.0] - 2026-05-25

### Added

- `shrine.simulation` framework: `Model`, `RunController`, inputs, recorder, scenarios, adapters
- Examples under `examples/` and tests under `tests/simulation/`

[Unreleased]: https://github.com/your-org/SHRINE/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/SHRINE/releases/tag/v0.1.0
