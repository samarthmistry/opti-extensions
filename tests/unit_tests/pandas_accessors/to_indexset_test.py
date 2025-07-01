# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Accessors to cast pandas Series/DataFrame/Index into IndexSet."""

import pandas as pd
import pytest

from opti_extensions import IndexSet1D, IndexSetND

from ..helper_indexset import assert_sets_same


@pytest.mark.parametrize(
    'input, expected',
    [
        (pd.Series(range(3)), IndexSet1D(range(3))),
        (pd.Series(range(3), index=('A', 'B', 'C')), IndexSet1D(range(3))),
        (pd.Series(range(3), index=(('A', 'X'), ('B', 'Y'), ('C', 'Z'))), IndexSet1D(range(3))),
        (pd.DataFrame({'A': (0, 1, 2)}), IndexSet1D(range(3))),
        (
            pd.DataFrame({'A': (0, 1, 2), 'B': ('X', 'Y', 'Z')}),
            IndexSetND([(0, 'X'), (1, 'Y'), (2, 'Z')]),
        ),
        (pd.Series(range(3)).index, IndexSet1D(range(3))),
        (pd.Series(range(3), index=('A', 'B', 'C')).index, IndexSet1D(['A', 'B', 'C'])),
        (
            pd.Series(range(3), index=(('A', 'X'), ('B', 'Y'), ('C', 'Z'))).index,
            IndexSetND([('A', 'X'), ('B', 'Y'), ('C', 'Z')]),
        ),
        (pd.DataFrame({'A': (0, 1, 2)}).index, IndexSet1D(range(3))),
        (pd.DataFrame({'A': (0, 1, 2)}).columns, IndexSet1D(['A'])),
        (
            pd.DataFrame({'A': (0, 1, 2), 'B': ('X', 'Y', 'Z')}).columns,
            IndexSet1D(['A', 'B']),
        ),
        (
            pd.DataFrame([range(3)], columns=(('A', 'X'), ('B', 'Y'), ('C', 'Z'))).columns,
            IndexSetND([('A', 'X'), ('B', 'Y'), ('C', 'Z')]),
        ),
    ],
)
def test_to_indexset_pass(input, expected):
    assert_sets_same(input.opti.to_indexset(), expected)


@pytest.mark.parametrize(
    'input, name, attrname',
    [
        (pd.Series(range(3)), None, 'name'),
        (pd.Series(range(3), name='ABC'), 'ABC', 'name'),
        (pd.DataFrame({'ABC': (0, 1, 2)}), 'ABC', 'name'),
        (pd.DataFrame({'A': (0, 1, 2), 'B': ('X', 'Y', 'Z')}), ['A', 'B'], 'names'),
        (pd.Series(range(3), name='VAL').rename_axis(['IDX'], axis=0).index, 'IDX', 'name'),
        (pd.DataFrame({'A': (0, 1, 2)}).index, None, 'name'),
        (pd.DataFrame({'A': (0, 1, 2)}).rename_axis(['ROW'], axis=0).index, 'ROW', 'name'),
        (pd.DataFrame({'A': (0, 1, 2)}).columns, None, 'name'),
        (pd.DataFrame({'A': (0, 1, 2)}).rename_axis(['COL'], axis=1).columns, 'COL', 'name'),
        (
            (
                pd.DataFrame([range(2)], columns=(('A', 'X'), ('B', 'Y')))
                .rename_axis(['L1', 'L2'], axis=1)
                .columns
            ),
            ['L1', 'L2'],
            'names',
        ),
    ],
)
def test_to_indexset_name(input, name, attrname):
    iset = input.opti.to_indexset()
    assert getattr(iset, attrname) == name


@pytest.mark.parametrize(
    'input',
    [
        pd.Series(name='EMP'),
        pd.DataFrame(columns=['EMP']),
        pd.DataFrame(columns=['EMP1', 'EMP2']),
        pd.Series(name='EMP').index,
        pd.DataFrame(columns=['EMP']).index,
        pd.DataFrame().columns,
    ],
)
def test_to_indexset_emp_valerr(input):
    with pytest.raises(ValueError):
        input.opti.to_indexset()


@pytest.mark.parametrize(
    'input',
    [
        pd.Series([1, 1, 1], name='DUP'),
        pd.DataFrame([1, 1, 1], columns=['DUP']),
        pd.DataFrame({'A': (0, 1, 1), 'B': (0, 1, 1)}),
        pd.DataFrame({'A': (0, 1, 1), 'B': (0, 'A', 'A')}),
        pd.Series(range(3), name='A', index=[0, 0, 0]).index,
        pd.DataFrame(range(3), columns=['A'], index=[0, 0, 0]).index,
        pd.DataFrame(columns=['A', 'A', 'B']).columns,
        pd.DataFrame(range(2), columns=['A'], index=((0, 0), (0, 0))).index,
        pd.DataFrame([range(2)], columns=(('A', 'B'), ('A', 'B'))).columns,
    ],
)
def test_to_indexset_duplicate_valerr(input):
    with pytest.raises(ValueError):
        input.opti.to_indexset()


@pytest.mark.parametrize(
    'input',
    [
        pd.Series([(0, 0), 1, 2], name='X'),
        pd.Series([[0, 0], 1, 2], name='X'),
        pd.Series([{0}, 1, 2], name='X'),
        pd.DataFrame({'A': ((0, 0), 1), 'B': (0, 'A')}),
        pd.DataFrame({'A': ([0, 0], 'B'), 'B': (0, 'A')}),
        pd.DataFrame({'A': ({0}, 'B'), 'B': (0, 'A')}),
        pd.Series(range(2), index=[(0, 0), (0, 1)]).index,
        pd.DataFrame(range(2), index=[(0, 0), (0, 1)]).index,
        pd.DataFrame([range(2)], columns=[(0, 0), (0, 1)]).columns,
    ],
)
def test_to_indexset_nonscal_typerr(input):
    with pytest.raises(TypeError):
        input.opti.to_indexset()
