"""Smoke-test the shrine-element-cookiecutter template (roadmap 4.2)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "shrine-element-cookiecutter"

COOKIE_EXTRA_CONTEXT = {
    "project_name": "Test Cookie Element",
    "project_slug": "test_cookie_element",
    "package_name": "test_cookie_element",
    "distribution_name": "test-cookie-element",
    "element_class_name": "TestDemandElement",
    "entry_point_name": "test_cookie_demand",
    "element_type": "test_demand",
    "input_key": "demand",
    "output_variable": "applied",
    "author_name": "Test User",
    "author_email": "test@example.com",
    "github_username": "testuser",
    "license": "MIT",
    "shrine_version": "0.2.0",
    "copyright_year": "2026",
}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("entry_point_name", "Bad-Name"),
        ("element_class_name", "bad_class"),
    ],
)
def test_pre_gen_hook_rejects_invalid_context(
    field: str,
    value: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pytest.importorskip("cookiecutter")
    from cookiecutter.main import cookiecutter

    context = {**COOKIE_EXTRA_CONTEXT, field: value}
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    with pytest.raises(Exception):
        cookiecutter(
            str(TEMPLATE),
            no_input=True,
            extra_context=context,
            output_dir=str(output_dir),
        )


def test_cookiecutter_generates_installable_plugin_package(tmp_path: Path) -> None:
    pytest.importorskip("cookiecutter")
    from cookiecutter.main import cookiecutter

    output_dir = tmp_path / "generated"
    output_dir.mkdir()
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE),
            no_input=True,
            extra_context=COOKIE_EXTRA_CONTEXT,
            output_dir=str(output_dir),
        )
    )

    assert project_dir.name == COOKIE_EXTRA_CONTEXT["project_slug"]
    assert (project_dir / "src" / "test_cookie_element" / "element.py").is_file()

    install = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", f"{project_dir}[dev]"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert install.returncode == 0, install.stderr

    tests = subprocess.run(
        [sys.executable, "-m", "pytest", str(project_dir / "tests"), "-q"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert tests.returncode == 0, tests.stdout + tests.stderr
