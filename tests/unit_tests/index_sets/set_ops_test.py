# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Set operation methods of IndexSet1D & IndexSetND."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_not_mutated


@pytest.mark.parametrize('cls', ['IS', list, set, dict.fromkeys])
@pytest.mark.parametrize(
    '_input, _other, expected',
    [
        ('set1d_emp', 'set1d_01', True),
        ('set1d_0', 'set1d_01', False),
        ('set1d_345', 'set1d_01', True),
        ('setNd_emp', 'setNd_01', True),
        ('setNd_0', 'setNd_01', False),
        ('setNd_345', 'setNd_01', True),
    ],
)
def test_set_disjoint_pass(cls, request, _input, _other, expected):
    input, other = request.getfixturevalue(_input), request.getfixturevalue(_other)
    if cls != 'IS':
        other = cls(other)
    assert input.isdisjoint(other) is expected


@pytest.mark.parametrize('_input', ['set1d_emp', 'setNd_emp', 'set1d_0', 'setNd_0'])
@pytest.mark.parametrize('other', [0.0, 123, None])
def test_set_disjoint_typerr(request, _input, other):
    input = request.getfixturevalue(_input)
    with pytest.raises(TypeError):
        input.isdisjoint(other)


set_op_test_cases = [
    ('set1d_emp', 'set1d_01', 'set1d_01', 'set1d_emp', 'set1d_emp', 'set1d_01'),
    ('set1d_0', 'set1d_01', 'set1d_01', 'set1d_0', 'set1d_emp', IndexSet1D([1])),
    ('set1d_01', 'set1d_01', 'set1d_01', 'set1d_01', 'set1d_emp', 'set1d_emp'),
    (
        'set1d_345',
        'set1d_01',
        IndexSet1D([0, 1, 3, 4, 5]),
        'set1d_emp',
        'set1d_345',
        IndexSet1D([0, 1, 3, 4, 5]),
    ),
    ('set1d_345', 'set1d_emp', 'set1d_345', 'set1d_emp', 'set1d_345', 'set1d_345'),
    ('setNd_emp', 'setNd_01', 'setNd_01', 'setNd_emp', 'setNd_emp', 'setNd_01'),
    ('setNd_0', 'setNd_01', 'setNd_01', 'setNd_0', 'setNd_emp', IndexSetND([(0, 1)])),
    ('setNd_01', 'setNd_01', 'setNd_01', 'setNd_01', 'setNd_emp', 'setNd_emp'),
    (
        'setNd_345',
        'setNd_01',
        IndexSetND([(0, 0), (0, 1), (0, 3), (0, 4), (0, 5)]),
        'setNd_emp',
        'setNd_345',
        IndexSetND([(0, 0), (0, 1), (0, 3), (0, 4), (0, 5)]),
    ),
    ('setNd_345', 'setNd_emp', 'setNd_345', 'setNd_emp', 'setNd_345', 'setNd_345'),
]


@pytest.mark.parametrize('cls', ['IS', list, set, dict.fromkeys])
@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_methods(
    request, cls, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), request.getfixturevalue(_other)
    if cls != 'IS':
        other = cls(other)

    exp_union = request.getfixturevalue(_exp_union) if isinstance(_exp_union, str) else _exp_union
    exp_intscn = (
        request.getfixturevalue(_exp_intscn) if isinstance(_exp_intscn, str) else _exp_intscn
    )
    exp_diff = request.getfixturevalue(_exp_diff) if isinstance(_exp_diff, str) else _exp_diff
    exp_symdiff = (
        request.getfixturevalue(_exp_symdiff) if isinstance(_exp_symdiff, str) else _exp_symdiff
    )

    assert input.union(other) == exp_union
    assert input.intersection(other) == exp_intscn
    assert input.difference(other) == exp_diff
    assert input.symmetric_difference(other) == exp_symdiff

    name_attr = 'name' if isinstance(input, IndexSet1D) else 'names'

    assert getattr(input.union(other), name_attr) == getattr(exp_union, name_attr)
    assert getattr(input.intersection(other), name_attr) == getattr(exp_intscn, name_attr)
    assert getattr(input.difference(other), name_attr) == getattr(exp_diff, name_attr)
    assert getattr(input.symmetric_difference(other), name_attr) == getattr(exp_symdiff, name_attr)


@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_operators_pass(
    request, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), request.getfixturevalue(_other)
    exp_union = request.getfixturevalue(_exp_union) if isinstance(_exp_union, str) else _exp_union
    exp_intscn = (
        request.getfixturevalue(_exp_intscn) if isinstance(_exp_intscn, str) else _exp_intscn
    )
    exp_diff = request.getfixturevalue(_exp_diff) if isinstance(_exp_diff, str) else _exp_diff
    exp_symdiff = (
        request.getfixturevalue(_exp_symdiff) if isinstance(_exp_symdiff, str) else _exp_symdiff
    )

    assert input | other == exp_union
    assert input & other == exp_intscn
    assert input - other == exp_diff
    assert input ^ other == exp_symdiff

    name_attr = 'name' if isinstance(input, IndexSet1D) else 'names'

    assert getattr(input.union(other), name_attr) == getattr(exp_union, name_attr)
    assert getattr(input.intersection(other), name_attr) == getattr(exp_intscn, name_attr)
    assert getattr(input.difference(other), name_attr) == getattr(exp_diff, name_attr)
    assert getattr(input.symmetric_difference(other), name_attr) == getattr(exp_symdiff, name_attr)


@pytest.mark.parametrize('cls', [list, set, dict.fromkeys])
@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_operators_typerr(
    request, cls, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), cls(request.getfixturevalue(_other))

    with pytest.raises(TypeError):
        _ = input | other
    with pytest.raises(TypeError):
        _ = input & other
    with pytest.raises(TypeError):
        _ = input - other
    with pytest.raises(TypeError):
        _ = input ^ other


@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_union_inplace_pass(
    request, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), request.getfixturevalue(_other)
    exp_union = request.getfixturevalue(_exp_union) if isinstance(_exp_union, str) else _exp_union

    input |= other
    assert input == exp_union


@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_intersection_inplace_pass(
    request, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), request.getfixturevalue(_other)
    exp_intscn = (
        request.getfixturevalue(_exp_intscn) if isinstance(_exp_intscn, str) else _exp_intscn
    )

    input &= other
    assert input == exp_intscn


@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_difference_inplace_pass(
    request, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), request.getfixturevalue(_other)
    exp_diff = request.getfixturevalue(_exp_diff) if isinstance(_exp_diff, str) else _exp_diff

    input -= other
    assert input == exp_diff


@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_symdifference_inplace_pass(
    request, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), request.getfixturevalue(_other)
    exp_symdiff = (
        request.getfixturevalue(_exp_symdiff) if isinstance(_exp_symdiff, str) else _exp_symdiff
    )

    input ^= other
    assert input == exp_symdiff


@pytest.mark.parametrize('cls', [list, set, dict.fromkeys])
@pytest.mark.parametrize(
    '_input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff', set_op_test_cases
)
def test_set_set_operator_inplace_typerr(
    request, cls, _input, _other, _exp_union, _exp_intscn, _exp_diff, _exp_symdiff
):
    input, other = request.getfixturevalue(_input), cls(request.getfixturevalue(_other))

    with pytest.raises(TypeError), assert_not_mutated(input):
        input |= other
    with pytest.raises(TypeError), assert_not_mutated(input):
        input &= other
    with pytest.raises(TypeError), assert_not_mutated(input):
        input -= other
    with pytest.raises(TypeError), assert_not_mutated(input):
        input ^= other
