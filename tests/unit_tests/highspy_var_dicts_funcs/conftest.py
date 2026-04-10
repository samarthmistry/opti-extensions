# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing variable functionality."""

import pytest
from highspy import Highs

from opti_extensions import IndexSetND


@pytest.fixture(scope='module')
def mdl():
    mdl = Highs()
    yield mdl
    # Highs object doesn't need explicit close/dispose like Gurobi Model?
    # highs.py doesn't show close/dispose method.


@pytest.fixture(scope='module')
def mdl_2():
    mdl_2 = Highs()
    yield mdl_2


@pytest.fixture
def setNd_cmb2():
    return IndexSetND(range(2), range(2))


@pytest.fixture
def setNd_cmb3():
    return IndexSetND(range(2), range(2), range(2))
