# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Dunder getitem, setitem, delitem of IndexSet1D & IndexSetND."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_not_mutated, assert_sets_same


@pytest.mark.parametrize(
    '_input, index, expected',
    [
        ('set1d_012', 0, 0),
        ('set1d_012', 2, 2),
        ('set1d_012', -1, 2),
        ('set1d_012', -3, 0),
        ('setNd_012', 0, (0, 0)),
        ('setNd_012', 2, (0, 2)),
        ('setNd_012', -1, (0, 2)),
        ('setNd_012', -3, (0, 0)),
    ],
)
def test_set_getitem_index_pass(request, _input, index, expected):
    input = request.getfixturevalue(_input)
    assert input[index] == expected


@pytest.mark.parametrize(
    '_input, slice, expected',
    [
        ('set1d_012', slice(1, 3), [1, 2]),
        ('set1d_012', slice(3, 1), []),
        ('set1d_012', slice(1, None), [1, 2]),
        ('set1d_012', slice(None, 2), [0, 1]),
        ('set1d_012', slice(None, None), [0, 1, 2]),
        ('set1d_012', slice(-3, -1), [0, 1]),
        ('set1d_012', slice(-1, -3), []),
        ('set1d_012', slice(-2, None), [1, 2]),
        ('set1d_012', slice(None, -2), [0]),
        ('setNd_012', slice(1, 3), [(0, 1), (0, 2)]),
        ('setNd_012', slice(3, 1), []),
        ('setNd_012', slice(1, None), [(0, 1), (0, 2)]),
        ('setNd_012', slice(None, 2), [(0, 0), (0, 1)]),
        ('setNd_012', slice(None, None), [(0, 0), (0, 1), (0, 2)]),
        ('setNd_012', slice(-3, -1), [(0, 0), (0, 1)]),
        ('setNd_012', slice(-1, -3), []),
        ('setNd_012', slice(-2, None), [(0, 1), (0, 2)]),
        ('setNd_012', slice(None, -2), [(0, 0)]),
    ],
)
def test_set_getitem_slice_pass(request, _input, slice, expected):
    input = request.getfixturevalue(_input)
    assert input[slice] == expected


getitem_delitem_indexerror_testdata = [
    ('set1d_emp', 0),
    ('set1d_012', 3),
    ('set1d_012', -4),
    ('setNd_emp', 0),
    ('setNd_012', 3),
    ('setNd_012', -4),
]


@pytest.mark.parametrize('_input, index', getitem_delitem_indexerror_testdata)
def test_set_getitem_indexerror(request, _input, index):
    input = request.getfixturevalue(_input)
    with pytest.raises(IndexError):
        input[index]


@pytest.mark.parametrize('_input', ['set1d_012', 'setNd_012'])
@pytest.mark.parametrize('index', [0.0, 'a', int])
def test_set_getitem_index_typeerror(request, _input, index):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError):
        input[index]


@pytest.mark.parametrize(
    '_input, index, value, expected',
    [
        ('set1d_012', 0, 9, IndexSet1D([9, 1, 2])),
        ('set1d_012', 2, 9, IndexSet1D([0, 1, 9])),
        ('set1d_012', -1, 9, IndexSet1D([0, 1, 9])),
        ('set1d_012', -3, 9, IndexSet1D([9, 1, 2])),
        ('setNd_012', 0, (0, 9), IndexSetND([(0, 9), (0, 1), (0, 2)])),
        ('setNd_012', 2, (0, 9), IndexSetND([(0, 0), (0, 1), (0, 9)])),
        ('setNd_012', -1, (0, 9), IndexSetND([(0, 0), (0, 1), (0, 9)])),
        ('setNd_012', -3, (0, 9), IndexSetND([(0, 9), (0, 1), (0, 2)])),
    ],
)
def test_set_setitem_index_pass(request, _input, index, value, expected):
    input = request.getfixturevalue(_input)
    input[index] = value
    assert_sets_same(input, expected)


