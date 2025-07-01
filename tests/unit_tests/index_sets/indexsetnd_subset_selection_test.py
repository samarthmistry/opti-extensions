# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Subset selection methods of IndexSetND."""

from collections import defaultdict

import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_sets_same


@pytest.mark.parametrize(
    '_input, values, expected',
    [
        ('setNd_int_cmb2', ('*', 1), [(0, 1), (1, 1)]),
        ('setNd_int_cmb2', (0, '*'), [(0, 0), (0, 1)]),
        ('setNd_int_cmb2', (2, '*'), []),
        ('setNd_int_cmb2', ('*', 2), []),
        ('setNd_int_cmb3', (0, '*', '*'), [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]),
        ('setNd_int_cmb3', ('*', 1, '*'), [(0, 1, 0), (0, 1, 1), (1, 1, 0), (1, 1, 1)]),
        ('setNd_int_cmb3', (0, 1, '*'), [(0, 1, 0), (0, 1, 1)]),
        ('setNd_int_cmb3', (0, '*', 1), [(0, 0, 1), (0, 1, 1)]),
        ('setNd_int_cmb3', (2, '*', '*'), []),
        ('setNd_int_cmb3', (0, '*', 2), []),
        ('setNd_str_int_mix', (0, '*', '*'), [(0, 7, 'A'), (0, 8, 'B'), (0, 9, 'B')]),
        ('setNd_str_int_mix', (0, '*', 'B'), [(0, 8, 'B'), (0, 9, 'B')]),
        ('setNd_str_int_mix', (0, '*', 2), []),
    ],
)
def test_subset_pass(request, _input, values, expected):
    input = request.getfixturevalue(_input)
    assert input.subset(*values) == expected


def test_subset_empty():
    ts = IndexSetND()
    with pytest.raises(LookupError):
        ts.subset(0, '*')


@pytest.mark.parametrize('values', [(0, '*'), (0, '*', 2, '*')])
def test_subset_values_diff_tuplelen(values):
    ts = IndexSetND(range(2), range(2), range(2))
    with pytest.raises(ValueError):
        ts.subset(*values)


@pytest.mark.parametrize('values', [((0, 1), (0, 0)), [(0, 1)]])
def test_subset_values_nonscaler(values):
    ts = IndexSetND(range(2), range(2))
    with pytest.raises(TypeError):
        ts.subset(*values)


@pytest.mark.parametrize('values', [('*', '*'), (0, 1)])
def test_subset_values_invalid_values(values):
    ts = IndexSetND(range(2), range(2))
    with pytest.raises(ValueError):
        ts.subset(*values)


@pytest.fixture
def value_1():
    return [(0, 9)]


@pytest.fixture
def expected_1():
    return [(0, 0), (0, 1), (0, 9)]


@pytest.fixture
def expected_2():
    return defaultdict(list, {(0,): [(0, 0), (0, 1), (0, 9)], (1,): [(1, 0), (1, 1)]})


def test_subset_w_addl_elem_append(setNd_int_cmb2, value_1, expected_1):
    _ = setNd_int_cmb2.subset(0, '*')
    setNd_int_cmb2.append(value_1[0])

    assert setNd_int_cmb2.subset(0, '*') == expected_1


def test_subset_w_addl_elem_extend(setNd_int_cmb2, value_1, expected_1):
    _ = setNd_int_cmb2.subset(0, '*')
    setNd_int_cmb2.extend(value_1)

    assert setNd_int_cmb2.subset(0, '*') == expected_1


def test_subset_w_addl_elem_add(setNd_int_cmb2, value_1, expected_1):
    _ = setNd_int_cmb2.subset(0, '*')
    setNd_int_cmb2 = setNd_int_cmb2 + value_1

    assert setNd_int_cmb2.subset(0, '*') == expected_1


def test_subset_w_addl_elem_iadd(setNd_int_cmb2, value_1, expected_1):
    _ = setNd_int_cmb2.subset(0, '*')
    setNd_int_cmb2 += value_1

    assert setNd_int_cmb2.subset(0, '*') == expected_1


@pytest.mark.parametrize(
    'index, value, expected',
    [
        [0, (0, 9), [(0, 9), (0, 1)]],
        [2, (0, 9), [(0, 0), (0, 1), (0, 9)]],
        [slice(0, 2), [(0, 9)], [(0, 9)]],
        [slice(1, 3), [(0, 9)], [(0, 0), (0, 9)]],
    ],
)
def test_subset_w_addl_elem_setitem(setNd_int_cmb2, index, value, expected):
    _ = setNd_int_cmb2.subset(0, '*')
    setNd_int_cmb2[index] = value

    assert setNd_int_cmb2.subset(0, '*') == expected


