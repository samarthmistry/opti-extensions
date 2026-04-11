# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Shared test logic for dunder setitem & delitem of VarDict1D & VarDictND."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND

test_cases = [(IndexSet1D(['A', 'B', 'C']), 'A'), (IndexSetND(range(2), range(2)), (0, 0))]


@pytest.mark.parametrize('indexset, key', test_cases)
def test_vardict_setitem_err(model, add_vars_fn, add_vars_kwargs, indexset, key):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(AttributeError):
        v[key] = 1


@pytest.mark.parametrize('indexset, key', test_cases)
def test_vardict_delitem_err(model, add_vars_fn, add_vars_kwargs, indexset, key):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(AttributeError):
        del v[key]
