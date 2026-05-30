#!/usr/bin/env python3
"""Generate mkdocstrings API pages from ``shrine.simulation`` public exports (roadmap 3.2)."""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTOGEN_DIR = ROOT / "docs" / "api" / "autogen"

# Mirrors categories in ``shrine.simulation`` package docstring / ``__all__``.
API_GROUPS: list[tuple[str, str, list[str]]] = [
    (
        "run-orchestration",
        "Run orchestration",
        [
            "Model",
            "RegisteredElement",
            "RunController",
            "RunResult",
            "RunSession",
            "StepResult",
            "ElementScheduler",
        ],
    ),
    (
        "time-and-context",
        "Time and context",
        ["Clock", "RunContext", "TimestepContext"],
    ),
    (
        "units",
        "Units",
        ["get_default_units", "get_unit_registry", "validate_unit_string"],
    ),
    (
        "elements",
        "Elements and adapters",
        [
            "Simulatable",
            "WatershedElement",
            "CatchmentElement",
            "ReservoirElement",
            "ClimateRecorderElement",
            "StorageElement",
            "StorageLike",
            "ELEMENTS_ENTRY_POINT_GROUP",
            "ElementPlugin",
            "list_element_plugins",
            "load_element_plugin",
            "create_element_from_plugin",
        ],
    ),
    (
        "inputs",
        "Inputs",
        [
            "InputManager",
            "InputProvider",
            "ConstantInput",
            "MonthlyLookupInput",
            "StochasticInput",
            "TimeSeriesCsvInput",
            "load_csv_timeseries",
            "bind_csv_columns",
        ],
    ),
    (
        "flow-balance",
        "Flow and mass balance",
        [
            "FlowSolver",
            "NetworkXFlowSolver",
            "FlowSolveResult",
            "MassBalanceCheck",
            "MassBalanceReport",
            "MassBalanceTerm",
        ],
    ),
    (
        "scenarios",
        "Scenarios and recording",
        [
            "Recorder",
            "export_run_result",
            "ScenarioConfig",
            "load_scenario_file",
            "run_scenario",
            "run_scenarios",
            "load_and_run",
        ],
    ),
    (
        "metadata",
        "Metadata, manifest, and RNG",
        [
            "build_run_metadata",
            "build_run_manifest",
            "attach_output_units",
            "enrich_run_metadata",
            "element_list_from_model",
            "resolve_git_commit",
            "scenario_content_hash",
            "outputs_content_hash",
            "RunTimer",
            "make_rng",
        ],
    ),
    (
        "errors",
        "Errors and deprecation",
        ["SimulationError", "SimulationPhase", "warn_api_deprecated"],
    ),
]

MKDOCSTRINGS_OPTIONS = """\
    options:
      heading_level: 4
      show_root_heading: false
      show_if_no_docstring: true
      inherited_members: true
      merge_init_into_class: true
      separate_signature: true
      show_signature_annotations: true
      summary: true
"""


def _qualified_name(obj: Any, export_name: str) -> str:
    if inspect.ismodule(obj):
        return obj.__name__
    if inspect.isclass(obj) or inspect.isfunction(obj):
        return f"{obj.__module__}.{obj.__qualname__}"
    return f"shrine.simulation.{export_name}"


def _render_group_page(simulation: Any, slug: str, title: str, symbols: list[str]) -> str:
    lines = [
        f"# {title}",
        "",
        "Auto-generated from ``shrine.simulation`` docstrings. "
        "Regenerate with ``python scripts/gen_api_reference.py``.",
        "",
    ]
    seen: set[str] = set()
    for name in symbols:
        obj = getattr(simulation, name)
        qname = _qualified_name(obj, name)
        dedupe_key = f"{name}:{qname}"
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        lines.append(f"## `{name}`")
        lines.append("")
        lines.append(f"::: {qname}")
        lines.append(MKDOCSTRINGS_OPTIONS.strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _import_simulation() -> Any:
    src = ROOT / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    import shrine.simulation as simulation  # noqa: PLC0415

    return simulation


def _validate_coverage(simulation: Any) -> None:
    documented = {name for _, _, names in API_GROUPS for name in names}
    exported = set(simulation.__all__)
    version_symbols = {"__api_version__", "__framework_version__"}
    missing = sorted(exported - documented - version_symbols)
    extra = sorted(documented - exported)
    if missing:
        raise SystemExit(f"API_GROUPS missing __all__ symbols: {missing}")
    if extra:
        raise SystemExit(f"API_GROUPS contains symbols not in __all__: {extra}")


def main() -> None:
    simulation = _import_simulation()
    _validate_coverage(simulation)

    AUTOGEN_DIR.mkdir(parents=True, exist_ok=True)
    for path in AUTOGEN_DIR.glob("*.md"):
        if path.name != "README.md":
            path.unlink()

    nav_entries: list[tuple[str, str]] = []
    for slug, title, symbols in API_GROUPS:
        content = _render_group_page(simulation, slug, title, symbols)
        out_path = AUTOGEN_DIR / f"{slug}.md"
        out_path.write_text(content, encoding="utf-8")
        nav_entries.append((title, f"api/autogen/{slug}.md"))

    readme = AUTOGEN_DIR / "README.md"
    readme.write_text(
        "# Autogenerated API pages\n\n"
        "Do not edit `*.md` here by hand. Run `python scripts/gen_api_reference.py`.\n",
        encoding="utf-8",
    )

    nav_path = AUTOGEN_DIR / "nav-snippet.yml"
    nav_lines = ["  # Autogenerated nav (copy into mkdocs.yml when groups change):"]
    for title, href in nav_entries:
        nav_lines.append(f"      - {title}: {href}")
    nav_path.write_text("\n".join(nav_lines) + "\n", encoding="utf-8")

    print(f"Wrote {len(nav_entries)} API pages to {AUTOGEN_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
