# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Other methods of ParamDict1D & ParamDictND."""

import pytest

from opti_extensions import ParamDict1D, ParamDictND


@pytest.mark.parametrize(
    '_input, _expected',
    [
        ('paramdict1d_emp', 'paramdict1d_emp'),
        ('paramdict1d_pop3', 'paramdict1d_emp'),
        ('paramdictNd_emp', 'paramdictNd_emp'),
        ('paramdictNd_pop3', 'paramdictNd_emp'),
    ],
)
def test_paramdict_clear_output_pass(request, _input, _expected):
    input = request.getfixturevalue(_input)
    expected = request.getfixturevalue(_expected)
    input.clear()
    assert input == expected


@pytest.mark.parametrize(
    '_input',
    ['paramdict1d_emp', 'paramdict1d_pop3', 'paramdictNd_emp', 'paramdictNd_pop3'],
)
def test_paramdict_copy_attrerr(request, _input):
    input = request.getfixturevalue(_input)
    with pytest.raises(AttributeError):
        input.copy()


@pytest.mark.parametrize(
    '_input, key, default, expected',
    [
        ('paramdict1d_emp', 'A', None, None),
        ('paramdict1d_emp', 'A', 9, 9),
        ('paramdict1d_pop3', 'A', None, 0),
        ('paramdict1d_pop3', 'A', 9, 0),
        ('paramdict1d_pop3', 'Z', None, None),
        ('paramdict1d_pop3', 'Z', 9, 9),
        ('paramdictNd_emp', ('A', 'B'), None, None),
        ('paramdictNd_emp', ('A', 'B'), 9, 9),
        ('paramdictNd_pop3', ('A', 'B'), None, 0),
        ('paramdictNd_pop3', ('A', 'B'), 9, 0),
        ('paramdictNd_pop3', ('Y', 'Z'), None, None),
        ('paramdictNd_pop3', ('Y', 'Z'), 9, 9),
    ],
)
def test_paramdict_get_pass(request, _input, key, default, expected):
    input = request.getfixturevalue(_input)
    value = input.get(key, default)
    assert value == expected


@pytest.mark.parametrize(
    '_input, key, default, popped, expected',
    [
        ('paramdict1d_pop2', 'A', None, 0, ParamDict1D({'B': 1})),
        ('paramdict1d_pop2', 'A', 9, 0, ParamDict1D({'B': 1})),
        ('paramdict1d_pop2', 'Z', None, None, ParamDict1D({'A': 0, 'B': 1})),
        ('paramdict1d_pop2', 'Z', 9, 9, ParamDict1D({'A': 0, 'B': 1})),
        ('paramdict1d_pop2', 'Z', 9.0, 9.0, ParamDict1D({'A': 0, 'B': 1})),
        ('paramdict1d_pop2', 'Z', '9', '9', ParamDict1D({'A': 0, 'B': 1})),
        ('paramdict1d_pop2', 'Z', (8, 9), (8, 9), ParamDict1D({'A': 0, 'B': 1})),
        ('paramdictNd_pop2', ('A', 'B'), None, 0, ParamDictND({('C', 'D'): 1})),
        ('paramdictNd_pop2', ('A', 'B'), 9, 0, ParamDictND({('C', 'D'): 1})),
        ('paramdictNd_pop2', ('Y', 'Z'), None, None, ParamDictND({('A', 'B'): 0, ('C', 'D'): 1})),
        ('paramdictNd_pop2', ('Y', 'Z'), 9, 9, ParamDictND({('A', 'B'): 0, ('C', 'D'): 1})),
        ('paramdictNd_pop2', ('Y', 'Z'), 9.0, 9.0, ParamDictND({('A', 'B'): 0, ('C', 'D'): 1})),
        ('paramdictNd_pop2', ('Y', 'Z'), '9', '9', ParamDictND({('A', 'B'): 0, ('C', 'D'): 1})),
        (
            'paramdictNd_pop2',
            ('Y', 'Z'),
            (8, 9),
            (8, 9),
            ParamDictND({('A', 'B'): 0, ('C', 'D'): 1}),
        ),
    ],
)
def test_paramdict_pop_wdefault_pass(request, _input, key, default, popped, expected):
    input = request.getfixturevalue(_input)
    value = input.pop(key, default)
    assert value == popped
    assert input == expected


@pytest.mark.parametrize(
    '_input, key, popped, expected',
    [
        ('paramdict1d_pop2', 'A', 0, ParamDict1D({'B': 1})),
        ('paramdict1d_pop2', 'A', 0, ParamDict1D({'B': 1})),
        ('paramdictNd_pop2', ('A', 'B'), 0, ParamDictND({('C', 'D'): 1})),
        ('paramdictNd_pop2', ('A', 'B'), 0, ParamDictND({('C', 'D'): 1})),
    ],
)
def test_paramdict_pop_wodefault_pass(request, _input, key, popped, expected):
    input = request.getfixturevalue(_input)
    value = input.pop(key)
    assert value == popped
    assert input == expected


