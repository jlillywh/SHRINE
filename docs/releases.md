# Versioning & releases

SHRINE uses [Semantic Versioning 2.0](https://semver.org/) for the **distribution** version (`shrine.__version__`) and documents every release in **[CHANGELOG.md](https://github.com/jlillywh/SHRINE/blob/master/CHANGELOG.md)** ([Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format).

Simulation API stability (`shrine.simulation.__api_version__`, deprecation cycles, public surface) is defined separately in [API stability](api-stability.md).

---

## Two version numbers

| Symbol | Example | When it changes |
|--------|---------|-----------------|
| `shrine.__version__` | `0.2.0` | Every tagged release (SemVer below) |
| `shrine.simulation.__api_version__` | `1.0` | Breaking or deprecating changes to `shrine.simulation.__all__` |

Both are exposed at import time:

```python
import shrine
import shrine.simulation as sim

print(shrine.__version__, sim.__api_version__)
```

---

## Semantic versioning (`shrine.__version__`)

Given **MAJOR.MINOR.PATCH**:

| Change | Bump | Example |
|--------|------|---------|
| Bug fix, docs-only, internal refactor | **PATCH** | `0.1.0` → `0.1.1` |
| New backward-compatible feature | **MINOR** | `0.1.1` → `0.2.0` |
| Breaking change to supported public API (after deprecation cycle) | **MAJOR** | `0.9.0` → `1.0.0` |

### Pre-1.0 (`0.y.z`)

While `shrine.__version__` starts with `0`, the project is **alpha**. MINOR releases may include small breaking changes if:

- the [deprecation cycle](api-stability.md#deprecation-cycle-one-minor-release) was satisfied, or
- the change is clearly experimental and noted under **Changed** or **Removed** in the changelog.

Do not treat `0.x` as “no semver” — downstream users still pin versions (`shrine>=0.2,<0.3`).

---

## Changelog (`CHANGELOG.md`)

The changelog lives at the [repository root](https://github.com/jlillywh/SHRINE/blob/master/CHANGELOG.md). Follow [Keep a Changelog 1.1](https://keepachangelog.com/en/1.1.0/):

1. **`[Unreleased]`** — work merged to `master` but not yet tagged.
2. **`[X.Y.Z] - YYYY-MM-DD`** — one section per release, newest first.
3. **Categories** (use only sections that apply):
   - **Added** — new features
   - **Changed** — behavior changes in existing functionality
   - **Deprecated** — soon-to-be removed
   - **Removed** — removed in this release
   - **Fixed** — bug fixes
   - **Security** — vulnerability fixes

### What to record

| Audience | Include |
|----------|---------|
| **Users** | Public API, scenario schema, install extras, documented behavior |
| **Contributors** | CI, tooling, test layout — when it affects how to develop or release |
| **Simulation API** | Note `__api_version__` when `shrine.simulation.__all__` changes |

Every PR that changes user-visible behavior should add a line under **`[Unreleased]`** (or the maintainer adds it at release time).

### Compare links

At the bottom of `CHANGELOG.md`, keep version links in Keep a Changelog style:

```markdown
[Unreleased]: https://github.com/jlillywh/SHRINE/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jlillywh/SHRINE/releases/tag/v0.1.0
```

Update `[Unreleased]` when cutting a new tag (point the left side at the previous release).

---

## Release checklist (maintainers)

Use this when publishing **`vX.Y.Z`** on GitHub (and optionally PyPI — see [PyPI publishing](pypi.md)).

1. **Changelog**
   - Move `[Unreleased]` entries into `[X.Y.Z] - YYYY-MM-DD`.
   - Add a fresh empty `[Unreleased]` section.
   - Update compare links at the bottom.

2. **Version strings** (must match the tag):
   - `pyproject.toml` → `[project] version`
   - `src/shrine/__init__.py` → `__version__`

3. **Verify locally**

   ```bash
   pip install -e ".[dev]"
   pytest tests/ -q
   ./scripts/build_package.sh    # when packaging CI is enabled
   ```

4. **Commit** on `master`: e.g. `Release v0.2.0`.

5. **Tag** (annotated tag recommended):

   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin master v0.2.0
   ```

6. **GitHub Release**
   - **Releases** → **Draft a new release** → choose tag `v0.2.0`.
   - Paste the `[X.Y.Z]` section from `CHANGELOG.md` as the release notes.
   - Publish (triggers [PyPI upload](pypi.md) when trusted publishing is configured).

7. **Post-release**
   - Open `[Unreleased]` on `master` for the next cycle.
   - Bump to next dev version only if the project uses a explicit pre-release scheme (optional; SHRINE typically stays at the released number until the next release PR).

### Tag naming

- Git tag: **`v` + SemVer** (e.g. `v0.1.0`, `v0.2.0`).
- Must equal `shrine.__version__` with a `v` prefix.

---

## Supported versions

| Version | Status |
|---------|--------|
| `0.2.x` | **Alpha** — active development on `master` |
| `0.1.x` | Superseded by `0.2.0` |
| Pre-`0.1.0` | Not supported |

Security reporting will be formalized in roadmap **3.18** (`SECURITY.md`). Until then, open a [GitHub issue](https://github.com/jlillywh/SHRINE/issues) or contact maintainers privately for sensitive reports.

---

## Related

- [API stability](api-stability.md) — `__api_version__`, deprecation warnings, public surface
- [PyPI publishing](pypi.md) — packaging CI live; first upload deferred until **3.8** + P1 gates (**3.6** part 2)
- [Testing & CI](testing.md) — workflows that must pass before a release
- [CHANGELOG.md](https://github.com/jlillywh/SHRINE/blob/master/CHANGELOG.md) — full history
