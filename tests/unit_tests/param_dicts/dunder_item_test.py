# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Dunder getitem, setitem, delitem of ParamDict1D & ParamDictND."""

import pytest

from opti_extensions import ParamDict1D, ParamDictND


@pytest.mark.parametrize(
    '_input',
    ['paramdict1d_emp', 'paramdict1d_pop3', 'paramdictNd_emp', 'paramdictNd_pop3'],
)
@pytest.mark.parametrize('index', ['Z', 1, ('Y', 'Z')])
def test_paramdict_getitem_keyerr(request, _input, index):
    input = request.getfixturevalue(_input)
    with pytest.raises(KeyError):
        input[index]


@pytest.mark.parametrize(
    '_input, index, value, expected',
    [
        ('paramdict1d_pop2', 'Z', 9, ParamDict1D({'A': 0, 'B': 1, 'Z': 9})),
        ('paramdict1d_pop2', 'Z', 9.0, ParamDict1D({'A': 0, 'B': 1, 'Z': 9.0})),
        (
            'paramdictNd_pop2',
            ('Y', 'Z'),
            9,
            ParamDictND({('A', 'B'): 0, ('C', 'D'): 1, ('Y', 'Z'): 9}),
        ),
        (
            'paramdictNd_pop2',
            ('Y', 'Z'),
            9.0,
            ParamDictND({('A', 'B'): 0, ('C', 'D'): 1, ('Y', 'Z'): 9.0}),
        ),
        ('paramdict1d_pop2', 'B', 9, ParamDict1D({'A': 0, 'B': 9})),
        ('paramdict1d_pop2', 'B', 9.0, ParamDict1D({'A': 0, 'B': 9.0})),
        ('paramdictNd_pop2', ('C', 'D'), 9, ParamDictND({('A', 'B'): 0, ('C', 'D'): 9})),
        ('paramdictNd_pop2', ('C', 'D'), 9.0, ParamDictND({('A', 'B'): 0, ('C', 'D'): 9.0})),
    ],
)
def test_paramdict_setitem_pass(request, _input, index, value, expected):
    input = request.getfixturevalue(_input)
    input[index] = value
    assert input == expected


@pytest.mark.parametrize(
    '_input, index, value, err',
    [
        ('paramdict1d_pop2', ('Y', 'Z'), 9, TypeError),
        ('paramdict1d_pop2', {'X', 'Y', 'Z'}, 9, TypeError),
        ('paramdictNd_pop2', 'Z', 9, TypeError),
        ('paramdictNd_pop2', {'X', 'Y', 'Z'}, 9, TypeError),
        ('paramdictNd_pop2', int, 9, TypeError),
        ('paramdictNd_pop2', ('X', 'Y', 'Z'), 9, ValueError),
        ('paramdictNd_pop2', ('X',), 9, ValueError),
    ],
)
def test_paramdict_setitem_idxset_err(request, _input, index, value, err):
    input = request.getfixturevalue(_input)
    with pytest.raises(err):
        input[index] = value


@pytest.mark.parametrize(
    '_input, index',
    [('paramdict1d_pop2', 'Z'), ('paramdictNd_pop2', ('Y', 'Z'))],
)
@pytest.mark.parametrize('value', ['DEF', [1, 2, 3], (1, 2, 3), {1, 2, 3}])
def test_paramdict_setitem_val_typerr(request, _input, index, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError):
        input[index] = value


@pytest.mark.parametrize(
    '_input, key, _expected',
    [
        ('paramdict1d_pop3', 'C', 'paramdict1d_pop2'),
        ('paramdictNd_pop3', ('E', 'F'), 'paramdictNd_pop2'),
    ],
)
def test_paramdict_delitem_pass(request, _input, key, _expected):
    input = request.getfixturevalue(_input)
    expected = request.getfixturevalue(_expected)
    del input[key]
    assert input == expected


@pytest.mark.parametrize(
    '_input, key',
    [('paramdict1d_pop3', 'Z'), ('paramdictNd_pop3', ('Y', 'Z'))],
)
def test_paramdict_delitem_keyerr(request, _input, key):
    input = request.getfixturevalue(_input)
    with pytest.raises(KeyError):
        del input[key]
