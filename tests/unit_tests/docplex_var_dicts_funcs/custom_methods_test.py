# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Custom methods of VarDict1D & VarDictND."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.docplex import add_variables

# Import all shared tests
from tests.unit_tests._shared_custom_methods_tests import *  # noqa: F401, F403
from tests.unit_tests._shared_custom_methods_tests import SUM_PARTIAL_PASS_CASES

# ---- Solver-specific: sum tests (docplex uses .to_string() comparison) ----

SUM_INDEXSETS = [
    IndexSet1D(['A', 'B', 'C']),
    IndexSet1D(range(3)),
    IndexSetND(range(2), range(2)),
    IndexSetND(['A', 'B', 'C'], range(2)),
]


@pytest.mark.parametrize('indexset', SUM_INDEXSETS)
def test_vardict_sum_pass(mdl, indexset):
    v = add_variables(mdl, indexset, 'C', name='VAL')
    assert v.sum().to_string() == mdl.sum(v.values()).to_string()
    assert v.sum_squares().to_string() == mdl.sumsq(v.values()).to_string()


@pytest.mark.parametrize('indexset, pattern', SUM_PARTIAL_PASS_CASES)
def test_vardictNd_sum_partial_pass(mdl, indexset, pattern):
    v = add_variables(mdl, indexset, 'C', name='VAL')

    def _match(key, pattern):
        return all(p in (k, '*') for k, p in zip(key, pattern, strict=False))

    assert (
        v.sum(*pattern).to_string()
        == mdl.sum(var for idx, var in v.items() if _match(idx, pattern)).to_string()
    )
    assert (
        v.sum_squares(*pattern).to_string()
        == mdl.sumsq(var for idx, var in v.items() if _match(idx, pattern)).to_string()
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
def test_vardictNd_sum_squares_partial_valerr(mdl, indexset, pattern):
    v = add_variables(mdl, indexset, 'C', name='VAL')
    with pytest.raises(ValueError):
        v.sum_squares(*pattern)
