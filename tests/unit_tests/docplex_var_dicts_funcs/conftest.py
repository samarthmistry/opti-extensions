# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing docplex variable functionality."""

import pytest
from docplex.mp.model import Model

from opti_extensions.docplex import VarDict1D, VarDictND, add_variables


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


# --- Shared fixture aliases for shared test modules ---


@pytest.fixture
def model(mdl):
    return mdl


@pytest.fixture
def add_vars_fn():
    return add_variables


@pytest.fixture
def add_vars_kwargs():
    return {'vartype': 'C', 'name': 'VAL'}


@pytest.fixture
def add_vars_kwargs_with_name():
    def _factory(name):
        return {'vartype': 'C', 'name': name}

    return _factory


@pytest.fixture
def add_vars_kwargs_nd():
    return {'vartype': 'C', 'name': 'VAL'}


@pytest.fixture
def vardict_classes():
    return {'1D': VarDict1D, 'ND': VarDictND}


@pytest.fixture
def create_kwargs(mdl):
    return {'model': mdl, 'vartype': mdl.continuous_vartype}


@pytest.fixture
def model_attr_name():
    return 'model'


@pytest.fixture
def vartype_attr_name():
    return 'vartype'


@pytest.fixture
def sum_fn(mdl):
    return mdl.sum


@pytest.fixture
def has_sum_squares():
    return True


@pytest.fixture
def needs_update():
    return False
