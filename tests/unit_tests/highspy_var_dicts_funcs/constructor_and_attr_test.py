# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict1D & VarDictND constructor and attributes."""

from collections import abc

import pytest
from highspy import HighsVarType

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.highspy import VarDict1D, VarDictND, addVariables


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_typerr0(mdl, cls, indexset):
    highs_vars = addVariables(mdl, indexset)
    with pytest.raises(TypeError):
        cls(highs_vars, indexset, model=mdl, type=HighsVarType.kContinuous)


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
        cls._create(vardict, indexset, model=mdl, type=HighsVarType.kContinuous)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_valerr1(mdl, cls, indexset):
    with pytest.raises(ValueError):
        cls._create({}, indexset, model=mdl, type=HighsVarType.kContinuous)


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
        cls._create(vardict, indexset, model=mdl, type=HighsVarType.kContinuous)


@pytest.mark.parametrize(
    'cls, indexset, incorrect',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C']), IndexSet1D(['A', 'B'])],
        [VarDictND, IndexSetND(range(2), range(2)), IndexSetND(range(1), range(2))],
    ],
)
def test_vardict_init_valerr2(mdl, cls, indexset, incorrect):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    with pytest.raises(ValueError):
        cls._create(v, incorrect, model=mdl, type=HighsVarType.kContinuous)


@pytest.mark.parametrize('name', [None, 'KEY'])
def test_vardict1d_init_keyname_pass(mdl, name):
    indexset = IndexSet1D(['A', 'B', 'C'], name=name)
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    assert v.key_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_vardict1d_init_keyname_update_pass(mdl, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    v.key_name = input
    assert v.key_name == input


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict1d_init_keyname_update_typeerr(mdl, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
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
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    assert v.key_names == expected


@pytest.mark.parametrize('input', [('C', 'D'), ['A', 'B', 'C']])
def test_vardictNd_init_keynames_update_pass(mdl, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    v.key_names = input
    assert v.key_names == list(input)


@pytest.mark.parametrize('input', ['CD', 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_vardictNd_init_keynames_update_typeerr(mdl, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    with pytest.raises(TypeError):
        v.key_names = input


@pytest.mark.parametrize('name', [None, 'VAL'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_pass(mdl, indexset, name):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix=name)
    assert v.value_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_update_pass(mdl, indexset, input):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    v.value_name = input
    assert v.value_name == input


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict_init_valname_update_typeerr(mdl, indexset, input):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')
    with pytest.raises(TypeError):
        v.value_name = input


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_model_pass(mdl, indexset):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    assert v.Highs is mdl


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_model_attrerr(mdl, indexset):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous)
    with pytest.raises(AttributeError):
        v.Highs = 1


@pytest.mark.parametrize('type', [HighsVarType.kContinuous, HighsVarType.kInteger])
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_pass(mdl, indexset, type):
    v = addVariables(mdl, indexset, type=type)
    assert v.type is type


@pytest.mark.parametrize('type', [HighsVarType.kContinuous, HighsVarType.kInteger])
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_attrerr(mdl, indexset, type):
    v = addVariables(mdl, indexset, type=type)
    with pytest.raises(AttributeError):
        v.type = 1


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_isinstance_dict(mdl, indexset):
    v = addVariables(mdl, indexset, type=HighsVarType.kContinuous, name_prefix='VAL')

    assert isinstance(v, dict)
    assert isinstance(v, abc.MutableMapping)
