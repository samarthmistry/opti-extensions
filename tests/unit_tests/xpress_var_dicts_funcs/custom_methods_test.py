# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Custom methods of VarDict1D & VarDictND."""

import pytest
import xpress as xp

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.xpress import addVariables

# Import all shared tests
from tests.unit_tests._shared_custom_methods_tests import *  # noqa: F401, F403
from tests.unit_tests._shared_custom_methods_tests import SUM_PARTIAL_PASS_CASES

# ---- Solver-specific: sum tests (xpress uses xp.Sum) ----

SUM_INDEXSETS = [
    IndexSet1D(['A', 'B', 'C']),
    IndexSet1D(range(3)),
    IndexSetND(range(2), range(2)),
    IndexSetND(['A', 'B', 'C'], range(2)),
]


@pytest.mark.parametrize('indexset', SUM_INDEXSETS)
def test_vardict_sum_pass(prob, indexset):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')
    assert str(v.sum()) == str(xp.Sum(x for x in v.values()))
    assert str(v.sum_squares()) == str(xp.Sum(x**2 for x in v.values()))


@pytest.mark.parametrize('indexset, pattern', SUM_PARTIAL_PASS_CASES)
def test_vardictNd_sum_partial_pass(prob, indexset, pattern):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')

    def _match(key, pattern):
        return all(p in (k, '*') for k, p in zip(key, pattern, strict=False))

    assert str(v.sum(*pattern)) == str(
        xp.Sum(var for idx, var in v.items() if _match(idx, pattern))
    )
    assert str(v.sum_squares(*pattern)) == str(
        xp.Sum(var**2 for idx, var in v.items() if _match(idx, pattern))
    )


# ---- Solver-specific: sum_squares partial valerr ----


@pytest.mark.parametrize(
    'indexset, pattern',
    [
        [IndexSetND(range(2), range(2)), (0, 0)],
        [IndexSetND(range(2), range(2)), ('*', '*')],
        [IndexSetND(range(2), range(2)), (0, 0, 0)],
    ],
)
def test_vardictNd_sum_squares_partial_valerr(prob, indexset, pattern):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')
    with pytest.raises(ValueError):
        v.sum_squares(*pattern)
