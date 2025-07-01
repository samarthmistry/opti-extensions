# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Methods for ordering elements of IndexSet1D & IndexSetND."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_not_mutated, assert_sets_same


@pytest.mark.parametrize(
    '_input, key, reverse, expected',
    [
        ('set1d_emp', None, False, IndexSet1D()),
        ('set1d_012', None, True, IndexSet1D([2, 1, 0])),
        (IndexSet1D(['az', 'by', 'cx']), None, False, IndexSet1D(['az', 'by', 'cx'])),
        (IndexSet1D(['by', 'cx', 'az']), None, False, IndexSet1D(['az', 'by', 'cx'])),
        (IndexSet1D(['by', 'az', 'cx']), None, True, IndexSet1D(['cx', 'by', 'az'])),
        (IndexSet1D(['by', 'az', 'cx']), lambda x: x[1], False, IndexSet1D(['cx', 'by', 'az'])),
        (IndexSet1D(['by', 'az', 'cx']), lambda x: x[1], True, IndexSet1D(['az', 'by', 'cx'])),
        ('setNd_emp', None, False, IndexSetND()),
        ('setNd_012', lambda x: x[1], True, IndexSetND([(0, 2), (0, 1), (0, 0)])),
        (IndexSetND([(0, 2), (0, 0), (0, 1)]), None, False, IndexSetND([(0, 0), (0, 1), (0, 2)])),
    ],
)
def test_set_sort_pass(request, _input, key, reverse, expected):
    if isinstance(_input, str):
        input = request.getfixturevalue(_input)
    else:
        input = _input
    input.sort(key=key, reverse=reverse)
    assert_sets_same(input, expected)


@pytest.mark.parametrize(
    'input',
    [
        IndexSet1D([1, '2', 3]),
        IndexSetND([(1, 2), ('5', '6'), (3, 4)]),
    ],
)
def test_set_sort_typeerr(input):
    with pytest.raises(TypeError), assert_not_mutated(input):
        input.sort()


@pytest.mark.parametrize(
    '_input, expected',
    [
        ('set1d_emp', IndexSet1D()),
        ('set1d_012', IndexSet1D([2, 1, 0])),
        ('setNd_emp', IndexSetND()),
        ('setNd_012', IndexSetND([(0, 2), (0, 1), (0, 0)])),
    ],
)
def test_set_reverse_pass(request, _input, expected):
    input = request.getfixturevalue(_input)
    input.reverse()
    assert_sets_same(input, expected)
