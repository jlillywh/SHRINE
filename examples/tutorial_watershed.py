#!/usr/bin/env python3
"""Tutorial: build a watershed model, run from scenario, plot outflow (roadmap 3.3).

See docs/tutorial/first-watershed-model.md on the documentation site.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from hydrology.watershed import Watershed
from shrine.simulation import Model, WatershedElement, load_and_run

DEFAULT_SCENARIO = Path(__file__).resolve().parent.parent / "scenarios" / "tutorial_watershed.yaml"


def build_tutorial_model() -> Model:
    """Two catchments draining to a junction — same topology as the tutorial."""
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    model = Model(name="TutorialBasin")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def plot_watershed_results(
    result,
    *,
    output: Path | None = None,
    show: bool = True,
) -> None:
    """Plot basin outflow and total supply vs timestep index."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            'Plotting requires matplotlib. Install with: pip install -e ".[viz]"'
        ) from exc

    outputs = result.outputs
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(outputs.index, outputs["basin.outflow"], label="Outflow (routed)")
    ax.plot(
        outputs.index,
        outputs["basin.total_supply"],
        label="Total supply (catchments)",
        linestyle="--",
        alpha=0.85,
    )
    ax.set_xlabel("Timestep")
    ax.set_ylabel("Flow")
    ax.set_title("Twin-catchment watershed — tutorial scenario")
    ax.legend(loc="best")
    fig.tight_layout()

    if output is not None:
        fig.savefig(output, dpi=120)
        print(f"Wrote plot to {output}")
    if show:
        plt.show()
    elif output is None:
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SHRINE tutorial: watershed model from scenario + plot",
    )
    parser.add_argument(
        "scenario",
        type=Path,
        nargs="?",
        default=DEFAULT_SCENARIO,
        help="Scenario YAML/JSON path (default: scenarios/tutorial_watershed.yaml)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Save plot to this path (PNG/PDF/SVG)",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open an interactive plot window",
    )
    args = parser.parse_args()

    result = load_and_run(build_tutorial_model, args.scenario)
    print(f"status={result.metadata.get('status')} scenario={result.metadata.get('scenario_name')}")
    if not result.success:
        raise SystemExit(result.error)

    print(result.outputs[["basin.outflow", "basin.total_supply"]].head())
    print(f"… {len(result.outputs)} timesteps total")

    plot_watershed_results(result, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
