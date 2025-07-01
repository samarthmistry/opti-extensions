# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Dunder add and iadd methods of IndexSet1D & IndexSetND."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_not_mutated, assert_sets_same

pass_testdata = [
    ('set1d_emp', IndexSet1D(), IndexSet1D()),
    ('set1d_emp', [], IndexSet1D()),
    ('set1d_emp', (), IndexSet1D()),
    ('set1d_emp', IndexSet1D([0, 1]), IndexSet1D([0, 1])),
    ('set1d_emp', [0, 1], IndexSet1D([0, 1])),
    ('set1d_emp', (0, 1), IndexSet1D([0, 1])),
    ('set1d_01', IndexSet1D(), IndexSet1D([0, 1])),
    ('set1d_01', [], IndexSet1D([0, 1])),
    ('set1d_01', (), IndexSet1D([0, 1])),
    ('set1d_01', IndexSet1D([2, 3]), IndexSet1D([0, 1, 2, 3])),
    ('set1d_01', [2, 3], IndexSet1D([0, 1, 2, 3])),
    ('set1d_01', (2, 3), IndexSet1D([0, 1, 2, 3])),
    ('setNd_emp', IndexSetND(), IndexSetND()),
    ('setNd_emp', [], IndexSetND()),
    ('setNd_emp', (), IndexSetND()),
    ('setNd_emp', IndexSetND([(0, 0), (0, 1)]), IndexSetND([(0, 0), (0, 1)])),
    ('setNd_emp', [(0, 0), (0, 1)], IndexSetND([(0, 0), (0, 1)])),
    ('setNd_emp', ((0, 0), (0, 1)), IndexSetND([(0, 0), (0, 1)])),
    ('setNd_01', IndexSetND(), IndexSetND([(0, 0), (0, 1)])),
    ('setNd_01', [], IndexSetND([(0, 0), (0, 1)])),
    ('setNd_01', (), IndexSetND([(0, 0), (0, 1)])),
    ('setNd_01', IndexSetND([(0, 2), (0, 3)]), IndexSetND([(0, 0), (0, 1), (0, 2), (0, 3)])),
    ('setNd_01', [(0, 2), (0, 3)], IndexSetND([(0, 0), (0, 1), (0, 2), (0, 3)])),
    ('setNd_01', ((0, 2), (0, 3)), IndexSetND([(0, 0), (0, 1), (0, 2), (0, 3)])),
]


@pytest.mark.parametrize('_input, other, expected', pass_testdata)
def test_set_add_pass(request, _input, other, expected):
    input = request.getfixturevalue(_input)
    assert_sets_same(input + other, expected)


@pytest.mark.parametrize('_input, other, expected', pass_testdata)
def test_set_iadd_pass(request, _input, other, expected):
    input = request.getfixturevalue(_input)
    input += other
    assert_sets_same(input, expected)


noniterable_testdata1 = ['set1d_01', 'setNd_01']
noniterable_testdata2 = [1, 1.9, int]


@pytest.mark.parametrize('_input', noniterable_testdata1)
@pytest.mark.parametrize('other', noniterable_testdata2)
def test_set_add_notiterable(request, _input, other):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError), assert_not_mutated(input):
        _ = input + other


@pytest.mark.parametrize('_input', noniterable_testdata1)
@pytest.mark.parametrize('other', noniterable_testdata2)
def test_set_iadd_notiterable(request, _input, other):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError), assert_not_mutated(input):
        input += other


duplicates_testdata = [
    ('set1d_01', [0]),
    ('set1d_01', [0.0]),
    ('set1d_01', [2, 2]),
    ('setNd_01', [(0, 0)]),
    ('setNd_01', [(0.0, 0.0)]),
    ('setNd_01', [(0, 2), (0, 2)]),
]


@pytest.mark.parametrize('_input, other', duplicates_testdata)
def test_set_add_elem_duplicates(request, _input, other):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError), assert_not_mutated(input):
        _ = input + other


@pytest.mark.parametrize('_input, other', duplicates_testdata)
def test_set_iadd_elem_duplicates(request, _input, other):
    input = request.getfixturevalue(_input)
    with pytest.raises(ValueError), assert_not_mutated(input):
        input += other


nonscalar_testdata = [[2, (3, 4)], [['A', 'B'], ['C', 'D']]]


@pytest.mark.parametrize('other', nonscalar_testdata)
def test_set1d_add_elem_nonscalar(set1d_01, other):
    with pytest.raises(TypeError), assert_not_mutated(set1d_01):
        _ = set1d_01 + other


@pytest.mark.parametrize('other', nonscalar_testdata)
def test_set1d_iadd_elem_nonscalar(set1d_01, other):
    with pytest.raises(TypeError), assert_not_mutated(set1d_01):
        set1d_01 += other


nontuple_testdata = [[2, 3], ['X', ('A', 'B')]]


@pytest.mark.parametrize('other', nontuple_testdata)
def test_tupleset_add_elem_nontuple(setNd_01, other):
    with pytest.raises(TypeError), assert_not_mutated(setNd_01):
        _ = setNd_01 + other


@pytest.mark.parametrize('other', nontuple_testdata)
def test_tupleset_iadd_elem_nontuple(setNd_01, other):
    with pytest.raises(TypeError), assert_not_mutated(setNd_01):
        setNd_01 += other


add_iadd_difflen_testdata = [[(0, 0, 0), (0, 3)], [(0,), (0, 3)]]


@pytest.mark.parametrize('other', add_iadd_difflen_testdata)
def test_tupleset_add_elem_difflen(setNd_01, other):
    with pytest.raises(ValueError), assert_not_mutated(setNd_01):
        _ = setNd_01 + other


@pytest.mark.parametrize('other', add_iadd_difflen_testdata)
def test_tupleset_iadd_elem_difflen(setNd_01, other):
    with pytest.raises(ValueError), assert_not_mutated(setNd_01):
        setNd_01 += other
