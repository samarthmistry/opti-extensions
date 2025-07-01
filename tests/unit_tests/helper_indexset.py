# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Helper functionality for testing index-sets."""

from contextlib import contextmanager
from copy import deepcopy


def assert_sets_same(first, second):
    """Run assertions to verify that the first set is same as the second set.

    Parameters
    ----------
    first : IndexSet1D or IndexSetND
        The first set.
    second : IndexSet1D or IndexSetND
        The second set.

    Examples
    --------
    >>> from opti_extensions import IndexSet1D

    Pass case:
    >>> assert_sets_same(IndexSet1D([0, 1]), IndexSet1D([0, 1]))

    Fail case:
    >>> assert_sets_same(IndexSet1D([0, 1]), IndexSet1D([0, 1, 2]))
    Traceback (most recent call last):
     ...
    AssertionError
    """
    assert first._list == second._list
    assert first._set == second._set


@contextmanager
def assert_not_mutated(input):
    """Run assertions to verify that the input index-set is not mutated at the end of the operation.

    Intended to be used in conjunction with the `pytest.raises` contextmanager.

    Parameters
    ----------
    input : IndexSet1D or IndexSetND
        Input index-set.

    Yields
    ------
    IndexSet1D or IndexSetND
        Given input index-set.

    Examples
    --------
    >>> import pytest
    >>> from opti_extensions import IndexSet1D

    Setup sample test data.
    >>> s = IndexSet1D([0, 1])

    Pass case:
    >>> with pytest.raises(TypeError), assert_not_mutated(s):
    ...     s.append((0, 9))

    Fail case (not used with `pytest.raises` in this one):
    >>> with assert_not_mutated(s):
    ...     assert s.append(2) == IndexSet1D([0, 1, 2])
    Traceback (most recent call last):
     ...
    AssertionError
    """
    ref = deepcopy(input)
    try:
        yield input
    finally:
        assert_sets_same(input, ref)
