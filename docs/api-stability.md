# API stability policy

This document defines versioning and deprecation rules for **`shrine.simulation`** and related public surfaces.

Related:

- [README](https://github.com/jlillywh/SHRINE/blob/master/README.md) — public API table
- [Versioning & releases](releases.md) — SemVer, changelog, maintainer release checklist
- [modernization-roadmap.md](modernization-roadmap.md) — Phase 1 hardening
- [architecture.md](architecture.md) — framework vs domain layers

---

## Two version numbers

| Symbol | Example | Meaning |
|--------|---------|---------|
| `shrine.__version__` | `0.1.0` | **Distribution** version (PyPI / `pip install`, SemVer) |
| `shrine.simulation.__api_version__` | `1.0` | **Simulation public API** version (symbols in `shrine.simulation.__all__`) |

- Bump **`__version__`** for any release (fixes, features, breaking changes per SemVer below).
- Bump **`__api_version__`** when the **documented public simulation API** changes incompatibly (major segment) or when deprecations are introduced (minor segment).

While `shrine.__version__` is `0.x`, the project is pre–1.0: breaking simulation API changes are allowed but must follow the **deprecation cycle** in this document.

---

## What is public API?

**Stable (supported):**

- Every name in `shrine.simulation.__all__`
- Behavior described in `docs/` for those symbols (requirements, scenarios, extending-elements)

**Not stable (internal):**

- Any other `shrine.simulation.*` submodule import (e.g. `run_controller`, `metadata`) unless explicitly listed as an extension point in [extending-elements.md](extending-elements.md)
- Legacy packages (`hydrology/`, `global_attributes/`, …) except where a deprecated alias is documented
- Underscore-prefixed names (`_execute_run`, etc.)

**Domain code** (`hydrology.Watershed`, `water_manage.Store`, …) has no stability guarantee until wrapped by a `shrine.simulation` adapter.

---

## Semantic versioning (`shrine.__version__`)

Given version **MAJOR.MINOR.PATCH**:

| Change | Version bump | Example |
|--------|--------------|---------|
| Bug fix, docs only | PATCH | `0.1.0` → `0.1.1` |
| New backward-compatible API | MINOR | `0.1.1` → `0.2.0` |
| Breaking change to public API (after deprecation cycle) | MAJOR | `0.2.0` → `1.0.0` |

Pre-1.0 (`0.y.z`): MINOR may include small breaking changes **only** if the deprecation cycle was satisfied or the change is clearly marked experimental.

---

## Deprecation cycle (one minor release)

When removing or renaming a symbol in `shrine.simulation.__all__`:

1. **Introduce** the replacement (if any) in the same or earlier release.
2. **Deprecate** the old symbol: keep it working, emit `DeprecationWarning` on use (instantiation, call, or import side effect as appropriate).
3. **Document** in [CHANGELOG](https://github.com/jlillywh/SHRINE/blob/master/CHANGELOG.md) under `Deprecated` and in the symbol’s docstring.
4. **Wait** at least **one minor** distribution release (`0.N` → `0.N+1`) with warnings enabled.
5. **Remove** in the next **minor** release after that warning period (or bump `__api_version__` major and `shrine` MAJOR when reaching 1.0).

### Timeline example

| Release | `__version__` | `__api_version__` | Action |
|---------|---------------|-------------------|--------|
| A | `0.2.0` | `1.0` | Add `new_run()` |
| B | `0.3.0` | `1.1` | Deprecate `old_run()`; warn → use `new_run()` |
| C | `0.4.0` | `2.0` | Remove `old_run()` |

Between B and C, `old_run()` must remain importable and functional.

### How to emit warnings (maintainers)

Use the shared helper:

```python
from shrine.simulation import warn_api_deprecated

warn_api_deprecated(
    "old_run",
    replacement="new_run",
    removed_in_api="2.0",
)
```

Legacy `global_attributes` aliases (`Model`, `Clock`) follow the same **user-visible** rule: `DeprecationWarning` on use, documented in CHANGELOG (see repo root).

---

## Exceptions and additions

| Change type | Policy |
|-------------|--------|
| New symbol in `__all__` | MINOR `__version__`; optional MINOR `__api_version__` |
| New optional argument with default | MINOR, no deprecation |
| Stricter validation (reject previously accepted bad input) | MINOR or MAJOR; note in CHANGELOG (repo root) |
| Bug fix that changes numerics | PATCH; mention in CHANGELOG if material |
| Scenario file schema | Document in [scenarios.md](scenarios.md); treat unknown keys per validation policy (1.3) |

---

## For downstream users

- Pin `shrine` in applications: `shrine>=0.1,<0.2` (adjust as releases ship).
- Run tests with warnings visible:

  ```bash
  pytest -W default::DeprecationWarning tests/simulation
  ```

- Prefer `from shrine.simulation import …` over deep imports.
- Do not build on `global_attributes.Model` / `global_attributes.Clock`; use `shrine.simulation` types.

---

## Changelog and releases

Every release that deprecates or removes API surface must update **[CHANGELOG.md](https://github.com/jlillywh/SHRINE/blob/master/CHANGELOG.md)** with:

- `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed`
- Affected `__api_version__` when simulation public API changes

Maintainer workflow (tagging, version bumps, GitHub Release): [Versioning & releases](releases.md).

Git tags should match `shrine.__version__` (e.g. `v0.2.0`).
