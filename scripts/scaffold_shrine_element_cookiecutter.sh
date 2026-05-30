#!/usr/bin/env bash
# One-time scaffold for shrine-element-cookiecutter (run from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="$ROOT/shrine-element-cookiecutter"
PROJ='{{cookiecutter.project_slug}}'
PKG='{{cookiecutter.package_name}}'

rm -rf "$BASE"
mkdir -p "$BASE/hooks"
mkdir -p "$BASE/$PROJ/src/$PKG"
mkdir -p "$BASE/$PROJ/tests"
mkdir -p "$BASE/$PROJ/examples"
mkdir -p "$BASE/$PROJ/.github/workflows"

cat > "$BASE/cookiecutter.json" <<'EOF'
{
  "project_name": "SHRINE Demand Element",
  "project_slug": "shrine_demand_element",
  "package_name": "shrine_demand_element",
  "distribution_name": "shrine-demand-element",
  "element_class_name": "DemandElement",
  "entry_point_name": "demand",
  "element_type": "demand",
  "input_key": "demand",
  "output_variable": "applied",
  "author_name": "Jason Lillywhite",
  "author_email": "you@example.com",
  "github_username": "jlillywh",
  "license": "MIT",
  "shrine_version": "0.2.0",
  "copyright_year": "{% now 'utc', '%Y' %}"
}
EOF

cat > "$BASE/hooks/pre_gen_project.py" <<'EOF'
"""Validate cookiecutter context before generating a SHRINE element package."""

from __future__ import annotations

import re
import sys

IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
CLASS_NAME = re.compile(r"^[A-Z][A-Za-z0-9_]*$")


def _fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def main() -> None:
    context = {
        "project_slug": "{{ cookiecutter.project_slug }}",
        "package_name": "{{ cookiecutter.package_name }}",
        "distribution_name": "{{ cookiecutter.distribution_name }}",
        "entry_point_name": "{{ cookiecutter.entry_point_name }}",
        "element_type": "{{ cookiecutter.element_type }}",
        "input_key": "{{ cookiecutter.input_key }}",
        "output_variable": "{{ cookiecutter.output_variable }}",
        "element_class_name": "{{ cookiecutter.element_class_name }}",
    }

    for field in (
        "project_slug",
        "package_name",
        "entry_point_name",
        "element_type",
        "input_key",
        "output_variable",
    ):
        value = context[field]
        if not IDENTIFIER.match(value):
            _fail(
                f"{field!r} must match {IDENTIFIER.pattern} (lowercase identifier); got {value!r}"
            )

    if context["project_slug"] != context["package_name"]:
        _fail("project_slug and package_name must match for src-layout imports")

    if not CLASS_NAME.match(context["element_class_name"]):
        _fail(
            "element_class_name must be PascalCase (e.g. DemandElement); "
            f"got {context['element_class_name']!r}"
        )

    if not context["distribution_name"].replace("-", "").isalnum():
        _fail(
            "distribution_name must be a PyPI-safe hyphenated name "
            f"(e.g. shrine-demand-element); got {context['distribution_name']!r}"
        )


if __name__ == "__main__":
    main()
EOF

cat > "$BASE/README.md" <<'EOF'
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
EOF

cat > "$BASE/$PROJ/pyproject.toml" <<'EOF'
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "{{ cookiecutter.distribution_name }}"
version = "0.1.0"
description = "{{ cookiecutter.project_name }} — SHRINE Simulatable element plugin"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "{{ cookiecutter.license }}" }
authors = [{ name = "{{ cookiecutter.author_name }}", email = "{{ cookiecutter.author_email }}" }]
dependencies = [
    "shrine>={{ cookiecutter.shrine_version }}",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
]

[project.entry-points."shrine.elements"]
{{ cookiecutter.entry_point_name }} = "{{ cookiecutter.package_name }}.element:{{ cookiecutter.element_class_name }}"

[project.urls]
Homepage = "https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}"
Repository = "https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}"
Issues = "https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
EOF

cat > "$BASE/$PROJ/README.md" <<'EOF'
# {{ cookiecutter.project_name }}

