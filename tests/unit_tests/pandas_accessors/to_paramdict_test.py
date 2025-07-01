# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Accessors to cast pandas Series/DataFrame into ParamDict."""

import pandas as pd
import pytest

from opti_extensions import ParamDict1D, ParamDictND


@pytest.mark.parametrize(
    'input, expected',
    [
        (pd.Series(range(3)), ParamDict1D({0: 0, 1: 1, 2: 2})),
        (pd.Series(range(3), index=('A', 'B', 'C')), ParamDict1D({'A': 0, 'B': 1, 'C': 2})),
        (pd.Series([0.0, 1.0], index=('A', 'B')), ParamDict1D({'A': 0.0, 'B': 1.0})),
        (
            pd.DataFrame({'idx': ('A', 'B', 'C'), 'col': (0, 1, 2)}).set_index('idx'),
            ParamDict1D({'A': 0, 'B': 1, 'C': 2}),
        ),
        (
            pd.DataFrame({'idx': ('A', 'B', 'C'), 'col': (0.0, 1.0, 2.0)}).set_index('idx'),
            ParamDict1D({'A': 0.0, 'B': 1.0, 'C': 2.0}),
        ),
        (
            pd.Series(range(3), index=(('A', 'X'), ('B', 'Y'), ('C', 'Z'))),
            ParamDictND({('A', 'X'): 0, ('B', 'Y'): 1, ('C', 'Z'): 2}),
        ),
        (
            pd.DataFrame({'idx1': ('A', 'B'), 'idx2': ('X', 'Y'), 'col': (0.0, 1.0)}).set_index(
                ['idx1', 'idx2']
            ),
            ParamDictND({('A', 'X'): 0.0, ('B', 'Y'): 1.0}),
        ),
    ],
)
def test_to_paramdict_pass(input, expected):
    assert input.opti.to_paramdict() == expected


@pytest.mark.parametrize(
    'input, valuename',
    [
        (pd.Series(range(3)), None),
        (pd.Series(range(3), name='VAL'), 'VAL'),
        (pd.DataFrame({'idx': ('A', 'B', 'C'), 'col': (0, 1, 2)}).set_index('idx'), 'col'),
        (
            pd.DataFrame({'idx1': ('A', 'B'), 'idx2': ('X', 'Y'), 'col': (0.0, 1.0)}).set_index(
                ['idx1', 'idx2']
            ),
            'col',
        ),
    ],
)
def test_to_paramdict_valuename(input, valuename):
    param = input.opti.to_paramdict()
    assert param.value_name == valuename


@pytest.mark.parametrize(
    'input, keyname, attrname',
    [
        (pd.Series(range(3)), None, 'key_name'),
        (pd.Series(range(3)).to_frame(name='col'), None, 'key_name'),
        (
            pd.DataFrame({'idx': ('A', 'B', 'C'), 'col': (0, 1, 2)}).set_index('idx')['col'],
            'idx',
            'key_name',
        ),
        (
            pd.DataFrame({'idx': ('A', 'B', 'C'), 'col': (0, 1, 2)}).set_index('idx'),
            'idx',
            'key_name',
        ),
        (pd.Series(range(3), index=(('A', 'X'), ('B', 'Y'), ('C', 'Z'))), None, 'key_names'),
        (
            pd.DataFrame({'idx1': ('A', 'B'), 'idx2': ('X', 'Y'), 'col': (0.0, 1.0)}).set_index(
                ['idx1', 'idx2']
            ),
            ['idx1', 'idx2'],
            'key_names',
        ),
    ],
)
def test_to_paramdict_keyname(input, keyname, attrname):
    param = input.opti.to_paramdict()
    assert getattr(param, attrname) == keyname


@pytest.mark.parametrize('input', [pd.Series(name='EMP'), pd.DataFrame(columns=['EMP'])])
def test_to_paramdict_emp_valerr(input):
    with pytest.raises(ValueError):
        input.opti.to_paramdict()


@pytest.mark.parametrize(
    'input',
    [
        pd.DataFrame({'col1': (1, 2), 'col2': (1.0, 2.0)}),
        pd.DataFrame({'idx': ('A', 'B'), 'col1': (1, 2), 'col2': (1.0, 2.0)}).set_index('idx'),
    ],
)
def test_to_paramdict_multiple_cols_valerr(input):
    with pytest.raises(ValueError):
        input.opti.to_paramdict()


@pytest.mark.parametrize(
    'input',
    [
        pd.DataFrame({'idx': ('A', 'B', 'B'), 'col': (1, 2, 3)}).set_index('idx'),
        pd.DataFrame({'idx': ('A', 'B', 'B'), 'col': (1, 2, 3)}).set_index('idx')['col'],
    ],
)
def test_to_paramdict_duplicate_idx_valerr(input):
    with pytest.raises(ValueError):
        input.opti.to_paramdict()


@pytest.mark.parametrize(
    'input',
    [
        pd.DataFrame({'idx': (['A', 'B'], 'C'), 'col': (1, 2)}).set_index('idx'),
        pd.DataFrame({'idx': (['A', 'B'], 'C'), 'col': (1, 2)}).set_index('idx')['col'],
        pd.DataFrame({'idx': (('A', 'B'), 'C'), 'col': (1, 2)}).set_index('idx'),
        pd.DataFrame({'idx': (('A', 'B'), 'C'), 'col': (1, 2)}).set_index('idx')['col'],
        pd.DataFrame({'idx': ({'A', 'B'}, 'C'), 'col': (1, 2)}).set_index('idx'),
        pd.DataFrame({'idx': ({'A', 'B'}, 'C'), 'col': (1, 2)}).set_index('idx')['col'],
    ],
)
def test_to_paramdict_nonscal_typerr(input):
    with pytest.raises(TypeError):
        input.opti.to_paramdict()
