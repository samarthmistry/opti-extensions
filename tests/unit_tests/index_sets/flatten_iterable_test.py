# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Function to flatten iterable of nested tuples."""

import pytest

from opti_extensions._index_sets import IndexSetND


@pytest.mark.parametrize(
    'input, expected',
    [
        ((0, ['ABC', 'DEF']), (0, 'ABC', 'DEF')),
        ((0, (1, 2), [3, (4, 5)]), (0, 1, 2, 3, 4, 5)),
    ],
)
def test_flatten_nested_iterable(input, expected):
    assert tuple(IndexSetND._flatten(input)) == expected
