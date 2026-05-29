"""DEPRECATED legacy unittest aggregator (roadmap 2.11).

Hydrology and water_manage colocated tests were removed after migration to
``tests/hydrology/`` and ``tests/water_manage/``. Other ``src/*/test_*.py``
modules remain deprecated until migrated.

Run the canonical suite::

    pytest tests/
"""

from __future__ import annotations

import sys

from testing.colocated import deprecate_colocated_module

deprecate_colocated_module(
    path="global_attributes.test_suite",
    migrated_to="tests/hydrology/, tests/water_manage/, tests/global_attributes/",
)


def main() -> int:
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
