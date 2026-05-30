"""Validate cookiecutter context before generating a SHRINE element package."""

from __future__ import annotations

import re
import sys

IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
CLASS_NAME = re.compile(r"^[A-Z][A-Za-z0-9_]*$")


def _fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def main() -> None:
    context = {
        "project_slug": "{{ cookiecutter.project_slug }}",
        "package_name": "{{ cookiecutter.package_name }}",
        "distribution_name": "{{ cookiecutter.distribution_name }}",
        "entry_point_name": "{{ cookiecutter.entry_point_name }}",
        "element_type": "{{ cookiecutter.element_type }}",
        "input_key": "{{ cookiecutter.input_key }}",
        "output_variable": "{{ cookiecutter.output_variable }}",
        "element_class_name": "{{ cookiecutter.element_class_name }}",
    }

    for field in (
        "project_slug",
        "package_name",
        "entry_point_name",
        "element_type",
        "input_key",
        "output_variable",
    ):
        value = context[field]
        if not IDENTIFIER.match(value):
            _fail(
                f"{field!r} must match {IDENTIFIER.pattern} (lowercase identifier); got {value!r}"
            )

    if context["project_slug"] != context["package_name"]:
        _fail("project_slug and package_name must match for src-layout imports")

    if not CLASS_NAME.match(context["element_class_name"]):
        _fail(
            "element_class_name must be PascalCase (e.g. DemandElement); "
            f"got {context['element_class_name']!r}"
        )

    if not context["distribution_name"].replace("-", "").isalnum():
        _fail(
            "distribution_name must be a PyPI-safe hyphenated name "
            f"(e.g. shrine-demand-element); got {context['distribution_name']!r}"
        )


if __name__ == "__main__":
    main()
