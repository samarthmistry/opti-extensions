# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict1D & VarDictND constructor and attributes."""

import pytest
from gurobipy import GRB

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.gurobipy import addVars

# Import all shared tests
from tests.unit_tests._shared_constructor_and_attr_tests import *  # noqa: F401, F403

# ---- Solver-specific: valname update pass ----


@pytest.mark.parametrize('input', ['DEF', 'Z'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_update_pass(mdl, indexset, input):
    v = addVars(mdl, indexset, vtype=GRB.CONTINUOUS, name='VAL')
    v.value_name = input
    assert v.value_name == input


# ---- Solver-specific: vartype passthrough tests ----


@pytest.mark.parametrize(
    'vtype', [GRB.CONTINUOUS, GRB.BINARY, GRB.INTEGER, GRB.SEMICONT, GRB.SEMIINT]
)
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_pass(mdl, indexset, vtype):
    v = addVars(mdl, indexset, vtype=vtype)
    assert v.VType is vtype
