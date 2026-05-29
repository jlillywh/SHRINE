"""DEPRECATED heavy/Monte Carlo unittest suite placeholder (roadmap 2.11).

Prefer ``pytest tests/`` for automated runs. Migrate long-running checks to
``tests/`` with explicit markers (e.g. ``@pytest.mark.slow``) when needed.
"""

from __future__ import annotations

from testing.colocated import deprecate_colocated_module

deprecate_colocated_module(path="global_attributes.test_suite_heavy")
