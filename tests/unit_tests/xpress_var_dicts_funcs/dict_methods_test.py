# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Other methods of VarDict1D & VarDictND."""

import pytest
import xpress as xp

from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.xpress import addVariables


@pytest.mark.parametrize(
    'method', ['clear', 'copy', 'pop', 'popitem', 'setdefault', 'update', 'fromkeys']
)
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_attrerr(prob, indexset, method):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')
    with pytest.raises(AttributeError):
        getattr(v, method)()


@pytest.mark.parametrize(
    'indexset, key, default, present',
    [
        (IndexSet1D(['A', 'B', 'C']), 'A', None, True),
        (IndexSet1D(['A', 'B', 'C']), 'A', -1, True),
        (IndexSet1D(['A', 'B', 'C']), 'Z', None, False),
        (IndexSet1D(['A', 'B', 'C']), 'Z', -1, False),
        (IndexSetND(range(2), range(2)), (0, 0), None, True),
        (IndexSetND(range(2), range(2)), (0, 0), -1, True),
        (IndexSetND(range(2), range(2)), (0, 9), None, False),
        (IndexSetND(range(2), range(2)), (0, 9), -1, False),
    ],
)
def test_vardict_get_pass(prob, indexset, key, default, present):
    v = addVariables(prob, indexset, vartype=xp.continuous, name='')
    value = v.get(key, default)
    if present:
        assert value is v[key]
    else:
        assert value == default
