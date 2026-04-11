# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing highspy variable functionality."""

import pytest
from highspy import Highs, HighsVarType

from opti_extensions.highspy import VarDict1D, VarDictND, addVariables


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


# --- Shared fixture aliases for shared test modules ---


@pytest.fixture
def model(mdl):
    return mdl


@pytest.fixture
def add_vars_fn():
    return addVariables


@pytest.fixture
def add_vars_kwargs():
    return {'type': HighsVarType.kContinuous, 'name_prefix': 'VAL'}


@pytest.fixture
def add_vars_kwargs_with_name():
    def _factory(name):
        return {'type': HighsVarType.kContinuous, 'name_prefix': name}

    return _factory


@pytest.fixture
def add_vars_kwargs_nd():
    return {'type': HighsVarType.kContinuous, 'name_prefix': 'VAL'}


@pytest.fixture
def vardict_classes():
    return {'1D': VarDict1D, 'ND': VarDictND}


@pytest.fixture
def create_kwargs(mdl):
    return {'model': mdl, 'type': HighsVarType.kContinuous}


@pytest.fixture
def model_attr_name():
    return 'Highs'


@pytest.fixture
def vartype_attr_name():
    return 'type'


@pytest.fixture
def sum_fn():
    return Highs.qsum


@pytest.fixture
def has_sum_squares():
    return False


@pytest.fixture
def needs_update():
    return False
