"""Smoke tests for tutorial example (roadmap 3.3)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from examples.tutorial_watershed import build_tutorial_model, plot_watershed_results

from shrine.simulation import load_and_run

REPO_ROOT = Path(__file__).resolve().parents[2]
TUTORIAL_SCENARIO = REPO_ROOT / "scenarios" / "tutorial_watershed.yaml"


@pytest.mark.skipif(
    importlib.util.find_spec("matplotlib") is None,
    reason="matplotlib not installed",
)
def test_tutorial_watershed_run_and_plot(tmp_path: Path) -> None:
    result = load_and_run(build_tutorial_model, TUTORIAL_SCENARIO)
    assert result.success
    assert result.metadata["scenario_name"] == "tutorial_watershed"
    assert "basin.outflow" in result.outputs.columns
    # Jan 1 – Mar 31 2019 (non-leap): 31 + 28 + 31 timesteps
    assert len(result.outputs) == 90
    outflow = result.outputs["basin.outflow"]
    assert outflow.iloc[0] != outflow.iloc[32]  # Jan vs Feb monthly step

    plot_path = tmp_path / "tutorial.png"
    plot_watershed_results(result, output=plot_path, show=False)
    assert plot_path.is_file()