@pytest.mark.parametrize(
    '_input, key',
    [('paramdict1d_pop2', 'Z'), ('paramdictNd_pop2', ('Y', 'Z'))],
)
def test_paramdict_pop_wodefault_keyerr(request, _input, key):
    input = request.getfixturevalue(_input)
    with pytest.raises(KeyError):
        input.pop(key)


@pytest.mark.parametrize(
    '_input, popped1, expected1, popped2, expected2',
    [
        ('paramdict1d_pop2', ('B', 1), ParamDict1D({'A': 0}), ('A', 0), ParamDict1D()),
        (
            'paramdictNd_pop2',
            (('C', 'D'), 1),
            ParamDictND({('A', 'B'): 0}),
            (('A', 'B'), 0),
            ParamDictND(),
        ),
    ],
)
def test_paramdict_popitem_pass(request, _input, popped1, expected1, popped2, expected2):
    input = request.getfixturevalue(_input)

    value1 = input.popitem()
    assert value1 == popped1
    assert input == expected1

    value2 = input.popitem()
    assert value2 == popped2
    assert input == expected2


@pytest.mark.parametrize('_input', ['paramdict1d_emp', 'paramdictNd_emp'])
def test_paramdict_popitem_emp_keyerr(request, _input):
    input = request.getfixturevalue(_input)
    with pytest.raises(KeyError):
        input.popitem()


@pytest.mark.parametrize(
    'input, key, default, expected',
    [
        (ParamDict1D({'A': 0}), 'B', 1, ParamDict1D({'A': 0, 'B': 1})),
        (ParamDict1D({'A': 0}), 'B', 1.0, ParamDict1D({'A': 0, 'B': 1})),
        (ParamDictND({('A', 'B'): 0}), ('C', 'D'), 1, ParamDictND({('A', 'B'): 0, ('C', 'D'): 1})),
        (
            ParamDictND({('A', 'B'): 0}),
            ('C', 'D'),
            1.0,
            ParamDictND({('A', 'B'): 0, ('C', 'D'): 1.0}),
        ),
    ],
)
def test_paramdict_setdefault_pass(request, input, key, default, expected):
    input.setdefault(key, default)
    assert input == expected


@pytest.mark.parametrize('_input', [('paramdict1d_pop3'), ('paramdictNd_pop3')])
@pytest.mark.parametrize('default', ['1', int, [1, 2, 3], (1, 'A'), {1, 2}])
def test_paramdict_setdefault_value_typerr(request, _input, default):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError):
        input.setdefault('Z', default)


@pytest.mark.parametrize(
    '_input, key',
    [
        ('paramdict1d_pop3', ('Y', 'Z')),
        ('paramdict1d_pop3', ['Y', 'Z']),
        ('paramdict1d_pop3', {'Y', 'Z'}),
        ('paramdictNd_pop3', 'A'),
        ('paramdictNd_pop3', 1),
        ('paramdictNd_pop3', int),
        ('paramdictNd_pop3', ['Y', 'Z']),
        ('paramdictNd_pop3', {'Y', 'Z'}),
    ],
)
def test_paramdict_setdefault_key_typerr(request, _input, key):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError):
        input.setdefault(key, 1)


@pytest.mark.parametrize(
    '_input, key',
    [('paramdictNd_pop3', ('X', 'Y', 'Z')), ('paramdictNd_pop3', ('X',))],
)
def test_paramdictNd_setdefault_keydifflen_valerr(request, _input, key):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError):
        input.setdefault(key, 1)


@pytest.mark.parametrize(
    '_input',
    ['paramdict1d_emp', 'paramdict1d_pop3', 'paramdictNd_emp', 'paramdictNd_pop3'],
)
@pytest.mark.parametrize('other', [{}, {'Y': 8, 'Z': 9}, [('Y', 8), ('Z', 9)]])
def test_paramdict_update_attrerr(request, _input, other):
    input = request.getfixturevalue(_input)
    with pytest.raises(AttributeError):
        input.update(other)


@pytest.mark.parametrize(
    'cls, iterable',
    [(ParamDict1D, ('A', 'B')), (ParamDictND, (('A', 'B'), ('C', 'D')))],
)
def test_paramdict_fromkeys_attrerr(cls, iterable):
    with pytest.raises(AttributeError):
        cls.fromkeys(iterable)
