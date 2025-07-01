# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Sequence methods of IndexSet1D & IndexSetND."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_not_mutated, assert_sets_same


@pytest.mark.parametrize(
    '_input, value',
    [
        ('set1d_012', 0),
        ('setNd_012', (0, 0)),
    ],
)
def test_set_contains(request, _input, value):
    input = request.getfixturevalue(_input)
    assert value in input


@pytest.mark.parametrize(
    '_input, value',
    [
        ('set1d_012', 9),
        ('setNd_012', (0, 9)),
    ],
)
def test_set_contains_not(request, _input, value):
    input = request.getfixturevalue(_input)
    assert value not in input


@pytest.mark.parametrize(
    '_input, expected',
    [
        ('set1d_emp', 0),
        ('set1d_0', 1),
        ('set1d_012', 3),
        ('setNd_emp', 0),
        ('setNd_0', 1),
        ('setNd_012', 3),
    ],
)
def test_set_len(request, _input, expected):
    input = request.getfixturevalue(_input)
    assert len(input) == expected


@pytest.mark.parametrize(
    '_input, elem, expected',
    [
        ('set1d_012', 0, 0),
        ('set1d_012', 2, 2),
        ('setNd_012', (0, 0), 0),
        ('setNd_012', (0, 2), 2),
    ],
)
def test_set_index_pass(request, _input, elem, expected):
    input = request.getfixturevalue(_input)
    assert input.index(elem) == expected


@pytest.mark.parametrize(
    '_input, elem',
    [
        ('set1d_emp', 0),
        ('set1d_012', -1),
        ('setNd_emp', (0, 0)),
        ('setNd_012', (0, -1)),
    ],
)
def test_set_index_valueerror(request, _input, elem):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError):
        input.index(elem)


@pytest.mark.parametrize(
    '_input, value, expected',
    [
        ('set1d_emp', 9, IndexSet1D([9])),
        ('set1d_01', 9, IndexSet1D([0, 1, 9])),
        ('set1d_01', 'A', IndexSet1D([0, 1, 'A'])),
        ('set1d_01', 9.0, IndexSet1D([0, 1, 9.0])),
        ('setNd_emp', (0, 9), IndexSetND([(0, 9)])),
        ('setNd_01', (0, 9), IndexSetND([(0, 0), (0, 1), (0, 9)])),
        ('setNd_01', ('A', 'B'), IndexSetND([(0, 0), (0, 1), ('A', 'B')])),
        ('setNd_01', (0.0, 9.0), IndexSetND([(0, 0), (0, 1), (0.0, 9.0)])),
    ],
)
def test_set_append_pass(request, _input, value, expected):
    input = request.getfixturevalue(_input)
    input.append(value)
    assert_sets_same(input, expected)


@pytest.mark.parametrize(
    '_input, value',
    [
        ('set1d_012', 0),
        ('set1d_012', 0.0),
        ('setNd_012', (0, 0)),
        ('setNd_012', (0.0, 0.0)),
    ],
)
def test_set_append_elem_duplicates(request, _input, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError), assert_not_mutated(input):
        input.append(value)


@pytest.mark.parametrize(
    'value',
    [
        (2, 3, 4),
        [['A', 'B'], ['C', 'D']],
    ],
)
def test_set1d_append_elem_nonscalar(set1d_01, value):
    with pytest.raises(TypeError), assert_not_mutated(set1d_01):
        set1d_01.append(value)


@pytest.mark.parametrize('value', [[2, 3], 'X', 5.0])
def test_tupleset_append_elem_nontuple(setNd_01, value):
    with pytest.raises(TypeError), assert_not_mutated(setNd_01):
        setNd_01.append(value)


@pytest.mark.parametrize('value', [(0,), (0, 0, 0)])
def test_tupleset_append_elem_difflen(setNd_01, value):
    with pytest.raises(ValueError), assert_not_mutated(setNd_01):
        setNd_01.append(value)


