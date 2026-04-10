# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Custom methods of VarDict1D & VarDictND."""

import pytest
from highspy import Highs, HighsVarType

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND
from opti_extensions.highspy import addVariables


@pytest.mark.parametrize(
    'indexset, key, present',
    [(IndexSet1D(['A', 'B', 'C']), 'A', True), (IndexSet1D(['A', 'B', 'C']), 'Z', False)],
)
def test_vardict1d_lookup_pass(mdl, indexset, key, present):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
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
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    value = v.lookup(*key)
    if present:
        assert value is v[key]
    else:
        assert value == 0


@pytest.mark.parametrize('key', [[13], (0, 0), ()])
def test_vardictNd_lookup_typerr(mdl, key):
    v = addVariables(
        mdl, IndexSetND(range(2), range(2)), type=HighsVarType.kContinuous, name_prefix='VAL'
    )
    with pytest.raises(TypeError):
        v.lookup(key)


@pytest.mark.parametrize('key', [(), (0, 0, 0), (1, 2, 3, 4)])
def test_vardictNd_lookup_valerr(mdl, key):
    v = addVariables(
        mdl, IndexSetND(range(2), range(2)), type=HighsVarType.kContinuous, name_prefix='VAL'
    )
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
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    # mdl.update() # Highs doesn't need update?
    assert str(v.sum()) == str(Highs.qsum(x for x in v.values()))


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
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')

    def _match(key, pattern):
        return all(k == p or p == '*' for k, p in zip(key, pattern, strict=False))

    assert str(v.sum(*pattern)) == str(
        Highs.qsum(var for idx, var in v.items() if _match(idx, pattern))
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
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    with pytest.raises(ValueError):
        v.sum(*pattern)


@pytest.mark.parametrize(
    'indexset',
    [
        IndexSet1D(['A', 'B', 'C']),
        IndexSet1D(range(3)),
        IndexSetND(range(2), range(2)),
        IndexSetND(['A', 'B', 'C'], range(2)),
    ],
)
def test_vardict_sum_squares_not_implemented(mdl, indexset):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    with pytest.raises(NotImplementedError, match='sum_squares is not implemented for highspy'):
        v.sum_squares()


@pytest.mark.parametrize(
    'indexset, pattern',
    [
        [IndexSetND(range(2), range(2)), (0, '*')],
        [IndexSetND(range(2), range(2)), ('*', 0)],
    ],
)
def test_vardictNd_sum_squares_not_implemented(mdl, indexset, pattern):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    with pytest.raises(NotImplementedError, match='sum_squares is not implemented for highspy'):
        v.sum_squares(*pattern)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
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
    ],
)
def test_vardict_dot_pass(mdl, indexset, paramdict):
    vardict = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    res = Highs.qsum(paramdict.get(k, 0) * v for k, v in vardict.items())

    assert str(vardict.dot(paramdict)) == str(res)
    assert str(paramdict @ vardict) == str(res)
    assert str(vardict @ paramdict) == str(res)


@pytest.mark.parametrize(
    'other',
    [
        ParamDictND({(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2}),
        {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2},
        {'A': 1, 'B': 2, 'X': 9},
        1,
        1.0,
        'ABC',
    ],
)
def test_vardict1D_typ_err(mdl, other):
    vardict = addVariables(
        mdl, IndexSet1D(['A', 'B', 'C']), type=HighsVarType.kContinuous, name_prefix='VAL'
    )
    with pytest.raises(TypeError):
        vardict.dot(other)
    with pytest.raises(TypeError):
        other @ vardict
    with pytest.raises(TypeError):
        vardict @ other


@pytest.mark.parametrize(
    'other',
    [
        ParamDict1D({0: 0, 1: 10, 2: 20}),
        {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2},
        {'A': 1, 'B': 2, 'X': 9},
        1,
        1.0,
        'ABC',
        (0, 10, 20),
        [0, 10, 20],
    ],
)
def test_vardictND_typ_err(mdl, other):
    vardict = addVariables(
        mdl, IndexSetND(['A', 'B'], range(3)), type=HighsVarType.kContinuous, name_prefix='VAL'
    )
    with pytest.raises(TypeError):
        vardict.dot(other)
    with pytest.raises(TypeError):
        other @ vardict
    with pytest.raises(TypeError):
        vardict @ other


@pytest.mark.parametrize(
    'other',
    [
        ParamDictND({('A', 0): 0, ('A', 1): 1, ('B', 0): 1, ('B', 1): 2}),
        ParamDictND({('A', 0, 0, 0): 0, ('B', 1, 0, 0): 1, ('A', 0, 0, 1): 1, ('B', 1, 0, 1): 2}),
    ],
)
def test_vardictND_val_err(mdl, other):
    vardict = addVariables(
        mdl,
        IndexSetND(['A', 'B'], range(3), range(3)),
        type=HighsVarType.kContinuous,
        name_prefix='VAL',
    )
    with pytest.raises(ValueError):
        vardict.dot(other)
    with pytest.raises(ValueError):
        other @ vardict
    with pytest.raises(ValueError):
        vardict @ other
