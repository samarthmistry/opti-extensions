# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Shared test logic for subset selection methods of VarDictND."""

import pytest

SUBSET_KEYS_CASES = [
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
]

SUBSET_VALUES_CASES = [
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
]


@pytest.mark.parametrize('_input, values, expected', SUBSET_KEYS_CASES)
def test_subset_keys_pass(model, add_vars_fn, add_vars_kwargs, request, _input, values, expected):
    indexset = request.getfixturevalue(_input)
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    assert v.subset_keys(*values) == expected


@pytest.mark.parametrize('values', [(0, '*'), (0, '*', 2, '*')])
def test_subset_keys_diff_tuplelen(model, add_vars_fn, add_vars_kwargs, setNd_cmb3, values):
    v = add_vars_fn(model, setNd_cmb3, **add_vars_kwargs)
    with pytest.raises(ValueError):
        v.subset_keys(*values)


@pytest.mark.parametrize('values', [((0, 1), (0, 0)), [(0, 1)]])
def test_subset_keys_nonscaler(model, add_vars_fn, add_vars_kwargs, setNd_cmb2, values):
    v = add_vars_fn(model, setNd_cmb2, **add_vars_kwargs)
    with pytest.raises(TypeError):
        v.subset_keys(*values)


@pytest.mark.parametrize('values', [('*', '*'), (0, 1)])
def test_subset_keys_invalid_values(model, add_vars_fn, add_vars_kwargs, setNd_cmb2, values):
    v = add_vars_fn(model, setNd_cmb2, **add_vars_kwargs)
    with pytest.raises(ValueError):
        v.subset_keys(*values)


@pytest.mark.parametrize('_input, values, expected', SUBSET_VALUES_CASES)
def test_subset_values_pass(model, add_vars_fn, add_vars_kwargs, request, _input, values, expected):
    indexset = request.getfixturevalue(_input)
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    assert v.subset_values(*values) == [v[x] for x in v.subset_keys(*values)]


@pytest.mark.parametrize('values', [(0, '*'), (0, '*', 2, '*')])
def test_subset_values_diff_tuplelen(model, add_vars_fn, add_vars_kwargs, setNd_cmb3, values):
    v = add_vars_fn(model, setNd_cmb3, **add_vars_kwargs)
    with pytest.raises(ValueError):
        v.subset_values(*values)


@pytest.mark.parametrize('values', [((0, 1), (0, 0)), [(0, 1)]])
def test_subset_values_nonscaler(model, add_vars_fn, add_vars_kwargs, setNd_cmb2, values):
    v = add_vars_fn(model, setNd_cmb2, **add_vars_kwargs)
    with pytest.raises(TypeError):
        v.subset_values(*values)


@pytest.mark.parametrize('values', [('*', '*'), (0, 1)])
def test_subset_values_invalid_values(model, add_vars_fn, add_vars_kwargs, setNd_cmb2, values):
    v = add_vars_fn(model, setNd_cmb2, **add_vars_kwargs)
    with pytest.raises(ValueError):
        v.subset_values(*values)
