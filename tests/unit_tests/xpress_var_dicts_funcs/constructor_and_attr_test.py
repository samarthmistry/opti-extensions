# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict1D & VarDictND constructor and attributes."""

from collections import abc

import pytest
import xpress as xp

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.xpress import VarDict1D, VarDictND, addVariables


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_typerr0(prob, cls, indexset):
    xp_vars = prob.addVariables(indexset)
    with pytest.raises(TypeError):
        cls(xp_vars, indexset, problem=prob, vartype=xp.continuous)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
@pytest.mark.parametrize('vardict', [0, int, [1, 2], 'A'])
def test_vardict_init_typerr1(prob, cls, indexset, vardict):
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, problem=prob, vartype=xp.continuous)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_valerr1(prob, cls, indexset):
    with pytest.raises(ValueError):
        cls._create({}, indexset, problem=prob, vartype=xp.continuous)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
@pytest.mark.parametrize('vardict', [{'A': 0, 'B': 1}, {1: [1, 2], 2: [2, 3]}])
def test_vardict_init_typerr2(prob, cls, indexset, vardict):
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, problem=prob, vartype=xp.continuous)


@pytest.mark.parametrize(
    'cls, indexset, incorrect',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C']), IndexSet1D(['A', 'B'])],
        [VarDictND, IndexSetND(range(2), range(2)), IndexSetND(range(1), range(2))],
    ],
)
def test_vardict_init_valerr2(prob, cls, indexset, incorrect):
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    with pytest.raises(ValueError):
        cls._create(v, incorrect, problem=prob, vartype=xp.continuous)


@pytest.mark.parametrize('name', [None, 'KEY'])
def test_vardict1d_init_keyname_pass(prob, name):
    indexset = IndexSet1D(['A', 'B', 'C'], name=name)
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    assert v.key_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_vardict1d_init_keyname_update_pass(prob, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    v.key_name = input
    assert v.key_name == input


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict1d_init_keyname_update_typeerr(prob, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    with pytest.raises(TypeError):
        v.key_name = input


@pytest.mark.parametrize(
    'input, expected',
    [
        [None, None],
        [('KEY1', 'KEY2'), ['KEY1', 'KEY2']],
        [['KEY1', 'KEY2'], ['KEY1', 'KEY2']],
        [('KEY1', 'KEY2', 'KEY3'), ['KEY1', 'KEY2', 'KEY3']],
        # ^ valid because ParamDictND doesn't enforce the names to conform with len of keys
    ],
)
def test_vardictNd_init_keynames_pass(prob, input, expected):
    indexset = IndexSetND(range(2), range(2), names=input)
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    assert v.key_names == expected


@pytest.mark.parametrize('input', [('C', 'D'), ['A', 'B', 'C']])
def test_vardictNd_init_keynames_update_pass(prob, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    v.key_names = input
    assert v.key_names == list(input)


@pytest.mark.parametrize('input', ['CD', 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_vardictNd_init_keynames_update_typeerr(prob, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    with pytest.raises(TypeError):
        v.key_names = input


@pytest.mark.parametrize('name', [None, 'VAL'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_pass(prob, indexset, name):
    v = addVariables(prob, indexset, vartype=xp.continuous, name=name)
    assert v.value_name == name


@pytest.mark.parametrize('input, name', [('DEF', 'V1'), ('Z', 'V2')])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_update_pass(prob, indexset, input, name):
    v = addVariables(prob, indexset, vartype=xp.continuous, name=name)
    v.value_name = input
    assert v.value_name == input


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict_init_valname_update_typeerr(prob, indexset, input):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')
    with pytest.raises(TypeError):
        v.value_name = input


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_problem_pass(prob, indexset):
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    assert v.problem is prob


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_problem_attrerr(prob, indexset):
    v = addVariables(prob, indexset, name='', vartype=xp.continuous)
    with pytest.raises(AttributeError):
        v.problem = 1


@pytest.mark.parametrize(
    'vartype', [xp.continuous, xp.binary, xp.integer, xp.semicontinuous, xp.semiinteger]
)
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_pass(prob, indexset, vartype):
    v = addVariables(prob, indexset, name='', vartype=vartype)
    assert v.vartype is vartype


@pytest.mark.parametrize(
    'vartype', [xp.continuous, xp.binary, xp.integer, xp.semicontinuous, xp.semiinteger]
)
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_attrerr(prob, indexset, vartype):
    v = addVariables(prob, indexset, name='', vartype=vartype)
    with pytest.raises(AttributeError):
        v.vartype = 1


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_isinstance_dict(prob, indexset):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')

    assert isinstance(v, dict)
    assert isinstance(v, abc.MutableMapping)
