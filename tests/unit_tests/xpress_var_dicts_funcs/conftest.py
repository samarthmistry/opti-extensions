# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing xpress variable functionality."""

import warnings

import pytest
import xpress as xp

from opti_extensions.xpress import VarDict1D, VarDictND, addVariables


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


# --- Shared fixture aliases for shared test modules ---


@pytest.fixture
def model(prob):
    return prob


@pytest.fixture
def add_vars_fn():
    return addVariables


@pytest.fixture
def add_vars_kwargs():
    return {'vartype': xp.continuous, 'name': None}


@pytest.fixture
def add_vars_kwargs_with_name():
    def _factory(name):
        return {'vartype': xp.continuous, 'name': name}

    return _factory


@pytest.fixture
def add_vars_kwargs_nd():
    return {'vartype': xp.continuous, 'name': None}


@pytest.fixture
def vardict_classes():
    return {'1D': VarDict1D, 'ND': VarDictND}


@pytest.fixture
def create_kwargs(prob):
    return {'problem': prob, 'vartype': xp.continuous}


@pytest.fixture
def model_attr_name():
    return 'problem'


@pytest.fixture
def vartype_attr_name():
    return 'vartype'


@pytest.fixture
def sum_fn():
    return xp.Sum


@pytest.fixture
def has_sum_squares():
    return True


@pytest.fixture
def needs_update():
    return False
