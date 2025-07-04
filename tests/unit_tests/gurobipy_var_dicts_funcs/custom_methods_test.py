# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Custom methods of VarDict1D & VarDictND."""

import pytest
from gurobipy import GRB, quicksum

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.gurobipy import addVars


@pytest.mark.parametrize(
    'indexset, key, present',
    [(IndexSet1D(['A', 'B', 'C']), 'A', True), (IndexSet1D(['A', 'B', 'C']), 'Z', False)],
)
def test_vardict1d_lookup_pass(mdl, indexset, key, present):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    value = v.lookup(key)
    if present:
        assert value is v[key]
    else:
        assert value == 0


@pytest.mark.parametrize(
    'indexset, key, present',
    [
        (IndexSetND(range(2), range(2)), (0, 0), True),
        (IndexSetND(range(2), range(2)), (0, 9), False),
        (IndexSetND(['A', 'B', 'C'], range(2)), ('A', 0), True),
        (IndexSetND(['A', 'B', 'C'], range(2)), ('Z', 0), False),
    ],
)
def test_vardictNd_lookup_pass(mdl, indexset, key, present):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    value = v.lookup(*key)
    if present:
        assert value is v[key]
    else:
        assert value == 0


@pytest.mark.parametrize('key', [[13], (0, 0), ()])
def test_vardictNd_lookup_typerr(mdl, key):
    v = addVars(mdl, IndexSetND(range(2), range(2)), vtype=GRB.CONTINUOUS, name='VAL')
    with pytest.raises(TypeError):
        v.lookup(key)


@pytest.mark.parametrize('key', [(), (0, 0, 0), (1, 2, 3, 4)])
def test_vardictNd_lookup_valerr(mdl, key):
    v = addVars(mdl, IndexSetND(range(2), range(2)), vtype=GRB.CONTINUOUS, name='VAL')
    with pytest.raises(ValueError):
        v.lookup(*key)


@pytest.mark.parametrize(
    'indexset',
    [
        IndexSet1D(['A', 'B', 'C']),
        IndexSet1D(range(3)),
        IndexSetND(range(2), range(2)),
        IndexSetND(['A', 'B', 'C'], range(2)),
    ],
)
def test_vardict_sum_pass(mdl, indexset):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    mdl.update()
    assert str(v.sum()) == str(quicksum(x for x in v.values()))
    assert str(v.sum_squares()) == str(quicksum(x**2 for x in v.values()))


@pytest.mark.parametrize(
    'indexset, pattern',
    [
        [IndexSetND(range(2), range(2)), (0, '*')],
        [IndexSetND(range(2), range(2)), ('*', 0)],
        [IndexSetND(range(2), range(2)), (9, '*')],
        [IndexSetND(['A', 'B', 'C'], range(2)), ('A', '*')],
        [IndexSetND(['A', 'B', 'C'], range(2)), ('*', 0)],
        [IndexSetND(['A', 'B', 'C'], range(2)), ('*', 'Z')],
        [IndexSetND(['A', 'B', 'C'], [0]), ('B', '*')],
    ],
)
def test_vardictNd_sum_partial_pass(mdl, indexset, pattern):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    mdl.update()

    def _match(key, pattern):
        return all(k == p or p == '*' for k, p in zip(key, pattern, strict=False))

    assert str(v.sum(*pattern)) == str(
        quicksum(var for idx, var in v.items() if _match(idx, pattern))
    )
    assert str(v.sum_squares(*pattern)) == str(
        quicksum(var**2 for idx, var in v.items() if _match(idx, pattern))
    )


@pytest.mark.parametrize(
    'indexset, pattern',
    [
        [IndexSetND(range(2), range(2)), (0, 0)],
        [IndexSetND(range(2), range(2)), ('*', '*')],
        [IndexSetND(range(2), range(2)), (0, 0, 0)],
    ],
)
def test_vardictNd_sum_partial_valerr(mdl, indexset, pattern):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    with pytest.raises(ValueError):
        v.sum(*pattern)
    with pytest.raises(ValueError):
        v.sum_squares(*pattern)
