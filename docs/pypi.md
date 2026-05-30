# PyPI publishing

SHRINE is published on [PyPI](https://pypi.org/project/shrine/) as the **`shrine`** distribution (import name `shrine`). **Packaging CI** builds and smoke-tests wheels on every PR; **Publish** uploads on GitHub Release.

Alternate distribution names (`shrine-wrm`, `shrine-water`) are documented below if `shrine` is ever unavailable.

---

## Install from PyPI

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
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

Bundled **scenario YAML/JSON** live in the [GitHub repository](https://github.com/jlillywh/SHRINE) under `scenarios/` — **not** in the PyPI wheel. See [Install — wheel vs clone](install.md#wheel-vs-git-clone--what-you-get). Clone the repo for tutorials and `./scripts/run_tests.sh`. The wheel ships Python packages under `src/` and `examples/`.

---

## CI workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [`package.yml`](https://github.com/jlillywh/SHRINE/blob/master/.github/workflows/package.yml) | push/PR to `master` | Build wheel/sdist; `twine check`; smoke install on Ubuntu, Windows, macOS |
| [`publish.yml`](https://github.com/jlillywh/SHRINE/blob/master/.github/workflows/publish.yml) | GitHub **Release published** | Verify tag vs version; upload to PyPI; matrix `pip install shrine==X` |
| [`publish-testpypi.yml`](https://github.com/jlillywh/SHRINE/blob/master/.github/workflows/publish-testpypi.yml) | Manual (`workflow_dispatch`) | Optional TestPyPI dry run |

Local build:

```bash
./scripts/build_package.sh
pip install dist/shrine-*.whl
python scripts/check_release_version.py --tag v0.2.0
```

---

## One-time maintainer setup (PyPI trusted publishing)

Complete **before** the first GitHub Release.

### PyPI

1. Create an account on [PyPI](https://pypi.org/account/register/).
2. **PyPI** → **Your projects** → (project appears after first upload) or **Publishing** → **Add a new pending publisher**:
   - **PyPI Project Name:** `shrine`
   - **Owner:** `jlillywh`
   - **Repository name:** `SHRINE`
   - **Workflow name:** `publish.yml`
   - **Environment name:** `pypi`
3. **GitHub** → **Settings** → **Environments** → create **`pypi`** (optional: required reviewers for production).

### TestPyPI (optional)

1. Register on [TestPyPI](https://test.pypi.org/account/register/).
2. Add a pending trusted publisher for workflow **`publish-testpypi.yml`**, environment **`testpypi`**.
3. Create GitHub environment **`testpypi`**.
4. Run **Actions** → **Publish (TestPyPI)** → type `testpypi` in the confirmation field.

---

## First release checklist (`v0.2.0`)

Prerequisites: roadmap gates **3.8**, **3.10**, **3.11** met; [GOVERNANCE.md](https://github.com/jlillywh/SHRINE/blob/master/GOVERNANCE.md) and [SECURITY.md](https://github.com/jlillywh/SHRINE/blob/master/SECURITY.md) in place.

1. **Trusted publisher** configured (above).
2. **Version alignment** — must match the release tag:
   - `pyproject.toml` → `[project] version`
   - `src/shrine/__init__.py` → `__version__`
   - Run: `python scripts/check_release_version.py --tag v0.2.0`
3. **Changelog** — move `[Unreleased]` to `[0.2.0] - YYYY-MM-DD` in [CHANGELOG.md](https://github.com/jlillywh/SHRINE/blob/master/CHANGELOG.md).
4. **Verify locally:**
   ```bash
   pip install -e ".[dev]"
   pytest tests/ -q
   ./scripts/build_package.sh
   twine check dist/*
   ```
5. **Commit** on `master`: e.g. `Release v0.2.0`.
6. **Tag and push:**
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0 — first PyPI upload"
   git push origin master v0.2.0
   ```
7. **GitHub Release** — **Releases** → **Draft a new release** → tag `v0.2.0` → paste changelog section → **Publish release**.
8. **Confirm** — **Actions** → **Publish** succeeds; `pip install shrine==0.2.0` works on Linux/macOS/Windows (verify job in workflow).

---

## If the name `shrine` is taken

PyPI returned **404** for `shrine` at first-upload planning (name available). If that changes:

Use fallback distribution name **`shrine-wrm`** or **`shrine-water`** in `pyproject.toml` `[project] name` only — keep import package `shrine` under `src/shrine/`. Update trusted publisher project name, `publish.yml` environment URL, and this doc.

---

## Related

- [Install](install.md) — venv, extras, wheel vs clone
- [Versioning & releases](releases.md) — SemVer, changelog, release checklist
- [Testing & CI](testing.md) — workflows that must pass before a release
