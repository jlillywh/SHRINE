"""Golden-run regression: fixed scenario file → stable hash of ``result.outputs``."""

from __future__ import annotations

from pathlib import Path

from hydrology.watershed import Watershed
from shrine.simulation import (
    Clock,
    Model,
    WatershedElement,
    load_scenario_file,
    run_scenario,
)
from shrine.simulation.golden import outputs_content_hash
from tests.path_fixtures import REPO_ROOT

GOLDEN_DIR = Path(__file__).resolve().parent.parent / "golden"
BASELINE_SCENARIO = REPO_ROOT / "scenarios" / "baseline_watershed.json"
BASELINE_HASH_FILE = GOLDEN_DIR / "baseline_watershed.outputs.sha256"


def _watershed_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="GoldenWatershed", clock=Clock("1/1/2019", "1/10/2019"))
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


class TestGoldenRun:
    def test_baseline_watershed_outputs_hash(self) -> None:
        assert BASELINE_SCENARIO.is_file(), f"missing scenario: {BASELINE_SCENARIO}"
        assert BASELINE_HASH_FILE.is_file(), f"missing golden hash: {BASELINE_HASH_FILE}"

        scenario = load_scenario_file(BASELINE_SCENARIO)
        result = run_scenario(_watershed_model(), scenario, raise_on_error=False)
        assert result.success, result.error

        digest = outputs_content_hash(result.outputs)
        expected = BASELINE_HASH_FILE.read_text(encoding="utf-8").strip()
        assert digest == expected, (
            f"outputs hash changed for {BASELINE_SCENARIO.name}; "
            f"expected {expected}, got {digest}. "
            "If intentional, run: python scripts/update_golden_outputs.py"
        )

    def test_outputs_content_hash_is_deterministic(self) -> None:
        scenario = load_scenario_file(BASELINE_SCENARIO)
        model = _watershed_model()
        r1 = run_scenario(model, scenario, raise_on_error=False)
        r2 = run_scenario(_watershed_model(), scenario, raise_on_error=False)
        assert outputs_content_hash(r1.outputs) == outputs_content_hash(r2.outputs)
