# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Rich comparison methods of IndexSet1D & IndexSetND."""

from copy import deepcopy

import pytest

from opti_extensions import IndexSet1D


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_0', 'set1d_01'),
        ('setNd_0', 'setNd_01'),
    ],
)
def test_set_is_lt(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert left < right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_emp', 'set1d_emp'),
        ('set1d_01', 'set1d_01'),
        ('set1d_012', 'set1d_01'),
        ('setNd_emp', 'setNd_emp'),
        ('setNd_01', 'setNd_01'),
        ('setNd_012', 'setNd_01'),
    ],
)
def test_set_not_lt(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert not left < right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_emp', 'set1d_emp'),
        ('set1d_0', 'set1d_01'),
        ('set1d_01', 'set1d_01'),
        ('setNd_emp', 'setNd_emp'),
        ('setNd_0', 'setNd_01'),
        ('setNd_01', 'setNd_01'),
    ],
)
def test_set_is_le(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert left <= right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_012', 'set1d_01'),
        ('setNd_012', 'setNd_01'),
    ],
)
def test_set_not_le(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert not left <= right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_emp', 'set1d_emp'),
        ('set1d_01', 'set1d_01'),
        ('setNd_emp', 'setNd_emp'),
        ('setNd_01', 'setNd_01'),
    ],
)
def test_set_is_eq(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert left == right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_0', 'set1d_01'),
        ('set1d_012', 'set1d_01'),
        ('setNd_0', 'setNd_01'),
        ('setNd_012', 'setNd_01'),
    ],
)
def test_set_not_eq(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert not left == right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_0', 'set1d_01'),
        ('set1d_012', 'set1d_01'),
        ('setNd_0', 'setNd_01'),
        ('setNd_012', 'setNd_01'),
    ],
)
def test_set_is_ne(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert left != right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_emp', 'set1d_emp'),
        ('set1d_01', 'set1d_01'),
        ('setNd_emp', 'setNd_emp'),
        ('setNd_01', 'setNd_01'),
    ],
)
def test_set_not_ne(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert not left != right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_012', 'set1d_01'),
        ('setNd_012', 'setNd_01'),
    ],
)
def test_set_is_gt(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert left > right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_emp', 'set1d_emp'),
        ('set1d_0', 'set1d_01'),
        ('set1d_01', 'set1d_01'),
        ('setNd_emp', 'setNd_emp'),
        ('setNd_0', 'setNd_01'),
        ('setNd_01', 'setNd_01'),
    ],
)
def test_set_not_gt(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert not left > right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_emp', 'set1d_emp'),
        ('set1d_01', 'set1d_01'),
        ('set1d_012', 'set1d_01'),
        ('setNd_emp', 'setNd_emp'),
        ('setNd_01', 'setNd_01'),
        ('setNd_012', 'setNd_01'),
    ],
)
def test_set_is_ge(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert left >= right


@pytest.mark.parametrize(
    '_left, _right',
    [
        ('set1d_0', 'set1d_01'),
        ('setNd_0', 'setNd_01'),
    ],
)
def test_set_not_ge(request, _left, _right):
    left = request.getfixturevalue(_left)
    right = request.getfixturevalue(_right) if _left != _right else deepcopy(left)
    assert not left >= right


@pytest.mark.parametrize(
    'sym_opr',
    ['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__'],
)
@pytest.mark.parametrize(
    '_left, right',
    [
        ('set1d_01', [0, 1]),
        ('set1d_01', (0, 1)),
        ('set1d_01', {0, 1}),
        ('setNd_01', [(0, 0), (0, 1)]),
        ('setNd_01', ((0, 0), (0, 1))),
        ('setNd_01', {(0, 0), (0, 1)}),
    ],
)
def test_set_sym_opr_invalid(request, _left, sym_opr, right):
    left = request.getfixturevalue(_left)
    with pytest.raises(TypeError):
        getattr(left, sym_opr)(right)


@pytest.mark.parametrize(
    '_left, right',
    [
        ('setNd_0', (IndexSet1D([0, 1]), IndexSet1D([0, 1]))),
        ('setNd_01', (IndexSet1D([0, 1]), IndexSet1D([0, 1]))),
        ('setNd_012', (IndexSet1D([0, 1]), IndexSet1D([0, 1, 2]))),
        ('setNd_0', (IndexSet1D([0]), IndexSet1D([0, 1]))),
        ('setNd_012', (IndexSet1D([0]), IndexSet1D([0, 1, 2]))),
        ('setNd_int_cmb2', (IndexSet1D([0, 1]), IndexSet1D([0, 1]))),
        ('setNd_int_cmb2', (IndexSet1D(range(9)), IndexSet1D(range(9)))),
    ],
)
def test_set_is_le_sparse(request, _left, right):
    left = request.getfixturevalue(_left)
    assert left <= right


@pytest.mark.parametrize(
    '_left, right',
    [
        ('setNd_01', (IndexSet1D([0, 1]), IndexSet1D([0]))),
        ('setNd_012', (IndexSet1D([0, 1]), IndexSet1D([0, 1]))),
        ('setNd_int_cmb3', (IndexSet1D([0]), IndexSet1D([0]), IndexSet1D([0]))),
        ('setNd_int_cmb3', (IndexSet1D([0]), IndexSet1D([0, 1]), IndexSet1D([0]))),
    ],
)
def test_set_not_le_sparse(request, _left, right):
    left = request.getfixturevalue(_left)
    assert not left <= right


@pytest.mark.parametrize(
    '_left, right',
    [
        ('setNd_01', (IndexSet1D([0, 1]),)),
        ('setNd_01', (IndexSet1D([0, 1]), IndexSet1D([0, 1]), IndexSet1D([0, 1]))),
    ],
)
def test_set_is_le_sparse_len_valerr(request, _left, right):
    left = request.getfixturevalue(_left)
    with pytest.raises(ValueError):
        _ = left <= right


@pytest.mark.parametrize(
    '_left, right',
    [
        ('setNd_emp', (IndexSet1D([0, 1]),)),
        ('setNd_emp', (IndexSet1D([0, 1]), IndexSet1D([0, 1]))),
        ('setNd_emp', (IndexSet1D([0, 1]), IndexSet1D([0, 1]), IndexSet1D([0, 1]))),
    ],
)
def test_set_is_le_sparse_emp_lkperr(request, _left, right):
    left = request.getfixturevalue(_left)
    with pytest.raises(LookupError):
        _ = left <= right
