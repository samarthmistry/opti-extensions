# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures testing index-set functionality."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND


@pytest.fixture
def set1d_emp():
    return IndexSet1D()


@pytest.fixture
def set1d_0():
    return IndexSet1D([0])


@pytest.fixture
def set1d_01():
    return IndexSet1D([0, 1])


@pytest.fixture
def set1d_012():
    return IndexSet1D([0, 1, 2])


@pytest.fixture
def setNd_emp():
    return IndexSetND()


@pytest.fixture
def setNd_0():
    return IndexSetND([(0, 0)])


@pytest.fixture
def setNd_01():
    return IndexSetND([(0, 0), (0, 1)])


@pytest.fixture
def setNd_012():
    return IndexSetND([(0, 0), (0, 1), (0, 2)])


@pytest.fixture
def setNd_int_cmb2():
    return IndexSetND(range(2), range(2))


@pytest.fixture
def setNd_int_cmb3():
    return IndexSetND(range(2), range(2), range(2))


@pytest.fixture
def setNd_str_int_mix():
    return IndexSetND([(0, 7, 'A'), (0, 8, 'B'), (0, 9, 'B'), (1, 7, 'A'), (1, 8, 'B')])
