# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Iteration methods of IndexSet1D & IndexSetND."""

import pytest


@pytest.mark.parametrize(
    '_input, expected',
    [
        ('set1d_emp', []),
        ('set1d_012', [0, 1, 2]),
        ('setNd_emp', []),
        ('setNd_012', [(0, 0), (0, 1), (0, 2)]),
    ],
)
def test_set_iter(request, _input, expected):
    input = request.getfixturevalue(_input)
    iterator = input.__iter__()
    for value in expected:
        assert next(iterator) == value
    with pytest.raises(StopIteration):
        next(iterator)


@pytest.mark.parametrize(
    '_input, expected',
    [
        ('set1d_emp', []),
        ('set1d_012', [2, 1, 0]),
        ('setNd_emp', []),
        ('setNd_012', [(0, 2), (0, 1), (0, 0)]),
    ],
)
def test_set_reversed(request, _input, expected):
    input = request.getfixturevalue(_input)
    rv_iterator = input.__reversed__()
    for value in expected:
        assert next(rv_iterator) == value
    with pytest.raises(StopIteration):
        next(rv_iterator)
