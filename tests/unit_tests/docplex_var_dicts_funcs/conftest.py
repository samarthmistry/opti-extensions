# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing variable functionality."""

import pytest
from docplex.mp.model import Model

from opti_extensions import IndexSetND


@pytest.fixture(scope='module')
def mdl():
    mdl = Model(ignore_names=True)
    yield mdl
    mdl.end()


@pytest.fixture(scope='module')
def mdl_2():
    mdl_2 = Model(ignore_names=True)
    yield mdl_2
    mdl_2.end()


@pytest.fixture
def setNd_cmb2():
    return IndexSetND(range(2), range(2))


@pytest.fixture
def setNd_cmb3():
    return IndexSetND(range(2), range(2), range(2))
