# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict1D & VarDictND constructor and attributes."""

from collections import abc

import pytest
from gurobipy import GRB

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.gurobipy import VarDict1D, VarDictND, addVars


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_typerr0(mdl, cls, indexset):
    gp_vars = mdl.addVars(indexset)
    with pytest.raises(TypeError):
        cls(gp_vars, indexset, model=mdl, vtype=GRB.CONTINUOUS)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
@pytest.mark.parametrize('vardict', [0, int, [1, 2], 'A'])
def test_vardict_init_typerr1(mdl, cls, indexset, vardict):
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, model=mdl, vtype=GRB.CONTINUOUS)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_valerr1(mdl, cls, indexset):
    with pytest.raises(ValueError):
        cls._create({}, indexset, model=mdl, vtype=GRB.CONTINUOUS)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
@pytest.mark.parametrize('vardict', [{'A': 0, 'B': 1}, {1: [1, 2], 2: [2, 3]}])
def test_vardict_init_typerr2(mdl, cls, indexset, vardict):
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, model=mdl, vtype=GRB.CONTINUOUS)


@pytest.mark.parametrize(
    'cls, indexset, incorrect',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C']), IndexSet1D(['A', 'B'])],
        [VarDictND, IndexSetND(range(2), range(2)), IndexSetND(range(1), range(2))],
    ],
)
def test_vardict_init_valerr2(mdl, cls, indexset, incorrect):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    with pytest.raises(ValueError):
        cls._create(v, incorrect, model=mdl, vtype=GRB.CONTINUOUS)


@pytest.mark.parametrize('name', [None, 'KEY'])
def test_vardict1d_init_keyname_pass(mdl, name):
    indexset = IndexSet1D(['A', 'B', 'C'], name=name)
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    assert v.key_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_vardict1d_init_keyname_update_pass(mdl, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    v.key_name = input
    assert v.key_name == input


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict1d_init_keyname_update_typeerr(mdl, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
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
def test_vardictNd_init_keynames_pass(mdl, input, expected):
    indexset = IndexSetND(range(2), range(2), names=input)
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    assert v.key_names == expected


@pytest.mark.parametrize('input', [('C', 'D'), ['A', 'B', 'C']])
def test_vardictNd_init_keynames_update_pass(mdl, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    v.key_names = input
    assert v.key_names == list(input)


@pytest.mark.parametrize('input', ['CD', 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_vardictNd_init_keynames_update_typeerr(mdl, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    with pytest.raises(TypeError):
        v.key_names = input


@pytest.mark.parametrize('name', [None, 'VAL'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_pass(mdl, indexset, name):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name=name)
    assert v.value_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_update_pass(mdl, indexset, input):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    v.value_name = input
    assert v.value_name == input


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict_init_valname_update_typeerr(mdl, indexset, input):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    with pytest.raises(TypeError):
        v.value_name = input


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_model_pass(mdl, indexset):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    assert v.Model is mdl


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_model_attrerr(mdl, indexset):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS)
    with pytest.raises(AttributeError):
        v.Model = 1


@pytest.mark.parametrize(
    'vtype', [GRB.CONTINUOUS, GRB.BINARY, GRB.INTEGER, GRB.SEMICONT, GRB.SEMIINT]
)
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_pass(mdl, indexset, vtype):
    v = addVars(mdl, indexset, vtype=vtype)
    assert v.VType is vtype


@pytest.mark.parametrize(
    'vtype', [GRB.CONTINUOUS, GRB.BINARY, GRB.INTEGER, GRB.SEMICONT, GRB.SEMIINT]
)
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_attrerr(mdl, indexset, vtype):
    v = addVars(mdl, indexset, vtype=vtype)
    with pytest.raises(AttributeError):
        v.VType = 1


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_isinstance_dict(mdl, indexset):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')

    assert isinstance(v, dict)
    assert isinstance(v, abc.MutableMapping)
