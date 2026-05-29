"""Repo-relative paths for legacy domain tests (importable without pytest)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
HYDROLOGY_TEST_DATA = SRC_ROOT / "hydrology" / "test_data"
WATER_MANAGE_TEST_DATA = SRC_ROOT / "water_manage" / "test_data"
WATERSHED_GML = HYDROLOGY_TEST_DATA / "watershed_GML_input.gml"
NETWORK_GML = WATER_MANAGE_TEST_DATA / "network_GML_input.gml"
