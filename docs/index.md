# SHRINE

**S**imulation of **H**ydrology, **R**eservoirs, and **I**ntegrated **N**etwork **E**nvironments.

SHRINE is an open-source Python library for integrated water-resources modeling. It combines legacy domain modules (hydrology, storage, flow networks) with **`shrine.simulation`** — a calendar-driven run engine with mass balance, scenario files, and structured outputs.

## New to SHRINE?

1. [Install](install.md) from a Git clone (venv required on Ubuntu/WSL).
2. Follow the [Quickstart](quickstart.md) to run a watershed model from a scenario file.
3. Work through [Build your first watershed model](tutorial/first-watershed-model.md) (scenario + plot).
4. Read [Concepts](concepts.md) for the mental model: `Model`, elements, inputs, and the run loop.
5. See [Architecture](architecture.md) for framework / domain / adapter diagrams (Mermaid).

## Supported path for new work

Import the simulation framework from the package root:

```python
from shrine.simulation import Model, RunController, Clock, WatershedElement
```

Legacy domain packages (`hydrology`, `water_manage`, …) remain available and are wrapped by **adapters** — see [Architecture](architecture.md).

## Documentation map

| Section | Contents |
|---------|----------|
| **Get started** | Install, quickstart, concepts, **architecture** (framework / domain / adapters) |
| **Tutorials** | End-to-end watershed model with scenario and plot |
| **Guides** | Scenarios, extending elements, testing, requirements |
| **API reference** | Public `shrine.simulation` surface |
| **Project** | Roadmap, **tool comparison**, naming, [contributing](https://github.com/jlillywh/SHRINE/blob/master/CONTRIBUTING.md), contributor hygiene |

## Versions

| Symbol | Meaning |
|--------|---------|
| `shrine.__version__` | Distribution version (PyPI package) |
| `shrine.simulation.__api_version__` | Stable simulation API (`1.0`) |

See [API stability](api-stability.md) for deprecation policy and [Versioning & releases](releases.md) for SemVer and the [changelog](https://github.com/jlillywh/SHRINE/blob/master/CHANGELOG.md).

## License

GNU General Public License v3.0 — see [LICENSE](https://github.com/jlillywh/SHRINE/blob/master/LICENSE).
