"""Optional Google Maps elevation demo. Requires a Maps Platform API key."""

import os
import sys
from pathlib import Path

import googlemaps
from gmplot import gmplot
from pint import UnitRegistry

ureg = UnitRegistry()

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_KEY_FILE = _REPO_ROOT / "data_external" / "apikey.txt"


def load_maps_api_key() -> str:
    key = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
    if key:
        return key
    if _DEFAULT_KEY_FILE.is_file():
        return _DEFAULT_KEY_FILE.read_text(encoding="utf-8").strip()
    sys.exit(
        "Set GOOGLE_MAPS_API_KEY or create data_external/apikey.txt "
        "(see data_external/apikey.txt.example). Do not commit API keys."
    )


def main() -> None:
    gmaps = googlemaps.Client(key=load_maps_api_key())
    location = (46.850530, -121.758061)
    elevation_dict = gmaps.elevation(location)
    print(elevation_dict)
    print("-----------")
    elev = elevation_dict[0]["elevation"] * ureg.meter
    elev = elev.to(ureg.ft)

    print(round(elev, 2))

    gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)

    golden_gate_park_lats, golden_gate_park_lons = zip(
        *[
            (37.771269, -122.511015),
            (37.773495, -122.464830),
            (37.774797, -122.454538),
            (37.771988, -122.454018),
            (37.773646, -122.440979),
            (37.772742, -122.440797),
            (37.771096, -122.453889),
            (37.768669, -122.453518),
            (37.766227, -122.460213),
            (37.764028, -122.510347),
            (37.771269, -122.511015),
        ]
    )
    gmap.plot(
        golden_gate_park_lats, golden_gate_park_lons, "cornflowerblue", edge_width=10
    )

    top_attraction_lats, top_attraction_lons = zip(
        *[
            (37.769901, -122.498331),
            (37.768645, -122.475328),
            (37.771478, -122.468677),
            (37.769867, -122.466102),
            (37.767187, -122.467496),
            (37.770104, -122.470436),
        ]
    )
    gmap.scatter(
        top_attraction_lats, top_attraction_lons, "#3B0B39", size=40, marker=False
    )

    hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
    gmap.marker(hidden_gem_lat, hidden_gem_lon, "cornflowerblue")

    gmap.draw("my_map.html")


if __name__ == "__main__":
    main()
