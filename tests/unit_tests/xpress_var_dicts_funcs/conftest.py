# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing variable functionality."""

import warnings

import pytest
import xpress as xp

from opti_extensions import IndexSetND


@pytest.fixture(scope='module')
def prob():
    with warnings.catch_warnings():
        # Filter out warnings here instead of general pytest settings because
        # tox will run several configurations where xpress is not a dep
        #   filterwarnings = ["ignore::xpress.LicenseWarning"]
        warnings.filterwarnings('ignore', category=xp.LicenseWarning)
        prob = xp.problem()
    yield prob
    prob.reset()


@pytest.fixture(scope='module')
def prob_2():
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=xp.LicenseWarning)
        prob_2 = xp.problem()
    yield prob_2
    prob_2.reset()


@pytest.fixture
def setNd_cmb2():
    return IndexSetND(range(2), range(2))


@pytest.fixture
def setNd_cmb3():
    return IndexSetND(range(2), range(2), range(2))
