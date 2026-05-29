# PyPI publishing

SHRINE is published to [PyPI](https://pypi.org/project/shrine/) as the **`shrine`** distribution (import name `shrine`). Alternate names (`shrine-wrm`, `shrine-water`) are reserved in the roadmap if the primary name is ever unavailable.

## Install from PyPI

```bash
pip install shrine
pip install "shrine[viz]"              # matplotlib
pip install "shrine[hydrology]"       # NWIS demo deps
pip install "shrine[dev]"               # pytest, mypy, ruff, …
pip install "shrine[dev,viz,hydrology]"
```

After install:

```python
import shrine
import shrine.simulation as sim
print(shrine.__version__, sim.__api_version__)
```

Bundled **scenario YAML/JSON** and the full **tutorial** paths live in the [GitHub repository](https://github.com/jlillywh/SHRINE); clone the repo for `scenarios/` and `./scripts/run_tests.sh`. The PyPI wheel ships the Python packages under `src/` and `examples/`.

## CI

| Workflow | Purpose |
|----------|---------|
| [`.github/workflows/package.yml`](../.github/workflows/package.yml) | Build wheel/sdist; smoke `pip install` on Ubuntu, Windows, macOS |
| [`.github/workflows/publish.yml`](../.github/workflows/publish.yml) | Upload to PyPI when a GitHub **Release** is published |

Local build:

```bash
./scripts/build_package.sh
pip install dist/shrine-*.whl
```

## One-time maintainer setup (PyPI trusted publishing)

1. Create accounts on [PyPI](https://pypi.org/account/register/) and [TestPyPI](https://test.pypi.org/account/register/) (optional dry run).
2. On **PyPI** → **Publishing** → **Add a new pending publisher**:
   - **PyPI Project Name:** `shrine` (create the project on first upload if it does not exist — trusted publisher can be added before first release in PyPI settings)
   - **Owner:** `jlillywh`
   - **Repository name:** `SHRINE`
   - **Workflow name:** `publish.yml`
   - **Environment name:** `pypi` (must match `publish.yml`)
3. In GitHub → **Settings** → **Environments** → create environment **`pypi`** (optional: require reviewers for production releases).
4. Publish a release:
   - Tag `v0.1.0` (or current `shrine.__version__`) on `master`
   - **GitHub** → **Releases** → **Draft a new release** → publish
   - The **Publish** workflow uploads the built artifacts to PyPI

### TestPyPI (optional)

Duplicate the trusted publisher on TestPyPI and add a `testpypi` job/environment, or publish manually once:

```bash
python -m pip install -U twine
twine upload --repository testpypi dist/*
```

## If the name `shrine` is taken

Use the roadmap fallback distribution name (`shrine-wrm` or `shrine-water`) in `pyproject.toml` `[project] name` only — keep the import package `shrine` under `src/shrine/`. Update this doc and PyPI trusted publisher project name.

## Related

- [Install](install.md) — venv and editable installs from source
- [Versioning & releases](releases.md) — SemVer, `CHANGELOG.md`, release checklist (roadmap **3.7**)
- Roadmap **3.8** — document extras after PyPI is live
