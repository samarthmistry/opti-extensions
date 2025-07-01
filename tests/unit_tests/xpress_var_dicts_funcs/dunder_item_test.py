# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Dunder setitem & delitem of VarDict1D & VarDictND."""

import pytest
import xpress as xp

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.xpress import addVariables

test_cases = [(IndexSet1D(['A', 'B', 'C']), 'A'), (IndexSetND(range(2), range(2)), (0, 0))]


@pytest.mark.parametrize('indexset, key', test_cases)
def test_vardict_setitem_err(prob, indexset, key):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')
    with pytest.raises(AttributeError):
        v[key] = 1


@pytest.mark.parametrize('indexset, key', test_cases)
def test_vardict_delitem_err(prob, indexset, key):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')
    with pytest.raises(AttributeError):
        del v[key]