@pytest.mark.parametrize(
    '_input, values, expected',
    [
        ('set1d_emp', [8, 9], IndexSet1D([8, 9])),
        ('set1d_01', [8, 9], IndexSet1D([0, 1, 8, 9])),
        ('set1d_emp', IndexSet1D([8, 9]), IndexSet1D([8, 9])),
        ('set1d_01', IndexSet1D([8, 9]), IndexSet1D([0, 1, 8, 9])),
        ('set1d_emp', (8, 9), IndexSet1D([8, 9])),
        ('set1d_01', (8, 9), IndexSet1D([0, 1, 8, 9])),
        ('set1d_emp', {8, 9}, IndexSet1D([8, 9])),
        ('set1d_01', {8, 9}, IndexSet1D([0, 1, 8, 9])),
        ('set1d_01', 'ABC', IndexSet1D([0, 1, 'A', 'B', 'C'])),
        ('set1d_01', [9.0], IndexSet1D([0, 1, 9.0])),
        ('setNd_emp', IndexSetND([(0, 8), (0, 9)]), IndexSetND([(0, 8), (0, 9)])),
        ('setNd_01', IndexSetND([(0, 8), (0, 9)]), IndexSetND([(0, 0), (0, 1), (0, 8), (0, 9)])),
        ('setNd_emp', [(0, 8), (0, 9)], IndexSetND([(0, 8), (0, 9)])),
        ('setNd_01', [(0, 8), (0, 9)], IndexSetND([(0, 0), (0, 1), (0, 8), (0, 9)])),
        ('setNd_emp', ((0, 8), (0, 9)), IndexSetND([(0, 8), (0, 9)])),
        ('setNd_01', ((0, 8), (0, 9)), IndexSetND([(0, 0), (0, 1), (0, 8), (0, 9)])),
        ('setNd_emp', {(0, 8), (0, 9)}, IndexSetND([(0, 8), (0, 9)])),
        ('setNd_01', {(0, 8), (0, 9)}, IndexSetND([(0, 0), (0, 1), (0, 8), (0, 9)])),
        (
            'setNd_01',
            [('A', 'B'), ('C', 'D')],
            IndexSetND([(0, 0), (0, 1), ('A', 'B'), ('C', 'D')]),
        ),
        ('setNd_01', [(0.0, 9.0)], IndexSetND([(0, 0), (0, 1), (0.0, 9.0)])),
    ],
)
def test_set_extend_pass(request, _input, values, expected):
    input = request.getfixturevalue(_input)
    input.extend(values)
    assert_sets_same(input, expected)


@pytest.mark.parametrize('_input', ['set1d_01', 'setNd_01'])
@pytest.mark.parametrize('values', [1, 1.9, int])
def test_set_extend_noniterable(request, _input, values):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError), assert_not_mutated(input):
        input.extend(values)


@pytest.mark.parametrize(
    '_input, values',
    [
        ('set1d_012', IndexSet1D([0, 9])),
        ('set1d_012', [0, 9]),
        ('set1d_012', [0.0, 9]),
        ('setNd_012', IndexSetND([(0, 0), (9, 9)])),
        ('setNd_012', [(0, 0), (9, 9)]),
        ('setNd_012', [(0.0, 0.0), (9, 9)]),
    ],
)
def test_set_extend_elem_duplicates(request, _input, values):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError), assert_not_mutated(input):
        input.extend(values)


@pytest.mark.parametrize(
    'value',
    [
        [8, (9, 9)],
        [(8, 8), (9, 9)],
        [(8, 8), 9],
    ],
)
def test_set1d_extend_elem_nonscalar(set1d_01, value):
    with pytest.raises(TypeError), assert_not_mutated(set1d_01):
        set1d_01.extend(value)


@pytest.mark.parametrize(
    'value',
    [
        [[2, 3], 9],
        'XY',
        [5.0, 6.0],
    ],
)
def test_tupleset_extend_elem_nontuple(setNd_01, value):
    with pytest.raises(TypeError), assert_not_mutated(setNd_01):
        setNd_01.extend(value)


@pytest.mark.parametrize(
    'value',
    [
        [(0,), (0, 9)],
        [(0, 9), (0, 0, 0)],
    ],
)
def test_tupleset_extend_elem_difflen(setNd_01, value):
    with pytest.raises(ValueError), assert_not_mutated(setNd_01):
        setNd_01.extend(value)


@pytest.mark.parametrize(
    '_input, index, value, expected',
    [
        ('set1d_012', 0, 9, IndexSet1D([9, 0, 1, 2])),
        ('set1d_012', 2, 9, IndexSet1D([0, 1, 9, 2])),
        ('set1d_012', -1, 9, IndexSet1D([0, 1, 9, 2])),
        ('set1d_012', -3, 9, IndexSet1D([9, 0, 1, 2])),
        ('set1d_012', 9, 9, IndexSet1D([0, 1, 2, 9])),
        ('set1d_012', -9, 9, IndexSet1D([9, 0, 1, 2])),
        ('setNd_012', 0, (0, 9), IndexSetND([(0, 9), (0, 0), (0, 1), (0, 2)])),
        ('setNd_012', 2, (0, 9), IndexSetND([(0, 0), (0, 1), (0, 9), (0, 2)])),
        ('setNd_012', -1, (0, 9), IndexSetND([(0, 0), (0, 1), (0, 9), (0, 2)])),
        ('setNd_012', -3, (0, 9), IndexSetND([(0, 9), (0, 0), (0, 1), (0, 2)])),
        ('setNd_012', 9, (0, 9), IndexSetND([(0, 0), (0, 1), (0, 2), (0, 9)])),
        ('setNd_012', -9, (0, 9), IndexSetND([(0, 9), (0, 0), (0, 1), (0, 2)])),
    ],
)
def test_set_insert_pass(request, _input, index, value, expected):
    input = request.getfixturevalue(_input)
    input.insert(index, value)
    assert_sets_same(input, expected)