@pytest.mark.parametrize(
    'index, value, expected',
    [
        [0, (0, 9), [(0, 9), (0, 0), (0, 1)]],
        [5, (0, 9), [(0, 0), (0, 1), (0, 9)]],
    ],
)
def test_subset_w_addl_elem_insert(setNd_int_cmb2, index, value, expected):
    _ = setNd_int_cmb2.subset(0, '*')
    setNd_int_cmb2.insert(index, value)

    assert setNd_int_cmb2.subset(0, '*') == expected


@pytest.mark.parametrize(
    'index, expected',
    [[0, [(0, 1)]], [slice(0, 2), []]],
)
def test_subset_w_rmvd_elem_delitem(setNd_int_cmb2, index, expected):
    _ = setNd_int_cmb2.subset(0, '*')
    del setNd_int_cmb2[index]

    assert setNd_int_cmb2.subset(0, '*') == expected


def test_subset_w_rmvd_elem_remove(setNd_int_cmb2):
    value = (0, 0)
    expected = [(0, 1)]

    _ = setNd_int_cmb2.subset(0, '*')
    _ = setNd_int_cmb2.remove(value)

    assert setNd_int_cmb2.subset(0, '*') == expected


@pytest.mark.parametrize(
    'index, expected',
    [[None, [(0, 0), (0, 1)]], [-3, [(0, 0)]]],
)
def test_subset_w_rmvd_elem_pop(setNd_int_cmb2, index, expected):
    _ = setNd_int_cmb2.subset(0, '*')
    if index is None:
        _ = setNd_int_cmb2.pop()
    else:
        _ = setNd_int_cmb2.pop(index)

    assert setNd_int_cmb2.subset(0, '*') == expected


def test_subset_after_clear(setNd_int_cmb2):
    _ = setNd_int_cmb2.subset(0, '*')
    setNd_int_cmb2.clear()

    with pytest.raises(LookupError):
        setNd_int_cmb2.subset(0, '*')


@pytest.mark.parametrize(
    '_input, indices, expected',
    [
        ('setNd_int_cmb3', (0,), IndexSet1D(range(2))),
        ('setNd_int_cmb3', (0,), IndexSet1D(range(2))),
        ('setNd_int_cmb3', (0, 2), IndexSetND(range(2), range(2))),
        ('setNd_str_int_mix', (0,), IndexSet1D([0, 1])),
        ('setNd_str_int_mix', (0, 2), IndexSetND([(0, 'A'), (0, 'B'), (1, 'A'), (1, 'B')])),
    ],
)
def test_squeeze_pass(request, _input, indices, expected):
    input = request.getfixturevalue(_input)
    assert_sets_same(input.squeeze(*indices), expected)


def test_squeeze_empty():
    ts = IndexSetND()
    with pytest.raises(LookupError):
        ts.squeeze(0)


@pytest.mark.parametrize(
    'indices', [(0.0,), (int,), ([1],), ({1, 2},), (0.0, 0.0), (1, 0.0), (1, int)]
)
def test_squeeze_indices_typeerr(input, indices):
    with pytest.raises(TypeError):
        input.squeeze(*indices)


@pytest.mark.parametrize('indices', [(), (0, 1)])
def test_squeeze_values_invalid_values(indices):
    ts = IndexSetND(range(2), range(2))
    with pytest.raises(ValueError):
        ts.squeeze(*indices)


@pytest.mark.parametrize('indices', [(3,), (0, 3), (3, 1)])
def test_squeeze_values_diff_tuplelen(indices):
    ts = IndexSetND(range(2), range(2))
    with pytest.raises(ValueError):
        ts.squeeze(*indices)


@pytest.mark.parametrize('names', [('A', 'B'), ('A', 'B', 'C')])
def test_squeeze_values_invalid_names(names):
    ts = IndexSetND(range(2), range(2))
    with pytest.raises(ValueError):
        ts.squeeze(0, names=names)


@pytest.mark.parametrize('names', [('A',), ['A']])
def test_squeeze_1D_valid_name(names):
    ts = IndexSetND(range(2), range(2))
    squeezed = ts.squeeze(0, names=names)

    assert squeezed.name == names[0]


@pytest.fixture
def input():
    return IndexSetND(range(1), range(2), range(2))


@pytest.fixture
def value():
    return [(1, 1, 1)]