@pytest.mark.parametrize(
    '_input, index, value',
    [
        ('set1d_emp', 0, 9),
        ('set1d_012', 3, 9),
        ('set1d_012', -4, 9),
        ('setNd_emp', 0, (0, 9)),
        ('setNd_012', 3, (0, 9)),
        ('setNd_012', -4, (0, 9)),
    ],
)
def test_set_setitem_indexerror(request, _input, index, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(IndexError), assert_not_mutated(input):
        input[index] = value


@pytest.mark.parametrize(
    '_input, slice, values, expected',
    [
        ('set1d_012', slice(1, 3), [9], IndexSet1D([0, 9])),
        ('set1d_012', slice(3, 1), [9], IndexSet1D([0, 1, 2, 9])),
        ('set1d_012', slice(1, None), [9], IndexSet1D([0, 9])),
        ('set1d_012', slice(None, 2), [9], IndexSet1D([9, 2])),
        ('set1d_012', slice(None, None), [9], IndexSet1D([9])),
        ('set1d_012', slice(-3, -1), [9], IndexSet1D([9, 2])),
        ('set1d_012', slice(-1, -3), [9], IndexSet1D([0, 1, 9, 2])),
        ('set1d_012', slice(-2, None), [9], IndexSet1D([0, 9])),
        ('set1d_012', slice(None, -2), [9], IndexSet1D([9, 1, 2])),
        ('set1d_emp', slice(1, 3), [9], IndexSet1D([9])),
        ('set1d_emp', slice(3, 1), [9], IndexSet1D([9])),
        ('set1d_emp', slice(1, None), [9], IndexSet1D([9])),
        ('set1d_emp', slice(None, 2), [9], IndexSet1D([9])),
        ('set1d_emp', slice(None, None), [9], IndexSet1D([9])),
        ('set1d_emp', slice(-3, -1), [9], IndexSet1D([9])),
        ('set1d_emp', slice(-1, -3), [9], IndexSet1D([9])),
        ('set1d_emp', slice(-2, None), [9], IndexSet1D([9])),
        ('set1d_emp', slice(None, -2), [9], IndexSet1D([9])),
        ('setNd_012', slice(1, 3), [(0, 9)], IndexSetND([(0, 0), (0, 9)])),
        ('setNd_012', slice(3, 1), [(0, 9)], IndexSetND([(0, 0), (0, 1), (0, 2), (0, 9)])),
        ('setNd_012', slice(1, None), [(0, 9)], IndexSetND([(0, 0), (0, 9)])),
        ('setNd_012', slice(None, 2), [(0, 9)], IndexSetND([(0, 9), (0, 2)])),
        ('setNd_012', slice(None, None), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_012', slice(-3, -1), [(0, 9)], IndexSetND([(0, 9), (0, 2)])),
        ('setNd_012', slice(-1, -3), [(0, 9)], IndexSetND([(0, 0), (0, 1), (0, 9), (0, 2)])),
        ('setNd_012', slice(-2, None), [(0, 9)], IndexSetND([(0, 0), (0, 9)])),
        ('setNd_012', slice(None, -2), [(0, 9)], IndexSetND([(0, 9), (0, 1), (0, 2)])),
        ('setNd_emp', slice(1, 3), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(3, 1), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(1, None), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(None, 2), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(None, None), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(-3, -1), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(-1, -3), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(-2, None), [(0, 9)], IndexSetND([(0, 9)])),
        ('setNd_emp', slice(None, -2), [(0, 9)], IndexSetND([(0, 9)])),
    ],
)
def test_set_setitem_slice_pass(request, _input, slice, values, expected):
    input = request.getfixturevalue(_input)
    input[slice] = values
    assert_sets_same(input, expected)


@pytest.mark.parametrize('_input', ['set1d_012', 'setNd_012'])
@pytest.mark.parametrize('slice', [slice(1, 3)])
@pytest.mark.parametrize('value', [0.0, 9, int])
def test_set_setitem_slice_value_typeerror(request, _input, slice, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError), assert_not_mutated(input):
        input[slice] = value


@pytest.mark.parametrize(
    '_input, index_slice, value',
    [
        ('set1d_012', 1, 0),
        ('set1d_012', 1, 0.0),
        ('set1d_012', slice(1, 3), [0]),
        ('setNd_012', 1, (0, 0)),
        ('setNd_012', 1, (0.0, 0.0)),
        ('setNd_012', slice(1, 3), [(0, 0)]),
    ],
)
def test_set_setitem_elem_duplicates(request, _input, index_slice, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError), assert_not_mutated(input):
        input[index_slice] = value


@pytest.mark.parametrize(
    '_input, value',
    [
        ('set1d_012', 9),
        ('setNd_012', (0, 9)),
    ],
)
@pytest.mark.parametrize('index', [0.0, 'a', int])
def test_set_setitem_index_typeerror(request, _input, index, value):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError), assert_not_mutated(input):
        input[index] = value


@pytest.mark.parametrize(
    'value',
    [
        (2, 3, 4),
        [['A', 'B'], ['C', 'D']],
    ],
)
def test_set1d_setitem_elem_nonscalar(set1d_01, value):
    with pytest.raises(TypeError), assert_not_mutated(set1d_01):
        set1d_01[0] = value


@pytest.mark.parametrize('value', [[2, 3], 'X', 5.0])
def test_tupleset_setitem_elem_nontuple(setNd_01, value):
    with pytest.raises(TypeError), assert_not_mutated(setNd_01):
        setNd_01[0] = value


@pytest.mark.parametrize('value', [(0,), (0, 0, 0)])
def test_tupleset_setitem_elem_difflen(setNd_01, value):
    with pytest.raises(ValueError), assert_not_mutated(setNd_01):
        setNd_01[0] = value


@pytest.mark.parametrize(
    '_input, index, expected',
    [
        ('set1d_012', 0, IndexSet1D([1, 2])),
        ('set1d_012', 2, IndexSet1D([0, 1])),
        ('set1d_012', -1, IndexSet1D([0, 1])),
        ('set1d_012', -3, IndexSet1D([1, 2])),
        ('setNd_012', 0, IndexSetND([(0, 1), (0, 2)])),
        ('setNd_012', 2, IndexSetND([(0, 0), (0, 1)])),
        ('setNd_012', -1, IndexSetND([(0, 0), (0, 1)])),
        ('setNd_012', -3, IndexSetND([(0, 1), (0, 2)])),
    ],
)
def test_set_delitem_index_pass(request, _input, index, expected):
    input = request.getfixturevalue(_input)
    del input[index]
    assert_sets_same(input, expected)


@pytest.mark.parametrize(
    '_input, slice, expected',
    [
        ('set1d_012', slice(1, 3), IndexSet1D([0])),
        ('set1d_012', slice(3, 1), IndexSet1D([0, 1, 2])),
        ('set1d_012', slice(1, None), IndexSet1D([0])),
        ('set1d_012', slice(None, 2), IndexSet1D([2])),
        ('set1d_012', slice(None, None), IndexSet1D()),
        ('set1d_012', slice(-3, -1), IndexSet1D([2])),
        ('set1d_012', slice(-1, -3), IndexSet1D([0, 1, 2])),
        ('set1d_012', slice(-2, None), IndexSet1D([0])),
        ('set1d_012', slice(None, -2), IndexSet1D([1, 2])),
        ('setNd_012', slice(1, 3), IndexSetND([(0, 0)])),
        ('setNd_012', slice(3, 1), IndexSetND([(0, 0), (0, 1), (0, 2)])),
        ('setNd_012', slice(1, None), IndexSetND([(0, 0)])),
        ('setNd_012', slice(None, 2), IndexSetND([(0, 2)])),
        ('setNd_012', slice(None, None), IndexSetND()),
        ('setNd_012', slice(-3, -1), IndexSetND([(0, 2)])),
        ('setNd_012', slice(-1, -3), IndexSetND([(0, 0), (0, 1), (0, 2)])),
        ('setNd_012', slice(-2, None), IndexSetND([(0, 0)])),
        ('setNd_012', slice(None, -2), IndexSetND([(0, 1), (0, 2)])),
    ],
)
def test_set_delitem_slice_pass(request, _input, slice, expected):
    input = request.getfixturevalue(_input)
    del input[slice]
    assert_sets_same(input, expected)


@pytest.mark.parametrize('_input, index', getitem_delitem_indexerror_testdata)
def test_set_delitem_indexerror(request, _input, index):
    input = request.getfixturevalue(_input)
    with pytest.raises(IndexError), assert_not_mutated(input):
        del input[index]


@pytest.mark.parametrize('_input', ['set1d_012', 'setNd_012'])
@pytest.mark.parametrize('index', [0.0, 'a', int])
def test_set_delitem_index_typeerror(request, _input, index):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError), assert_not_mutated(input):
        del input[index]
