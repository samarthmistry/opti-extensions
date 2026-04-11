# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing gurobipy variable functionality."""

import pytest
from gurobipy import GRB, Model, quicksum

from opti_extensions.gurobipy import VarDict1D, VarDictND, addVars


@pytest.fixture(scope='module')
def mdl():
    mdl = Model()
    yield mdl
    mdl.close()


@pytest.fixture(scope='module')
def mdl_2():
    mdl_2 = Model()
    yield mdl_2
    mdl_2.close()


# --- Shared fixture aliases for shared test modules ---


@pytest.fixture
def model(mdl):
    return mdl


@pytest.fixture
def add_vars_fn():
    return addVars


@pytest.fixture
def add_vars_kwargs():
    return {'vtype': GRB.CONTINUOUS, 'name': 'VAL'}


@pytest.fixture
def add_vars_kwargs_with_name():
    def _factory(name):
        return {'vtype': GRB.CONTINUOUS, 'name': name}

    return _factory


@pytest.fixture
def add_vars_kwargs_nd():
    return {'vtype': GRB.CONTINUOUS, 'name': 'VAL'}


@pytest.fixture
def vardict_classes():
    return {'1D': VarDict1D, 'ND': VarDictND}


@pytest.fixture
def create_kwargs(mdl):
    return {'model': mdl, 'vtype': GRB.CONTINUOUS}


@pytest.fixture
def model_attr_name():
    return 'Model'


@pytest.fixture
def vartype_attr_name():
    return 'VType'


@pytest.fixture
def sum_fn():
    return quicksum


@pytest.fixture
def has_sum_squares():
    return True


@pytest.fixture
def needs_update():
    return True
