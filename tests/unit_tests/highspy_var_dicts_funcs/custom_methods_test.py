# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Custom methods of VarDict1D & VarDictND."""

import pytest
from highspy import Highs, HighsVarType

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.highspy import addVariables

# Import all shared tests
from tests.unit_tests._shared_custom_methods_tests import *  # noqa: F401, F403
from tests.unit_tests._shared_custom_methods_tests import SUM_PARTIAL_PASS_CASES

# ---- Solver-specific: sum tests (highspy uses Highs.qsum) ----

SUM_INDEXSETS = [
    IndexSet1D(['A', 'B', 'C']),
    IndexSet1D(range(3)),
    IndexSetND(range(2), range(2)),
    IndexSetND(['A', 'B', 'C'], range(2)),
]


@pytest.mark.parametrize('indexset', SUM_INDEXSETS)
def test_vardict_sum_pass(mdl, indexset):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    assert str(v.sum()) == str(Highs.qsum(x for x in v.values()))


@pytest.mark.parametrize('indexset, pattern', SUM_PARTIAL_PASS_CASES)
def test_vardictNd_sum_partial_pass(mdl, indexset, pattern):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')

    def _match(key, pattern):
        return all(p in (k, '*') for k, p in zip(key, pattern, strict=False))

    assert str(v.sum(*pattern)) == str(
        Highs.qsum(var for idx, var in v.items() if _match(idx, pattern))
    )


# ---- Solver-specific: sum_squares raises NotImplementedError ----


@pytest.mark.parametrize('indexset', SUM_INDEXSETS)
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
