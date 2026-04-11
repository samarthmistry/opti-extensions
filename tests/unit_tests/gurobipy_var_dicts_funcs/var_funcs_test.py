# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Add variable functionality."""

import pytest
from gurobipy import GRB

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND
from opti_extensions.gurobipy import addVars
from tests.unit_tests._shared_var_funcs_tests import *  # noqa: F401, F403
from tests.unit_tests._shared_var_funcs_tests import SHARED_INDEXSET_CASES


@pytest.mark.parametrize('indexset', SHARED_INDEXSET_CASES)
@pytest.mark.parametrize(
    'vtype', [GRB.CONTINUOUS, GRB.BINARY, GRB.INTEGER, GRB.SEMICONT, GRB.SEMIINT]
)
def test_addVars_pass(mdl, mdl_2, indexset, vtype):
    one = addVars(mdl, indexset, vtype=vtype, name='test')
    mdl.update()
    two = mdl_2.addVars(indexset, vtype=vtype, name='test')
    mdl_2.update()

    assert repr(dict(one)) == repr(two)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'A': 1, 'B': 1, 'C': 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_addVars_paramdict_bound(mdl, indexset, paramdict, bound_type):
    bound_kwargs_1 = {bound_type: paramdict}
    one = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='A', **bound_kwargs_1)

    bound_kwargs_2 = {bound_type: paramdict}
    two = mdl.addVars(indexset, vtype=GRB.CONTINUOUS, name='A', **bound_kwargs_2)

    mdl.update()
    assert repr(dict(one)) == repr(two)
