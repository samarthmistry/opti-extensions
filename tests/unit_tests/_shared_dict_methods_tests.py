# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Shared test logic for dict methods of VarDict1D & VarDictND.

Each solver backend imports and calls these functions, passing its own
model fixture and ``add_vars_fn`` / keyword arguments.
"""

import pytest

from opti_extensions import IndexSet1D, IndexSetND

DISABLED_METHODS = ['clear', 'copy', 'pop', 'popitem', 'setdefault', 'update', 'fromkeys']

GET_CASES = [
    (IndexSet1D(['A', 'B', 'C']), 'A', None, True),
    (IndexSet1D(['A', 'B', 'C']), 'A', -1, True),
    (IndexSet1D(['A', 'B', 'C']), 'Z', None, False),
    (IndexSet1D(['A', 'B', 'C']), 'Z', -1, False),
    (IndexSetND(range(2), range(2)), (0, 0), None, True),
    (IndexSetND(range(2), range(2)), (0, 0), -1, True),
    (IndexSetND(range(2), range(2)), (0, 9), None, False),
    (IndexSetND(range(2), range(2)), (0, 9), -1, False),
]


def make_vardict(model, add_vars_fn, indexset, add_vars_kwargs):
    """Create a VarDict via the solver's add_variables function."""
    return add_vars_fn(model, indexset, **add_vars_kwargs)


@pytest.mark.parametrize('method', DISABLED_METHODS)
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_attrerr(model, add_vars_fn, add_vars_kwargs, indexset, method):
    v = make_vardict(model, add_vars_fn, indexset, add_vars_kwargs)
    with pytest.raises(AttributeError):
        getattr(v, method)()


@pytest.mark.parametrize('indexset, key, default, present', GET_CASES)
def test_vardict_get_pass(model, add_vars_fn, add_vars_kwargs, indexset, key, default, present):
    v = make_vardict(model, add_vars_fn, indexset, add_vars_kwargs)
    value = v.get(key, default)
    if present:
        assert value is v[key]
    else:
        assert value == default
