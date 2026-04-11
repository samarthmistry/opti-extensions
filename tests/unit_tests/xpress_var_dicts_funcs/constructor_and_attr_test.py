# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict1D & VarDictND constructor and attributes."""

import pytest
import xpress as xp

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.xpress import addVariables

# Import all shared tests
from tests.unit_tests._shared_constructor_and_attr_tests import *  # noqa: F401, F403

# ---- Solver-specific: valname update pass ----


@pytest.mark.parametrize('input, name', [('DEF', 'V1'), ('Z', 'V2')])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_update_pass(prob, indexset, input, name):
    v = addVariables(prob, indexset, vartype=xp.continuous, name=name)
    v.value_name = input
    assert v.value_name == input


# ---- Solver-specific: vartype passthrough tests ----


@pytest.mark.parametrize(
    'vartype', [xp.continuous, xp.binary, xp.integer, xp.semicontinuous, xp.semiinteger]
)
@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_pass(prob, indexset, vartype):
    v = addVariables(prob, indexset, name='', vartype=vartype)
    assert v.vartype is vartype
