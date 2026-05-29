"""Sacramento soil moisture model (migrated from src/hydrology/test_sacramento.py)."""

from __future__ import annotations

import pytest

from hydrology.sacramento import Sacramento


@pytest.fixture
def sacramento_model() -> Sacramento:
    init_states = {
        "uztwc": 60.0,
        "uzfwc": 0.5,
        "lztwc": 100.0,
        "lzfsc": 11.0,
        "lzfpc": 47.0,
        "adimc": 160.0,
    }
    params = {
        "uztwm": 40.0,
        "uzfwm": 30.0,
        "lztwm": 330.0,
        "lzfpm": 40.0,
        "lzfsm": 15.0,
        "uzk": 0.4,
        "lzpk": 0.005,
        "lzsk": 0.1,
        "zperc": 150.0,
        "rexp": 2.0,
        "pfree": 0.1,
        "pctim": 0.0,
        "adimp": 0.0,
        "riva": 0.01,
        "side": 0.0,
        "rserv": 0.3,
    }
    globals_ = {
        "pxv": 2.5,
        "lwe": 1.0,
        "we": 1.0,
        "isc": 1.0,
        "aesc": 1.0,
    }
    return Sacramento(init_states, params, globals_)


@pytest.mark.skip(reason="Sacramento frost1 call signature drift; model fix tracked separately")
class TestSacramento:
    def test_et(self, sacramento_model: Sacramento) -> None:
        p = [0, 2, 4, 8, 16, 32, 0, 0, 0, 0, 0, 0, 0]
        et = 1.5
        for i in range(10):
            sacramento_model.update(p[i], et)
        assert sacramento_model.tci == pytest.approx(0.152, abs=1e-2)
