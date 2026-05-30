# Cookiecutter template for SHRINE element plugins

This guide describes **`shrine-element-cookiecutter`**, the official template for bootstrapping a
standalone Python package that registers a custom element on the
[`shrine.elements`](extending-elements.md#17-publishing-a-third-party-element-shrineelements)
entry-point group (roadmap **4.2**).

Related:

- [Extending elements](extending-elements.md) — `Simulatable` contract and adapter patterns
- [Plugin entry points (4.1)](extending-elements.md#17-publishing-a-third-party-element-shrineelements) — runtime discovery API

---

## Generate a project

Install [Cookiecutter](https://cookiecutter.readthedocs.io/):

```bash
pip install cookiecutter
```

From GitHub (monorepo subdirectory):

```bash
cookiecutter https://github.com/jlillywh/SHRINE --directory shrine-element-cookiecutter
```

From a local clone:

```bash
cookiecutter /path/to/SHRINE/shrine-element-cookiecutter
```

Answer the prompts (defaults suit a minimal demand-style element). The hook script
`hooks/pre_gen_project.py` rejects invalid identifiers before files are written.

---

## Template variables

| Variable | Default | Description |
|----------|---------|-------------|
| `project_name` | SHRINE Demand Element | Human-readable title |
| `project_slug` | `shrine_demand_element` | Directory name; must match `package_name` |
| `package_name` | `shrine_demand_element` | Python import path under `src/` |
| `distribution_name` | `shrine-demand-element` | PyPI / pip package name |
| `element_class_name` | `DemandElement` | PascalCase `Simulatable` class |
| `entry_point_name` | `demand` | Key in `[project.entry-points."shrine.elements"]` |
| `element_type` | `demand` | Value of `element_type` on the class |
| `input_key` | `demand` | Default `timestep_context.inputs` key |
| `output_variable` | `applied` | Recorded suffix: `{element_id}.{output_variable}` |
| `author_name` | (your name) | Package author |
| `author_email` | (your email) | Contact email |
| `github_username` | (GitHub user) | Used in `project.urls` |
| `license` | MIT | SPDX license id (MIT recommended) |
| `shrine_version` | `0.2.0` | Minimum `shrine` dependency |
| `copyright_year` | current UTC year | LICENSE file |

All lowercase identifiers (`entry_point_name`, `input_key`, …) must match `^[a-z][a-z0-9_]*$`.

---

## What you get

```
your_project/
  pyproject.toml          # shrine.elements entry point
  src/your_package/
    element.py            # Simulatable implementation
  tests/
    test_element.py       # Model + RunController smoke test
    test_plugin.py        # list_element_plugins / register_plugin
  examples/run_demo.py
  .github/workflows/test.yml
```

After generation:

```bash
cd shrine_demand_element
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
python examples/run_demo.py
```

---

## Publish your package

1. Push the generated project to its **own** GitHub repository (no need to fork SHRINE).
2. Optionally publish to PyPI (`pip install your-distribution-name`).
3. Users install your package, then load the element:

   ```python
   model.register_plugin("d1", "demand", element_id="d1")
   ```

---

## Maintainers

The template source lives in [`shrine-element-cookiecutter/`](../shrine-element-cookiecutter/)
in the SHRINE monorepo. Regenerate from the scaffold script after bulk edits:

```bash
bash scripts/scaffold_shrine_element_cookiecutter.sh
```

CI runs `tests/cookiecutter/test_shrine_element_cookiecutter.py` to cookiecutter-generate a
project, `pip install -e` it, and execute its test suite on every PR.