@pytest.mark.parametrize(
    '_input, index, value',
    [
        ('set1d_012', 1, 0),
        ('set1d_012', 1, 0.0),
        ('setNd_012', 1, (0, 0)),
        ('setNd_012', 1, (0.0, 0.0)),
    ],
)
def test_set_insert_elem_duplicates(request, _input, index, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError), assert_not_mutated(input):
        input.insert(index, value)


@pytest.mark.parametrize(
    '_input, value',
    [
        ('set1d_012', 9),
        ('setNd_012', (0, 9)),
    ],
)
@pytest.mark.parametrize('index', [0.0, 'a', int])
def test_set_insert_index_typeerror(request, _input, index, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError), assert_not_mutated(input):
        input.insert(index, value)


@pytest.mark.parametrize(
    'value',
    [
        (2, 3, 4),
        [['A', 'B'], ['C', 'D']],
    ],
)
def test_set1d_insert_elem_nonscalar(set1d_01, value):
    with pytest.raises(TypeError), assert_not_mutated(set1d_01):
        set1d_01.insert(0, value)


@pytest.mark.parametrize('value', [[2, 3], 'X', 5.0])
def test_tupleset_insert_elem_nontuple(setNd_01, value):
    with pytest.raises(TypeError), assert_not_mutated(setNd_01):
        setNd_01.insert(0, value)


@pytest.mark.parametrize('value', [(0,), (0, 0, 0)])
def test_tupleset_insert_elem_difflen(setNd_01, value):
    with pytest.raises(ValueError), assert_not_mutated(setNd_01):
        setNd_01.insert(0, value)


@pytest.mark.parametrize(
    '_input, value, expected',
    [
        ('set1d_0', 0, IndexSet1D()),
        ('set1d_012', 0, IndexSet1D([1, 2])),
        ('set1d_012', 0.0, IndexSet1D([1, 2])),
        ('set1d_012', 2, IndexSet1D([0, 1])),
        ('setNd_0', (0, 0), IndexSetND()),
        ('setNd_012', (0, 0), IndexSetND([(0, 1), (0, 2)])),
        ('setNd_012', (0.0, 0.0), IndexSetND([(0, 1), (0, 2)])),
        ('setNd_012', (0, 2), IndexSetND([(0, 0), (0, 1)])),
    ],
)
def test_set_remove_pass(request, _input, value, expected):
    input = request.getfixturevalue(_input)
    input.remove(value)
    assert_sets_same(input, expected)


@pytest.mark.parametrize(
    '_input, value',
    [
        ('set1d_012', 9),
        ('set1d_012', 'abc'),
        ('setNd_012', (0, 9)),
        ('setNd_012', (0, 0, 0)),
    ],
)
def test_set_remove_valueerr(request, _input, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError), assert_not_mutated(input):
        input.remove(value)


@pytest.mark.parametrize(
    '_input, index, expected',
    [
        ('set1d_012', 0, 0),
        ('set1d_012', -1, 2),
        ('set1d_012', 1, 1),
        ('setNd_012', 0, (0, 0)),
        ('setNd_012', -1, (0, 2)),
        ('setNd_012', 1, (0, 1)),
    ],
)
def test_set_pop_pass(request, _input, index, expected):
    input = request.getfixturevalue(_input)
    assert expected == input.pop(index)


@pytest.mark.parametrize(
    '_input, index',
    [
        ('set1d_emp', 0),
        ('set1d_012', 3),
        ('set1d_012', -4),
        ('setNd_emp', 0),
        ('setNd_012', 3),
        ('setNd_012', -4),
    ],
)
def test_set_pop_indexerr(request, _input, index):
    input = request.getfixturevalue(_input)
    with pytest.raises(IndexError), assert_not_mutated(input):
        _value = input.pop(index)


@pytest.mark.parametrize(
    '_input, _expected',
    [
        ('set1d_emp', 'set1d_emp'),
        ('set1d_012', 'set1d_emp'),
        ('setNd_emp', 'setNd_emp'),
        ('setNd_012', 'setNd_emp'),
    ],
)
def test_set_clear_output_pass(request, _input, _expected):
    input = request.getfixturevalue(_input)
    expected = request.getfixturevalue(_expected)
    input.clear()
    assert_sets_same(input, expected)