test_cases = [
    ((0,), IndexSet1D([0, 1])),
    ((1, 2), IndexSetND([(0, 0), (0, 1), (1, 0), (1, 1)])),
    ((0, 2), IndexSetND([(0, 0), (0, 1), (1, 1)])),
]


@pytest.mark.parametrize('indices, expected', test_cases)
def test_squeeze_w_addl_elem_append(input, value, indices, expected):
    _ = input.squeeze(*indices)
    input.append(value[0])

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize('indices, expected', test_cases)
def test_squeeze_w_addl_elem_extend(input, value, indices, expected):
    _ = input.squeeze(*indices)
    input.extend(value)

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize('indices, expected', test_cases)
def test_squeeze_w_addl_elem_add(input, value, indices, expected):
    _ = input.squeeze(*indices)
    input = input + value

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize('indices, expected', test_cases)
def test_squeeze_w_addl_elem_iadd(input, value, indices, expected):
    _ = input.squeeze(*indices)
    input += value

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize(
    'index, value, indices, expected',
    [
        (0, (1, 1, 1), (0,), IndexSet1D([1, 0])),
        (0, (1, 1, 1), (1, 2), IndexSetND([(1, 1), (0, 1), (1, 0)])),
        (2, (1, 1, 1), (0,), IndexSet1D([0, 1])),
        (2, (1, 1, 1), (1, 2), IndexSetND([(0, 0), (0, 1), (1, 1)])),
        (slice(0, 2), [(1, 1, 1)], (0,), IndexSet1D([0, 1])),
        (slice(0, 2), [(1, 1, 1)], (1, 2), IndexSetND([(1, 1), (1, 0)])),
        (slice(1, 3), [(1, 1, 1)], (0,), IndexSet1D([0, 1])),
        (slice(1, 3), [(1, 1, 1)], (1, 2), IndexSetND([(0, 0), (1, 1)])),
    ],
)
def test_squeeze_w_addl_elem_setitem(input, value, indices, expected, index):
    _ = input.squeeze(*indices)
    input[index] = value

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize('indices, expected', test_cases)
@pytest.mark.parametrize('index', [0, 2])
def test_squeeze_w_addl_elem_insert(input, indices, index, value, expected):
    _ = input.squeeze(*indices)
    input.insert(index, value[0])

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize(
    'index, indices, expected',
    [
        [0, (0,), IndexSet1D([0])],
        [0, (1, 2), IndexSetND([(0, 1), (1, 0), (1, 1)])],
        [slice(0, 2), (0,), IndexSet1D([0])],
        [slice(0, 2), (1, 2), IndexSetND([(1, 0), (1, 1)])],
    ],
)
def test_squeeze_w_rmvd_elem_delitem(input, index, indices, expected):
    _ = input.squeeze(*indices)
    del input[index]

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize(
    'value, indices, expected',
    [
        [(0, 0, 0), (0,), IndexSet1D([0])],
        [(0, 0, 0), (1, 2), IndexSetND([(0, 1), (1, 0), (1, 1)])],
        [(0, 1, 1), (0,), IndexSet1D([0])],
        [(0, 1, 1), (1, 2), IndexSetND([(0, 0), (0, 1), (1, 0)])],
    ],
)
def test_squeeze_w_rmvd_elem_remove(input, value, indices, expected):
    _ = input.squeeze(*indices)
    _ = input.remove(value)

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize(
    'index, indices, expected',
    [
        [None, (0,), IndexSet1D([0])],
        [None, (1, 2), IndexSetND([(0, 0), (0, 1), (1, 0)])],
        [0, (0,), IndexSet1D([0])],
        [0, (1, 2), IndexSetND([(0, 1), (1, 0), (1, 1)])],
    ],
)
def test_squeeze_w_rmvd_elem_pop(input, index, indices, expected):
    _ = input.squeeze(*indices)
    if index is None:
        _ = input.pop()
    else:
        _ = input.pop(index)

    assert input.squeeze(*indices) == expected


@pytest.mark.parametrize('sub_val', [('*', 1), ('*', 2), (0, '*'), (2, '*')])
@pytest.mark.parametrize('sqz_idx', [0, 1])
def test_squeeze_after_subset(setNd_int_cmb2, sub_val, sqz_idx):
    _ = setNd_int_cmb2.subset(*sub_val)
    assert_sets_same(setNd_int_cmb2.squeeze(sqz_idx), IndexSet1D(range(2)))


def test_squeeze_after_clear(setNd_int_cmb2):
    _ = setNd_int_cmb2.squeeze(0)
    setNd_int_cmb2.clear()

    with pytest.raises(LookupError):
        setNd_int_cmb2.squeeze(0)
