# shrine-element-cookiecutter

Cookiecutter template for a **standalone Python package** that registers a custom
[`Simulatable`](https://jlillywh.github.io/SHRINE/extending-elements/) element via the
[`shrine.elements`](https://jlillywh.github.io/SHRINE/extending-elements/#17-publishing-a-third-party-element-shrineelements)
entry-point group (SHRINE roadmap **4.2**).

## Quick start

Install [Cookiecutter](https://cookiecutter.readthedocs.io/), then generate a project:

```bash
pip install cookiecutter
cookiecutter https://github.com/jlillywh/SHRINE --directory shrine-element-cookiecutter
```

From a local SHRINE clone:

```bash
cookiecutter /path/to/SHRINE/shrine-element-cookiecutter
```

You will be prompted for package metadata, element class name, entry-point key, input/output
variable names, and minimum `shrine` version. See
[docs/cookiecutter-element.md](../docs/cookiecutter-element.md) for the full variable table.

## Generated project

The template scaffolds `src/<package>/element.py`, `pyproject.toml` with a `shrine.elements`
entry point, tests, an example script, and a GitHub Actions workflow for your standalone repo.

After generation:

```bash
cd shrine_demand_element   # your project_slug
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python examples/run_demo.py
```

Use the plugin from any SHRINE model:

```python
from shrine.simulation import Model

model = Model()
model.register_plugin("d1", "demand", element_id="d1")
```

## Related docs

- [Cookiecutter element guide](https://jlillywh.github.io/SHRINE/cookiecutter-element/)
- [Extending elements](https://jlillywh.github.io/SHRINE/extending-elements/)
