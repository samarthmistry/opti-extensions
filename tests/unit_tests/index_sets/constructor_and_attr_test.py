# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""IndexSet1D & IndexSetND constructor."""

from collections import abc

import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_sets_same


@pytest.mark.parametrize(
    'input, expected',
    [
        (IndexSet1D(), IndexSet1D()),
        (IndexSet1D([]), IndexSet1D()),
        (IndexSet1D(range(3)), IndexSet1D([0, 1, 2])),
        (IndexSet1D(['A', 3, 1.9]), IndexSet1D(['A', 3, 1.9])),
        (IndexSet1D('XYZ'), IndexSet1D(['X', 'Y', 'Z'])),
        (IndexSetND(), IndexSetND()),
        (IndexSetND([]), IndexSetND()),
        (IndexSetND([], []), IndexSetND()),
        (IndexSetND(range(2), range(2)), IndexSetND([(0, 0), (0, 1), (1, 0), (1, 1)])),
        (
            IndexSetND(IndexSet1D(range(2)), IndexSet1D(range(2))),
            IndexSetND([(0, 0), (0, 1), (1, 0), (1, 1)]),
        ),
        (IndexSetND(range(2), ['A', 'B']), IndexSetND([(0, 'A'), (0, 'B'), (1, 'A'), (1, 'B')])),
        (
            IndexSetND(IndexSet1D(range(2)), ['A', 'B']),
            IndexSetND([(0, 'A'), (0, 'B'), (1, 'A'), (1, 'B')]),
        ),
        (
            IndexSetND(range(2), [(5, 5), (6, 6)]),
            IndexSetND([(0, 5, 5), (0, 6, 6), (1, 5, 5), (1, 6, 6)]),
        ),
        (
            IndexSetND(range(2), IndexSetND(range(1), range(2))),
            IndexSetND([(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0, 1)]),
        ),
        (IndexSetND([[0, 'A'], [1, 'B']]), IndexSetND([(0, 'A'), (1, 'B')])),
    ],
)
def test_set_init_pass(input, expected):
    assert_sets_same(input, expected)


#  Separate class and input data as constructing it within parametrize will raise the error
#  at runtime.


@pytest.mark.parametrize('cls', [IndexSet1D, IndexSetND])
@pytest.mark.parametrize('input', [1, 1.9, int])
def test_set_init_notiterable1(cls, input):
    with pytest.raises(TypeError):
        cls(input)


@pytest.mark.parametrize(
    'input',
    [
        (1, 2),
        (range(2), 2),
        (1, {2, 3}),
    ],
)
def test_set_init_notiterable2(input):
    with pytest.raises(TypeError):
        IndexSetND(*input)


@pytest.mark.parametrize(
    'cls, input',
    [
        (IndexSet1D, ([0, 0, 1],)),
        (IndexSet1D, ([0, 0.0, 1],)),
        (IndexSet1D, ('BAA',)),
        (IndexSetND, (range(2), ['A', 'A'])),
        (IndexSetND, ([(0, 'A'), (0, 'A'), (1, 'B')],)),
        (IndexSetND, ([(0, 'A'), (0.0, 'A'), (1, 'B')],)),
    ],
)
def test_set_init_elem_duplicates(cls, input):
    with pytest.raises(ValueError):
        cls(*input)


@pytest.mark.parametrize(
    'input',
    [
        (0, 1, (2, 3, 4)),
        [['A', 'B'], ['C', 'D']],
    ],
)
def test_set1d_init_elem_nonscalar(input):
    with pytest.raises(TypeError):
        IndexSet1D(input)


@pytest.mark.parametrize(
    'input',
    [
        [0, 1, 2],
        range(3),
        [1, ('A', 'B')],
    ],
)
def test_setNd_init_elem_nontuple(input):
    with pytest.raises(TypeError):
        IndexSetND(input)


@pytest.mark.parametrize(
    'input',
    [
        [(0, 'A'), (1, 'B'), (2, 'C', 'D')],
        [(0, 'A', 3.0), (1, 'B'), (2,)],
    ],
)
def test_setNd_init_elem_difflen(input):
    with pytest.raises(ValueError):
        IndexSetND(input)


@pytest.mark.parametrize(
    'input, expected',
    [
        [None, None],
        (['A', 'B'], ['A', 'B']),
        (('A', 'B'), ['A', 'B']),
        (('A', 'B', 'C'), ['A', 'B', 'C']),
        # ^ valid because IndexSetND doesn't enforce the names to conform with len of tuple-elements
    ],
)
def test_setNd_init_names_pass(input, expected):
    t = IndexSetND(range(2), range(2), names=input)
    assert t.names == expected


@pytest.mark.parametrize(
    'input',
    [123, 'ABC', [1, 2, 3], [1, 'A', 'B'], {'A', 'B', 'C'}],
)
def test_setNd_init_names_typeerr(input):
    with pytest.raises(TypeError):
        IndexSetND(range(2), range(2), names=input)


@pytest.mark.parametrize('input', [('C', 'D'), ['A', 'B', 'C']])
def test_setNd_init_names_update_pass(input):
    t = IndexSetND(range(2), range(2), names=['A', 'B'])
    t.names = input
    assert t.names == list(input)


@pytest.mark.parametrize('input', ['CD', 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_setNd_init_names_update_typeerr(input):
    t = IndexSetND(range(2), range(2), names=['A', 'B'])
    with pytest.raises(TypeError):
        t.names = input


@pytest.mark.parametrize('name', [None, 'KEY'])
def test_set1d_init_name_pass(name):
    s = IndexSet1D(range(3), name=name)
    assert s.name == name


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), {'ABC'}])
def test_set1d_init_name_typeerr(input):
    with pytest.raises(TypeError):
        IndexSet1D(range(3), name=input)


@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_set1d_init_name_update_pass(input):
    s = IndexSet1D(range(3), name='ABC')
    s.name = input
    assert s.name == input


@pytest.mark.parametrize('input', [('C', 'D'), 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_set1d_init_name_update_typeerr(input):
    s = IndexSet1D(range(3), name='ABC')
    with pytest.raises(TypeError):
        s.name = input


@pytest.mark.parametrize('_input', ['set1d_012', 'setNd_012'])
def test_set_isinstance_collections_abc(request, _input):
    input = request.getfixturevalue(_input)

    assert isinstance(input, abc.Container)
    assert isinstance(input, abc.Iterable)
    assert isinstance(input, abc.Reversible)
    assert isinstance(input, abc.Sized)
    assert isinstance(input, abc.Collection)
    assert isinstance(input, abc.Sequence)
    assert isinstance(input, abc.MutableSequence)
