# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""ParamDict1D & ParamDictND constructor and attributes."""

from collections import abc

import pytest

from opti_extensions import ParamDict1D, ParamDictND


@pytest.mark.parametrize(
    'cls, input',
    [
        (ParamDict1D, {}),
        (ParamDict1D, {'A': 0, 'B': 1, 'C': 2}),
        (ParamDict1D, {1: 0, 2: 1.0, 3: 2.1}),
        (ParamDictND, {}),
        (ParamDictND, {('A', 'B'): 0, ('C', 'D'): 1, ('E', 'F'): 2}),
        (ParamDictND, {(0, 'B'): 0, (1, 'D'): 1.0, (2, 'F'): 1.5}),
    ],
)
def test_paramdict_init_pass(cls, input):
    # ParamDict is supposed to be a subclass of dict, so test for equality at init
    if input:
        assert cls(input) == input
    else:
        assert cls() == input


@pytest.mark.parametrize('cls', [ParamDict1D, ParamDictND])
@pytest.mark.parametrize(
    'input',
    [1, float, 'A', (1, 2, 3), ['A', 1, 2]],
)
def test_paramdict_init_nondict(cls, input):
    with pytest.raises(TypeError):
        cls(input)


@pytest.mark.parametrize('cls', [ParamDict1D, ParamDictND])
def test_paramdict_init_mix_scalartuple(cls):
    with pytest.raises(TypeError):
        cls({('A', 'B'): 0, ('C', 'D'): 1, 'E': 2})


@pytest.mark.parametrize(
    'input',
    [
        {(0, 'A'): 1, (1, 'B'): 2, (2, 'C', 'D'): 3},
        {(0, 'A', 3.0): 1, (1, 'B'): 2, (2,): 3},
    ],
)
def test_paramdictNd_init_elem_difflen(input):
    with pytest.raises(ValueError):
        ParamDictND(input)


@pytest.mark.parametrize(
    'cls, input',
    [
        (ParamDict1D, {'A': 1, 'B': 'X'}),
        (ParamDict1D, {'A': 1, 'B': (1, 2, 3)}),
        (ParamDict1D, {'A': 1, 'B': {1, 2, 3}}),
        (ParamDict1D, {'A': 1, 'B': [1, 2, 3]}),
        (ParamDictND, {(0, 'A'): 1, (1, 'B'): 'X'}),
        (ParamDictND, {(0, 'A'): 1, (1, 'B'): (1, 2, 3)}),
        (ParamDictND, {(0, 'A'): 1, (1, 'B'): {1, 2, 3}}),
        (ParamDictND, {(0, 'A'): 1, (1, 'B'): [1, 2, 3]}),
    ],
)
def test_paramdict_init_other_value(cls, input):
    with pytest.raises(TypeError):
        cls(input)


@pytest.mark.parametrize('name', [None, 'KEY'])
def test_paramdict1d_init_keyname_pass(name):
    p = ParamDict1D({'A': 0, 'B': 1}, key_name=name)
    assert p.key_name == name


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_paramdict1d_init_keyname_typeerr(input):
    with pytest.raises(TypeError):
        ParamDict1D({'A': 0, 'B': 1}, key_name=input)


@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_paramdict1d_init_keyname_update_pass(input):
    p = ParamDict1D({'A': 0, 'B': 1}, key_name='KEY')
    p.key_name = input
    assert p.key_name == input


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_paramdict1d_init_keyname_update_typeerr(input):
    p = ParamDict1D({'A': 0, 'B': 1}, key_name='KEY')
    with pytest.raises(TypeError):
        p.key_name = input


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
def test_paramdictNd_init_keynames_pass(input, expected):
    p = ParamDictND({('A', 'B'): 0, ('C', 'D'): 1}, key_names=input)
    assert p.key_names == expected


@pytest.mark.parametrize('input', [123, 'ABC', [1, 2, 3], [1, 'A', 'B'], {'A', 'B', 'C'}])
def test_paramdictNd_init_keynames_typeerr(input):
    with pytest.raises(TypeError):
        ParamDictND({('A', 'B'): 0, ('C', 'D'): 1}, key_names=input)


@pytest.mark.parametrize('input', [('C', 'D'), ['A', 'B', 'C']])
def test_paramdictNd_init_keynames_update_pass(input):
    p = ParamDictND({('A', 'B'): 0, ('C', 'D'): 1}, key_names=('KEY1', 'KEY2'))
    p.key_names = input
    assert p.key_names == list(input)


@pytest.mark.parametrize('input', ['CD', 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_paramdictNd_init_keynames_update_typeerr(input):
    p = ParamDictND({('A', 'B'): 0, ('C', 'D'): 1}, key_names=('KEY1', 'KEY2'))
    with pytest.raises(TypeError):
        p.key_names = input


@pytest.mark.parametrize(
    'cls, data',
    [
        (ParamDict1D, {'A': 0, 'B': 1, 'C': 2}),
        (ParamDictND, {('A', 'B'): 0, ('C', 'D'): 1, ('E', 'F'): 2}),
    ],
)
def test_paramdict_init_valname_pass(cls, data):
    name = 'VALUE'
    p = cls(data, value_name=name)
    assert p.value_name == name


@pytest.mark.parametrize(
    'cls, data',
    [
        (ParamDict1D, {'A': 0, 'B': 1, 'C': 2}),
        (ParamDictND, {('A', 'B'): 0, ('C', 'D'): 1, ('E', 'F'): 2}),
    ],
)
@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_paramdict_init_valname_typeerr(cls, data, input):
    with pytest.raises(TypeError):
        cls(data, value_name=input)


@pytest.mark.parametrize(
    'cls, data',
    [
        (ParamDict1D, {'A': 0, 'B': 1, 'C': 2}),
        (ParamDictND, {('A', 'B'): 0, ('C', 'D'): 1, ('E', 'F'): 2}),
    ],
)
@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_paramdict_init_valname_update_pass(cls, data, input):
    p = cls(data, value_name='VALUE')
    p.value_name = input
    assert p.value_name == input


@pytest.mark.parametrize(
    'cls, data',
    [
        (ParamDict1D, {'A': 0, 'B': 1, 'C': 2}),
        (ParamDictND, {('A', 'B'): 0, ('C', 'D'): 1, ('E', 'F'): 2}),
    ],
)
@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_paramdict_init_valname_update_typeerr(cls, data, input):
    p = cls(data, value_name='VALUE')
    with pytest.raises(TypeError):
        p.value_name = input


@pytest.mark.parametrize(
    '_input', ['paramdict1d_emp', 'paramdictNd_emp', 'paramdict1d_pop3', 'paramdictNd_pop3']
)
def test_paramdict_isinstance_dict(request, _input):
    input = request.getfixturevalue(_input)

    assert isinstance(input, dict)
    assert isinstance(input, abc.MutableMapping)
