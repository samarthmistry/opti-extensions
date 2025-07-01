# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Add variable functionality."""

import pytest
import xpress as xp

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND
from opti_extensions.xpress import addVariables


@pytest.mark.parametrize('indexset', [IndexSet1D(), IndexSetND()])
def test_addVariables_indexset_valerr(prob, indexset):
    with pytest.raises(ValueError):
        addVariables(prob, indexset, vartype=xp.continuous)


indexset_cases = [
    IndexSet1D(['A', 'B', 'C']),
    IndexSet1D(range(3)),
    IndexSetND(['A', 'B', 'C'], range(3)),
    IndexSetND(range(3), range(3)),
]


@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize(
    'vartype', [xp.continuous, xp.binary, xp.integer, xp.semicontinuous, xp.semiinteger]
)
def test_addVariables_pass(prob, prob_2, indexset, vartype, request):
    name = request.node.nodeid.split('/')[-1]

    one = addVariables(prob, indexset, vartype=vartype, name=name)
    repr_one = repr(dict(one))
    prob.reset()

    two = prob_2.addVariables(indexset, vartype=vartype, name=name)

    assert repr_one == repr(two)


@pytest.mark.parametrize('mdl', ['abc', 123, ('A', 'B')])
@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize(
    'vartype', [xp.continuous, xp.binary, xp.integer, xp.semicontinuous, xp.semiinteger]
)
def test_addVariables_mdl_typerr(mdl, indexset, vartype):
    with pytest.raises(TypeError):
        addVariables(mdl, indexset, vartype=vartype)


@pytest.mark.parametrize(
    'indexset',
    [
        (1, 2, 3),
        [1, 2, 3],
        [('A', 'B'), ('C', 'D')],
        [('A', '1'), ('C', '2')],
    ],
)
@pytest.mark.parametrize(
    'vartype', [xp.continuous, xp.binary, xp.integer, xp.semicontinuous, xp.semiinteger]
)
def test_addVariables_idxset_typerr(prob, indexset, vartype):
    with pytest.raises(TypeError):
        addVariables(prob, indexset, vartype=vartype)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'A': 1, 'B': 1, 'C': 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_addVariables_paramdict_bound(prob, indexset, paramdict, bound_type, request):
    name = request.node.nodeid.split('/')[-1]

    bound_kwargs_1 = {bound_type: paramdict}
    one = addVariables(prob, indexset, vartype=xp.continuous, name=name, **bound_kwargs_1)
    repr_one = repr(dict(one))
    prob.reset()

    if bound_type == 'lb':
        two = {
            elem: prob.addVariable(
                name=f'{name}({elem})', lb=paramdict.get(elem, 0), vartype=xp.continuous
            )
            for elem in indexset
        }
    else:
        two = {
            elem: prob.addVariable(
                name=f'{name}({elem})', ub=paramdict.get(elem, xp.infinity), vartype=xp.continuous
            )
            for elem in indexset
        }

    assert repr_one == repr(two)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDictND({('A', 0): 1, ('B', 0): 1, ('C', 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDict1D({0: 1, 1: 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_addVariables_paramdict_typerr(prob, indexset, paramdict, bound_type):
    with pytest.raises(TypeError):
        bound_kwargs_1 = {bound_type: paramdict}
        addVariables(prob, indexset, name='', vartype=xp.continuous, **bound_kwargs_1)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0): 1, (0, 1, 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0, 0): 1, (0, 1, 0, 0): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_addVariables_paramdict_difflen_valerr(prob, indexset, paramdict, bound_type):
    with pytest.raises(ValueError):
        bound_kwargs_1 = {bound_type: paramdict}
        addVariables(prob, indexset, name='', vartype=xp.continuous, **bound_kwargs_1)
