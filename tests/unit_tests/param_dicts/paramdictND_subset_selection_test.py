# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Subset selection methods of ParamDictND."""

import pytest

from opti_extensions import ParamDictND


@pytest.mark.parametrize(
    '_input, values, expected',
    [
        ('paramdictNd_cmb2', ('*', 1), [(0, 1), (1, 1)]),
        ('paramdictNd_cmb2', (0, '*'), [(0, 0), (0, 1)]),
        ('paramdictNd_cmb2', (2, '*'), []),
        ('paramdictNd_cmb2', ('*', 2), []),
        ('paramdictNd_cmb3', (0, '*', '*'), [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]),
        ('paramdictNd_cmb3', ('*', 1, '*'), [(0, 1, 0), (0, 1, 1), (1, 1, 0), (1, 1, 1)]),
        ('paramdictNd_cmb3', (0, 1, '*'), [(0, 1, 0), (0, 1, 1)]),
        ('paramdictNd_cmb3', (0, '*', 1), [(0, 0, 1), (0, 1, 1)]),
        ('paramdictNd_cmb3', (2, '*', '*'), []),
        ('paramdictNd_cmb3', (0, '*', 2), []),
    ],
)
def test_subset_keys_pass(request, _input, values, expected):
    input = request.getfixturevalue(_input)
    assert input.subset_keys(*values) == expected


def test_subset_keys_empty():
    ts = ParamDictND()
    with pytest.raises(LookupError):
        ts.subset_keys(0, '*')


@pytest.mark.parametrize('values', [(0, '*'), (0, '*', 2, '*')])
def test_subset_keys_diff_tuplelen(paramdictNd_cmb3, values):
    with pytest.raises(ValueError):
        paramdictNd_cmb3.subset_keys(*values)


@pytest.mark.parametrize('values', [((0, 1), (0, 0)), [(0, 1)]])
def test_subset_keys_nonscaler(paramdictNd_cmb2, values):
    with pytest.raises(TypeError):
        paramdictNd_cmb2.subset_keys(*values)


@pytest.mark.parametrize('values', [('*', '*'), (0, 1)])
def test_subset_keys_invalid_values(paramdictNd_cmb2, values):
    with pytest.raises(ValueError):
        paramdictNd_cmb2.subset_keys(*values)


@pytest.mark.parametrize(
    'index, value, expected',
    [[(0, 0), 9, [(0, 0), (0, 1)]], [(0, 9), 9, [(0, 0), (0, 1), (0, 9)]]],
)
def test_subset_keys_w_addl_elem_setitem(paramdictNd_cmb2, index, value, expected):
    _ = paramdictNd_cmb2.subset_keys(0, '*')
    paramdictNd_cmb2[index] = value

    assert paramdictNd_cmb2.subset_keys(0, '*') == expected


def test_subset_keys_w_rmvd_elem_delitem(paramdictNd_cmb2):
    _ = paramdictNd_cmb2.subset_keys(0, '*')
    del paramdictNd_cmb2[0, 0]

    assert paramdictNd_cmb2.subset_keys(0, '*') == [(0, 1)]


def test_subset_keys_after_clear(paramdictNd_cmb2):
    _ = paramdictNd_cmb2.subset_keys(0, '*')
    paramdictNd_cmb2.clear()

    with pytest.raises(LookupError):
        paramdictNd_cmb2.subset_keys(0, '*')


@pytest.mark.parametrize(
    '_input, values, expected',
    [
        ('paramdictNd_cmb2', ('*', 1), [1, 3]),
        ('paramdictNd_cmb2', (0, '*'), [0, 1]),
        ('paramdictNd_cmb2', (2, '*'), []),
        ('paramdictNd_cmb2', ('*', 2), []),
        ('paramdictNd_cmb3', (0, '*', '*'), [0, 1, 2, 3]),
        ('paramdictNd_cmb3', ('*', 1, '*'), [2, 3, 6, 7]),
        ('paramdictNd_cmb3', (0, 1, '*'), [2, 3]),
        ('paramdictNd_cmb3', (0, '*', 1), [1, 3]),
        ('paramdictNd_cmb3', (2, '*', '*'), []),
        ('paramdictNd_cmb3', (0, '*', 2), []),
    ],
)
def test_subset_values_pass(request, _input, values, expected):
    input = request.getfixturevalue(_input)
    assert input.subset_values(*values) == expected


def test_subset_values_empty():
    ts = ParamDictND()
    with pytest.raises(LookupError):
        ts.subset_values(0, '*')


@pytest.mark.parametrize('values', [(0, '*'), (0, '*', 2, '*')])
def test_subset_values_diff_tuplelen(paramdictNd_cmb3, values):
    with pytest.raises(ValueError):
        paramdictNd_cmb3.subset_values(*values)


@pytest.mark.parametrize('values', [((0, 1), (0, 0)), [(0, 1)]])
def test_subset_values_nonscaler(paramdictNd_cmb2, values):
    with pytest.raises(TypeError):
        paramdictNd_cmb2.subset_values(*values)


@pytest.mark.parametrize('values', [('*', '*'), (0, 1)])
def test_subset_values_invalid_values(paramdictNd_cmb2, values):
    with pytest.raises(ValueError):
        paramdictNd_cmb2.subset_values(*values)


@pytest.mark.parametrize(
    'index, value, expected',
    [[(0, 0), 9, [9, 1]], [(0, 9), 9, [0, 1, 9]]],
)
def test_subset_values_w_addl_elem_setitem(paramdictNd_cmb2, index, value, expected):
    _ = paramdictNd_cmb2.subset_values(0, '*')
    paramdictNd_cmb2[index] = value

    assert paramdictNd_cmb2.subset_values(0, '*') == expected


def test_subset_values_w_rmvd_elem_delitem(paramdictNd_cmb2):
    _ = paramdictNd_cmb2.subset_values(0, '*')
    del paramdictNd_cmb2[0, 0]

    assert paramdictNd_cmb2.subset_values(0, '*') == [1]


def test_subset_values_after_clear(paramdictNd_cmb2):
    _ = paramdictNd_cmb2.subset_values(0, '*')
    paramdictNd_cmb2.clear()

    with pytest.raises(LookupError):
        paramdictNd_cmb2.subset_values(0, '*')
