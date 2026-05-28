import warnings

import pytest

from global_attributes.model import LegacyModel, Model


def test_legacy_model_instantiates_without_warning():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", DeprecationWarning)
        m = LegacyModel()
    assert m.clock is not None
    assert m.listSet is not None
    assert not any(
        issubclass(w.category, DeprecationWarning) for w in caught
    )


def test_model_alias_emits_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="global_attributes.Model"):
        m = Model()
    assert m.clock is not None
