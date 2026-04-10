# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Add variable functionality."""

import pytest
from highspy import HighsVarType

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND
from opti_extensions.highspy import addVariables


@pytest.mark.parametrize('indexset', [IndexSet1D(), IndexSetND()])
def test_addVars_indexset_valerr(mdl, indexset):
    with pytest.raises(ValueError):
        addVariables(mdl, indexset, type=HighsVarType.kContinuous)


indexset_cases = [
    IndexSet1D(['A', 'B', 'C']),
    IndexSet1D(range(3)),
    IndexSetND(['A', 'B', 'C'], range(3)),
    IndexSetND(range(3), range(3)),
]


@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize('vtype', [HighsVarType.kContinuous, HighsVarType.kInteger])
def test_addVars_pass(mdl, mdl_2, indexset, vtype):
    one = addVariables(mdl, indexset, type=vtype, name_prefix='test')
    two = mdl_2.addVariables(indexset, type=vtype, name_prefix='test', out_array=False)

    # Compare structure: both should have same keys and all values should be highs_var
    assert set(one.keys()) == set(two.keys())
    assert all(str(type(v)) == "<class 'highspy.highs.highs_var'>" for v in one.values())
    assert all(str(type(v)) == "<class 'highspy.highs.highs_var'>" for v in two.values())


@pytest.mark.parametrize('mdl', ['abc', 123, ('A', 'B')])
@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize('type', [HighsVarType.kContinuous, HighsVarType.kInteger])
def test_addVars_mdl_typerr(mdl, indexset, type):
    with pytest.raises(TypeError):
        addVariables(mdl, indexset, type=type)


@pytest.mark.parametrize(
    'indexset',
    [
        (1, 2, 3),
        [1, 2, 3],
        [('A', 'B'), ('C', 'D')],
        [('A', '1'), ('C', '2')],
    ],
)
@pytest.mark.parametrize('type', [HighsVarType.kContinuous, HighsVarType.kInteger])
def test_addVars_idxset_typerr(mdl, indexset, type):
    with pytest.raises(TypeError):
        addVariables(mdl, indexset, type=type)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'A': 1, 'B': 1, 'C': 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_addVars_paramdict_bound(mdl, mdl_2, indexset, paramdict, bound_type):
    bound_kwargs_1 = {bound_type: paramdict}
    one = addVariables(
        mdl, indexset, type=HighsVarType.kContinuous, name_prefix='A', **bound_kwargs_1
    )

    bound_kwargs_2 = {bound_type: paramdict}
    two = mdl_2.addVariables(
        indexset, type=HighsVarType.kContinuous, name_prefix='A', out_array=False, **bound_kwargs_2
    )

    # Compare structure: both should have same keys and all values should be highs_var
    assert set(one.keys()) == set(two.keys())
    assert all(str(type(v)) == "<class 'highspy.highs.highs_var'>" for v in one.values())
    assert all(str(type(v)) == "<class 'highspy.highs.highs_var'>" for v in two.values())


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDictND({('A', 0): 1, ('B', 0): 1, ('C', 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDict1D({0: 1, 1: 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_addVars_paramdict_typerr(mdl, indexset, paramdict, bound_type):
    with pytest.raises(TypeError):
        bound_kwargs_1 = {bound_type: paramdict}
        addVariables(mdl, indexset, type=HighsVarType.kContinuous, **bound_kwargs_1)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0): 1, (0, 1, 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0, 0): 1, (0, 1, 0, 0): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_addVars_paramdict_difflen_valerr(mdl, indexset, paramdict, bound_type):
    with pytest.raises(ValueError):
        bound_kwargs_1 = {bound_type: paramdict}
        addVariables(mdl, indexset, type=HighsVarType.kContinuous, **bound_kwargs_1)
