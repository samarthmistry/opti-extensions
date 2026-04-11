# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Shared test logic for custom methods of VarDict1D & VarDictND.

Solver-specific conftest files provide the following fixtures:
- ``model``: The solver model instance
- ``add_vars_fn``: The function to create variables
- ``add_vars_kwargs``: Default kwargs for creating variables
- ``sum_fn``: Solver's sum function for verification
- ``has_sum_squares``: Whether sum_squares is supported
- ``needs_update``: Whether model.update() is needed (gurobipy)
"""

import pytest

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND

# ---- lookup tests ----

LOOKUP_1D_CASES = [
    (IndexSet1D(['A', 'B', 'C']), 'A', True),
    (IndexSet1D(['A', 'B', 'C']), 'Z', False),
]

LOOKUP_ND_CASES = [
    (IndexSetND(range(2), range(2)), (0, 0), True),
    (IndexSetND(range(2), range(2)), (0, 9), False),
    (IndexSetND(['A', 'B', 'C'], range(2)), ('A', 0), True),
    (IndexSetND(['A', 'B', 'C'], range(2)), ('Z', 0), False),
]


@pytest.mark.parametrize('indexset, key, present', LOOKUP_1D_CASES)
def test_vardict1d_lookup_pass(model, add_vars_fn, add_vars_kwargs, indexset, key, present):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    value = v.lookup(key)
    if present:
        assert value is v[key]
    else:
        assert value == 0


@pytest.mark.parametrize('indexset, key, present', LOOKUP_ND_CASES)
def test_vardictNd_lookup_pass(model, add_vars_fn, add_vars_kwargs, indexset, key, present):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    value = v.lookup(*key)
    if present:
        assert value is v[key]
    else:
        assert value == 0


@pytest.mark.parametrize('key', [[13], (0, 0), ()])
def test_vardictNd_lookup_typerr(model, add_vars_fn, add_vars_kwargs, key):
    v = add_vars_fn(model, IndexSetND(range(2), range(2)), **add_vars_kwargs)
    with pytest.raises(TypeError):
        v.lookup(key)


@pytest.mark.parametrize('key', [(), (0, 0, 0), (1, 2, 3, 4)])
def test_vardictNd_lookup_valerr(model, add_vars_fn, add_vars_kwargs, key):
    v = add_vars_fn(model, IndexSetND(range(2), range(2)), **add_vars_kwargs)
    with pytest.raises(ValueError):
        v.lookup(*key)


# ---- sum partial pattern tests ----

SUM_PARTIAL_PASS_CASES = [
    [IndexSetND(range(2), range(2)), (0, '*')],
    [IndexSetND(range(2), range(2)), ('*', 0)],
    [IndexSetND(range(2), range(2)), (9, '*')],
    [IndexSetND(['A', 'B', 'C'], range(2)), ('A', '*')],
    [IndexSetND(['A', 'B', 'C'], range(2)), ('*', 0)],
    [IndexSetND(['A', 'B', 'C'], range(2)), ('*', 'Z')],
    [IndexSetND(['A', 'B', 'C'], [0]), ('B', '*')],
]

SUM_PARTIAL_VALERR_CASES = [
    [IndexSetND(range(2), range(2)), (0, 0)],
    [IndexSetND(range(2), range(2)), ('*', '*')],
    [IndexSetND(range(2), range(2)), (0, 0, 0)],
]


@pytest.mark.parametrize('indexset, pattern', SUM_PARTIAL_VALERR_CASES)
def test_vardictNd_sum_partial_valerr(model, add_vars_fn, add_vars_kwargs, indexset, pattern):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(ValueError):
        v.sum(*pattern)


# ---- dot product tests ----

DOT_PASS_CASES = [
    (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'A': 1, 'B': 2, 'C': 3})),
    (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'A': 1, 'B': 2})),
    (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'A': 1, 'B': 2, 'X': 9})),
    (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'X': 9})),
    (IndexSet1D(range(3)), ParamDict1D({0: 0, 1: 10, 2: 20})),
    (IndexSet1D(range(3)), ParamDict1D({0: 0, 1: 10})),
    (IndexSet1D(range(3)), ParamDict1D({0: 0, 1: 10, 9: 90})),
    (IndexSet1D(range(3)), ParamDict1D({9: 90})),
    (IndexSetND(range(2), range(2)), ParamDictND({(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2})),
    (IndexSetND(range(2), range(2)), ParamDictND({(0, 0): 0, (0, 1): 1, (1, 0): 1})),
    (IndexSetND(range(2), range(2)), ParamDictND({(0, 0): 0, (0, 1): 1, (1, 0): 1, (9, 9): 9})),
    (IndexSetND(range(2), range(2)), ParamDictND({(9, 9): 9})),
    (
        IndexSetND(['A', 'B'], range(2)),
        ParamDictND({('A', 0): 6, ('B', 0): 7, ('A', 1): 8, ('B', 1): 9}),
    ),
    (IndexSetND(['A', 'B'], range(2)), ParamDictND({('A', 0): 6, ('B', 0): 7, ('A', 1): 8})),
    (
        IndexSetND(['A', 'B'], range(2)),
        ParamDictND({('A', 0): 6, ('B', 0): 7, ('A', 1): 8, ('X', 9): 9}),
    ),
    (IndexSetND(['A', 'B'], range(2)), ParamDictND({('X', 9): 9})),
]


@pytest.mark.parametrize('indexset, paramdict', DOT_PASS_CASES)
def test_vardict_dot_pass(model, add_vars_fn, add_vars_kwargs, sum_fn, indexset, paramdict):
    vardict = add_vars_fn(model, indexset, **add_vars_kwargs)
    res = sum_fn(paramdict.get(k, 0) * v for k, v in vardict.items())

    assert str(vardict.dot(paramdict)) == str(res)
    assert str(paramdict @ vardict) == str(res)
    assert str(vardict @ paramdict) == str(res)


# ---- dot product type error tests ----

DOT_1D_TYPERR_CASES = [
    ParamDictND({(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2}),
    {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2},
    {'A': 1, 'B': 2, 'X': 9},
    1,
    1.0,
    'ABC',
]

DOT_ND_TYPERR_CASES = [
    ParamDict1D({0: 0, 1: 10, 2: 20}),
    {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2},
    {'A': 1, 'B': 2, 'X': 9},
    1,
    1.0,
    'ABC',
    (0, 10, 20),
    [0, 10, 20],
]

DOT_ND_VALERR_CASES = [
    ParamDictND({('A', 0): 0, ('A', 1): 1, ('B', 0): 1, ('B', 1): 2}),
    ParamDictND({('A', 0, 0, 0): 0, ('B', 1, 0, 0): 1, ('A', 0, 0, 1): 1, ('B', 1, 0, 1): 2}),
]


@pytest.mark.parametrize('other', DOT_1D_TYPERR_CASES)
def test_vardict1D_typ_err(model, add_vars_fn, add_vars_kwargs, other):
    vardict = add_vars_fn(model, IndexSet1D(['A', 'B', 'C']), **add_vars_kwargs)
    with pytest.raises(TypeError):
        vardict.dot(other)
    with pytest.raises(TypeError):
        other @ vardict
    with pytest.raises(TypeError):
        vardict @ other


@pytest.mark.parametrize('other', DOT_ND_TYPERR_CASES)
def test_vardictND_typ_err(model, add_vars_fn, add_vars_kwargs_nd, other):
    vardict = add_vars_fn(model, IndexSetND(['A', 'B'], range(3)), **add_vars_kwargs_nd)
    with pytest.raises(TypeError):
        vardict.dot(other)
    with pytest.raises(TypeError):
        other @ vardict
    with pytest.raises(TypeError):
        vardict @ other


@pytest.mark.parametrize('other', DOT_ND_VALERR_CASES)
def test_vardictND_val_err(model, add_vars_fn, add_vars_kwargs_nd, other):
    vardict = add_vars_fn(model, IndexSetND(['A', 'B'], range(3), range(3)), **add_vars_kwargs_nd)
    with pytest.raises(ValueError):
        vardict.dot(other)
    with pytest.raises(ValueError):
        other @ vardict
    with pytest.raises(ValueError):
        vardict @ other
