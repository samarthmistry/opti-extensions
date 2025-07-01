# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Subset selection methods of VarDictND."""

import pytest
import xpress as xp

from opti_extensions.xpress import addVariables


@pytest.mark.parametrize(
    '_input, values, expected',
    [
        ('setNd_cmb2', ('*', 1), [(0, 1), (1, 1)]),
        ('setNd_cmb2', (0, '*'), [(0, 0), (0, 1)]),
        ('setNd_cmb2', (2, '*'), []),
        ('setNd_cmb2', ('*', 2), []),
        ('setNd_cmb3', (0, '*', '*'), [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]),
        ('setNd_cmb3', ('*', 1, '*'), [(0, 1, 0), (0, 1, 1), (1, 1, 0), (1, 1, 1)]),
        ('setNd_cmb3', (0, 1, '*'), [(0, 1, 0), (0, 1, 1)]),
        ('setNd_cmb3', (0, '*', 1), [(0, 0, 1), (0, 1, 1)]),
        ('setNd_cmb3', (2, '*', '*'), []),
        ('setNd_cmb3', (0, '*', 2), []),
    ],
)
def test_subset_keys_pass(prob, request, _input, values, expected):
    indexset = request.getfixturevalue(_input)
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')

    assert v.subset_keys(*values) == expected


@pytest.mark.parametrize('values', [(0, '*'), (0, '*', 2, '*')])
def test_subset_keys_diff_tuplelen(prob, setNd_cmb3, values):
    v = addVariables(prob, setNd_cmb3, vartype=xp.continuous, name='')
    with pytest.raises(ValueError):
        v.subset_keys(*values)


@pytest.mark.parametrize('values', [((0, 1), (0, 0)), [(0, 1)]])
def test_subset_keys_nonscaler(prob, setNd_cmb2, values):
    v = addVariables(prob, setNd_cmb2, vartype=xp.continuous, name='')
    with pytest.raises(TypeError):
        v.subset_keys(*values)


@pytest.mark.parametrize('values', [('*', '*'), (0, 1)])
def test_subset_keys_invalid_values(prob, setNd_cmb2, values):
    v = addVariables(prob, setNd_cmb2, vartype=xp.continuous, name='')
    with pytest.raises(ValueError):
        v.subset_keys(*values)


@pytest.mark.parametrize(
    '_input, values, expected',
    [
        ('setNd_cmb2', ('*', 1), [1, 3]),
        ('setNd_cmb2', (0, '*'), [0, 1]),
        ('setNd_cmb2', (2, '*'), []),
        ('setNd_cmb2', ('*', 2), []),
        ('setNd_cmb3', (0, '*', '*'), [0, 1, 2, 3]),
        ('setNd_cmb3', ('*', 1, '*'), [2, 3, 6, 7]),
        ('setNd_cmb3', (0, 1, '*'), [2, 3]),
        ('setNd_cmb3', (0, '*', 1), [1, 3]),
        ('setNd_cmb3', (2, '*', '*'), []),
        ('setNd_cmb3', (0, '*', 2), []),
    ],
)
def test_subset_values_pass(prob, request, _input, values, expected):
    indexset = request.getfixturevalue(_input)
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')

    assert v.subset_values(*values) == [v[x] for x in v.subset_keys(*values)]


@pytest.mark.parametrize('values', [(0, '*'), (0, '*', 2, '*')])
def test_subset_values_diff_tuplelen(prob, setNd_cmb3, values):
    v = addVariables(prob, setNd_cmb3, vartype=xp.continuous, name='')
    with pytest.raises(ValueError):
        v.subset_values(*values)


@pytest.mark.parametrize('values', [((0, 1), (0, 0)), [(0, 1)]])
def test_subset_values_nonscaler(prob, setNd_cmb2, values):
    v = addVariables(prob, setNd_cmb2, vartype=xp.continuous, name='')
    with pytest.raises(TypeError):
        v.subset_values(*values)


@pytest.mark.parametrize('values', [('*', '*'), (0, 1)])
def test_subset_values_invalid_values(prob, setNd_cmb2, values):
    v = addVariables(prob, setNd_cmb2, vartype=xp.continuous, name='')
    with pytest.raises(ValueError):
        v.subset_values(*values)
