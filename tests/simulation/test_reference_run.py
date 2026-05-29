"""Golden-run regression for scenarios/reference/ (roadmap 3.10)."""

from __future__ import annotations

from pathlib import Path

import pytest

from shrine.simulation import load_scenario_file, run_scenario
from shrine.simulation.golden import outputs_content_hash
from tests.path_fixtures import REPO_ROOT
from tests.reference.manifest import REFERENCE_CASES

GOLDEN_DIR = Path(__file__).resolve().parent.parent / "golden" / "reference"


@pytest.mark.parametrize(
    "case",
    REFERENCE_CASES,
    ids=[Path(c.scenario).stem for c in REFERENCE_CASES],
)
def test_reference_scenario_outputs(case) -> None:
    scenario_path = REPO_ROOT / case.scenario
    hash_path = GOLDEN_DIR / case.golden
    assert scenario_path.is_file(), f"missing scenario: {scenario_path}"
    assert hash_path.is_file(), f"missing golden hash: {hash_path}"

    scenario = load_scenario_file(scenario_path)
    result = run_scenario(case.builder(), scenario, raise_on_error=False)
    assert result.success, result.error

    if case.expected_first_outflow is not None:
        first = float(result.outputs["basin.outflow"].iloc[0])
        assert first == pytest.approx(case.expected_first_outflow, rel=1e-5)

    digest = outputs_content_hash(result.outputs)
    expected = hash_path.read_text(encoding="utf-8").strip()
    assert digest == expected, (
        f"outputs hash changed for {scenario_path.name}; "
        f"expected {expected}, got {digest}. "
        "If intentional, run: python scripts/update_reference_golden.py"
    )
