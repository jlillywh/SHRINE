#!/usr/bin/env python3
"""Fetch USGS NWIS daily values for one site (hydrofunctions demo).

Requires the optional hydrology extra::

    pip install -e ".[hydrology]"

Not part of the ``hydrology`` package API — run as a script only.
"""

from __future__ import annotations

import hydrofunctions as hf

SITE_ID = "13011000"


def main() -> None:
    snake = hf.NWIS(SITE_ID, "dv", period="P55D")
    snake.get_data()
    print(snake.df().head())
    print(snake.start_date)
    print(snake.end_date)


if __name__ == "__main__":
    main()
