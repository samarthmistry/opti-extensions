# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Shared generic error-handling tests for add_variables / addVars."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND

# Shared cases used internally for testing generic wrapper boundaries
SHARED_INDEXSET_CASES = [
    IndexSet1D(['A', 'B', 'C']),
    IndexSet1D(range(3)),
    IndexSetND(['A', 'B', 'C'], range(3)),
    IndexSetND(range(3), range(3)),
]


@pytest.mark.parametrize('indexset', [IndexSet1D(), IndexSetND()])
def test_add_vars_indexset_empty_valerr(model, add_vars_fn, add_vars_kwargs, indexset):
    with pytest.raises(ValueError):
        add_vars_fn(model, indexset, **add_vars_kwargs)


@pytest.mark.parametrize('mdl_wrong', ['abc', 123, ('A', 'B')])
@pytest.mark.parametrize('indexset', SHARED_INDEXSET_CASES)
def test_add_vars_mdl_typerr(add_vars_fn, add_vars_kwargs, mdl_wrong, indexset):
    with pytest.raises(TypeError):
        add_vars_fn(mdl_wrong, indexset, **add_vars_kwargs)


@pytest.mark.parametrize(
    'indexset_wrong',
    [
        (1, 2, 3),
        [1, 2, 3],
        [('A', 'B'), ('C', 'D')],
        [('A', '1'), ('C', '2')],
    ],
)
def test_add_vars_idxset_typerr(model, add_vars_fn, add_vars_kwargs, indexset_wrong):
    with pytest.raises(TypeError):
        add_vars_fn(model, indexset_wrong, **add_vars_kwargs)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDictND({('A', 0): 1, ('B', 0): 1, ('C', 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDict1D({0: 1, 1: 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_add_vars_paramdict_typerr(
    model, add_vars_fn, add_vars_kwargs, indexset, paramdict, bound_type
):
    with pytest.raises(TypeError):
        bound_kwargs = {bound_type: paramdict}
        add_vars_fn(model, indexset, **add_vars_kwargs, **bound_kwargs)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0): 1, (0, 1, 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0, 0): 1, (0, 1, 0, 0): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_add_vars_paramdict_difflen_valerr(
    model, add_vars_fn, add_vars_kwargs, indexset, paramdict, bound_type
):
    with pytest.raises(ValueError):
        bound_kwargs = {bound_type: paramdict}
        add_vars_fn(model, indexset, **add_vars_kwargs, **bound_kwargs)