Standalone Python package registering **`{{ cookiecutter.entry_point_name }}`** on the
[`shrine.elements`](https://jlillywh.github.io/SHRINE/extending-elements/#17-publishing-a-third-party-element-shrineelements)
entry-point group.

Generated from [shrine-element-cookiecutter](https://github.com/jlillywh/SHRINE/tree/master/shrine-element-cookiecutter).

## Install

```bash
pip install -e ".[dev]"
```

Requires [SHRINE](https://pypi.org/project/shrine/) `>= {{ cookiecutter.shrine_version }}`.

## Usage

```python
from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController

model = Model(clock=Clock("1/1/2019", "1/6/2019"))
model.register_plugin("d1", "{{ cookiecutter.entry_point_name }}", element_id="d1")

inputs = InputManager()
inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(1.0))

result = RunController(model, input_manager=inputs).run()
print(result.outputs)
```

## Development

```bash
pytest
python examples/run_demo.py
```

## License

{{ cookiecutter.license }} — see [LICENSE](LICENSE).
EOF

cat > "$BASE/$PROJ/LICENSE" <<'EOF'
MIT License

Copyright (c) {{ cookiecutter.copyright_year }} {{ cookiecutter.author_name }}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

cat > "$BASE/$PROJ/src/$PKG/__init__.py" <<'EOF'
"""{{ cookiecutter.project_name }}."""

__version__ = "0.1.0"
EOF

cat > "$BASE/$PROJ/src/$PKG/element.py" <<'EOF'
"""{{ cookiecutter.element_class_name }} — a SHRINE Simulatable element plugin."""

from __future__ import annotations

from shrine.simulation.context import RunContext, TimestepContext


class {{ cookiecutter.element_class_name }}:
    """Reads ``{{ cookiecutter.input_key }}`` and records ``{{ cookiecutter.output_variable }}`` each timestep."""

    element_type = "{{ cookiecutter.element_type }}"

    def __init__(self, element_id: str = "{{ cookiecutter.entry_point_name }}") -> None:
        self.element_id = element_id
        self.{{ cookiecutter.output_variable }} = 0.0

    def initialize(self, run_context: RunContext) -> None:
        if run_context.recorder is not None:
            run_context.recorder.register(f"{self.element_id}.{{ cookiecutter.output_variable }}")

    def update(self, timestep_context: TimestepContext) -> None:
        self.{{ cookiecutter.output_variable }} = float(
            timestep_context.inputs.get("{{ cookiecutter.input_key }}", 0.0)
        )
        if timestep_context.recorder is not None:
            timestep_context.recorder.record(
                f"{self.element_id}.{{ cookiecutter.output_variable }}",
                self.{{ cookiecutter.output_variable }},
            )

    def finalize(self, run_context: RunContext) -> None:
        pass
EOF

cat > "$BASE/$PROJ/tests/test_element.py" <<'EOF'
"""Tests for {{ cookiecutter.element_class_name }}."""

from __future__ import annotations

from {{ cookiecutter.package_name }}.element import {{ cookiecutter.element_class_name }}

from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController


def test_element_records_input() -> None:
    model = Model(clock=Clock("1/1/2019", "1/4/2019"))
    model.register("d1", {{ cookiecutter.element_class_name }}("d1"))

    inputs = InputManager()
    inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(2.5))

    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    assert result.success
    assert result.outputs["d1.{{ cookiecutter.output_variable }}"].iloc[0] == 2.5


def test_register_plugin_runs() -> None:
    model = Model(clock=Clock("1/1/2019", "1/4/2019"))
    model.register_plugin("d1", "{{ cookiecutter.entry_point_name }}", element_id="d1")

    inputs = InputManager()
    inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(1.0))

    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    assert result.success
EOF

cat > "$BASE/$PROJ/tests/test_plugin.py" <<'EOF'
"""Verify the package registers a shrine.elements entry point."""

from __future__ import annotations

from shrine.simulation import create_element_from_plugin, list_element_plugins


def test_entry_point_is_listed() -> None:
    plugins = list_element_plugins()
    assert "{{ cookiecutter.entry_point_name }}" in plugins


def test_entry_point_loads_element() -> None:
    element = create_element_from_plugin("{{ cookiecutter.entry_point_name }}", element_id="d1")
    assert element.element_type == "{{ cookiecutter.element_type }}"
    assert element.element_id == "d1"
EOF

cat > "$BASE/$PROJ/examples/run_demo.py" <<'EOF'
#!/usr/bin/env python3
"""Minimal demo run for {{ cookiecutter.project_name }}."""

from __future__ import annotations

from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController


def main() -> None:
    model = Model(name="{{ cookiecutter.project_name }}", clock=Clock("1/1/2019", "1/6/2019"))
    model.register_plugin("d1", "{{ cookiecutter.entry_point_name }}", element_id="d1")

    inputs = InputManager()
    inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(3.5))

    result = RunController(model, input_manager=inputs).run()
    print(result.outputs)


if __name__ == "__main__":
    main()
EOF

cat > "$BASE/$PROJ/.github/workflows/test.yml" <<'EOF'
name: Tests

on:
  push:
    branches: [master, main]
  pull_request:
    branches: [master, main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install -U pip
          pip install -e ".[dev]"

      - name: Run tests
        run: pytest
EOF

echo "Scaffolded $BASE"
