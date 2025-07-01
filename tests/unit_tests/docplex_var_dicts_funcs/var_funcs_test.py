# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Add variable functionality."""

import pytest

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND
from opti_extensions.docplex import add_variable, add_variables


@pytest.mark.parametrize(
    'var_type, kwargs, docpx_method',
    [
        ('continuous', {}, 'continuous_var'),
        ('integer', {}, 'integer_var'),
        ('binary', {}, 'binary_var'),
        ('semicontinuous', {'lb': 1}, 'semicontinuous_var'),
        ('semiinteger', {'lb': 1}, 'semiinteger_var'),
        ('C', {}, 'continuous_var'),
        ('I', {}, 'integer_var'),
        ('B', {}, 'binary_var'),
        ('SC', {'lb': 1}, 'semicontinuous_var'),
        ('SI', {'lb': 1}, 'semiinteger_var'),
    ],
)
def test_add_variable_pass(mdl, mdl_2, var_type, kwargs, docpx_method):
    one = add_variable(mdl, var_type, name='test', **kwargs)
    two = getattr(mdl_2, docpx_method)(name='test', **kwargs)

    assert repr(one) == repr(two)


@pytest.mark.parametrize('mdl', ['abc', 123, ('A', 'B')])
@pytest.mark.parametrize(
    'var_type, kwargs',
    [
        ('continuous', {}),
        ('integer', {}),
        ('binary', {}),
        ('semicontinuous', {'lb': 1}),
        ('semiinteger', {'lb': 1}),
        ('C', {}),
        ('I', {}),
        ('B', {}),
        ('SC', {'lb': 1}),
        ('SI', {'lb': 1}),
    ],
)
def test_add_variable_mdl_typerr(mdl, var_type, kwargs):
    with pytest.raises(TypeError):
        add_variable(mdl, var_type, **kwargs)


@pytest.mark.parametrize('var_type', [123, (1, 2), {'SC'}])
def test_add_variable_vartype_typerr(mdl, var_type):
    with pytest.raises(TypeError):
        add_variable(mdl, var_type)


@pytest.mark.parametrize('var_type', ['semi-continuous', 'semi-integer', 'abc'])
def test_add_variable_vartype_valerr(mdl, var_type):
    with pytest.raises(ValueError):
        add_variable(mdl, var_type)


@pytest.mark.parametrize('indexset', [IndexSet1D(), IndexSetND()])
def test_add_variables_indexset_valerr(mdl, indexset):
    with pytest.raises(ValueError):
        add_variables(mdl, indexset, 'C')


@pytest.mark.parametrize('var_type', ['semicontinuous', 'semiinteger', 'SC', 'SI'])
def test_add_variable_semix_valerr(mdl, var_type):
    with pytest.raises(ValueError):
        add_variable(mdl, var_type)


indexset_cases = [
    IndexSet1D(['A', 'B', 'C']),
    IndexSet1D(range(3)),
    IndexSetND(['A', 'B', 'C'], range(3)),
    IndexSetND(range(3), range(3)),
]


@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize(
    'var_type, kwargs, docpx_method',
    [
        ('continuous', {}, 'continuous_var_dict'),
        ('integer', {}, 'integer_var_dict'),
        ('binary', {}, 'binary_var_dict'),
        ('semicontinuous', {'lb': 1}, 'semicontinuous_var_dict'),
        ('semiinteger', {'lb': 1}, 'semiinteger_var_dict'),
        ('C', {}, 'continuous_var_dict'),
        ('I', {}, 'integer_var_dict'),
        ('B', {}, 'binary_var_dict'),
        ('SC', {'lb': 1}, 'semicontinuous_var_dict'),
        ('SI', {'lb': 1}, 'semiinteger_var_dict'),
    ],
)
def test_add_variables_pass(mdl, mdl_2, indexset, var_type, kwargs, docpx_method):
    one = add_variables(mdl, indexset, var_type, name='test', **kwargs)
    two = getattr(mdl_2, docpx_method)(indexset, name='test', **kwargs)

    assert repr(dict(one)) == repr(two)


@pytest.mark.parametrize('mdl', ['abc', 123, ('A', 'B')])
@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize(
    'var_type, kwargs',
    [
        ('continuous', {}),
        ('integer', {}),
        ('binary', {}),
        ('semicontinuous', {'lb': 1}),
        ('semiinteger', {'lb': 1}),
        ('C', {}),
        ('I', {}),
        ('B', {}),
        ('SC', {'lb': 1}),
        ('SI', {'lb': 1}),
    ],
)
def test_add_variables_mdl_typerr(mdl, indexset, var_type, kwargs):
    with pytest.raises(TypeError):
        add_variables(mdl, indexset, var_type, **kwargs)


@pytest.mark.parametrize(
    'indexset',
    [
        (1, 2, 3),
        [1, 2, 3],
        [('A', 'B'), ('C', 'D')],
        [('A', '1'), ('C', '2')],
    ],
)
@pytest.mark.parametrize(
    'var_type, kwargs',
    [
        ('continuous', {}),
        ('integer', {}),
        ('binary', {}),
        ('semicontinuous', {'lb': 1}),
        ('semiinteger', {'lb': 1}),
        ('C', {}),
        ('I', {}),
        ('B', {}),
        ('SC', {'lb': 1}),
        ('SI', {'lb': 1}),
    ],
)
def test_add_variables_idxset_typerr(mdl, indexset, var_type, kwargs):
    with pytest.raises(TypeError):
        add_variables(mdl, indexset, var_type, **kwargs)


@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize('var_type', [123, (1, 2), {'SC'}])
def test_add_variables_vartype_typerr(mdl, indexset, var_type):
    with pytest.raises(TypeError):
        add_variables(mdl, indexset, var_type)


@pytest.mark.parametrize('indexset', indexset_cases)
@pytest.mark.parametrize('var_type', ['semi-continuous', 'semi-integer', 'abc'])
def test_add_variables_vartype_valerr(mdl, indexset, var_type):
    with pytest.raises(ValueError):
        add_variables(mdl, indexset, var_type)


@pytest.mark.parametrize('var_type', ['semicontinuous', 'semiinteger', 'SC', 'SI'])
@pytest.mark.parametrize(
    'indexset, lb',
    [
        (IndexSet1D(['A', 'B', 'C']), None),
        (IndexSetND(range(3), range(3)), None),
        (IndexSet1D(['A', 'B', 'C']), {'XYZ': 1}.get),
        (IndexSetND(range(3), range(3)), {(9, 9): 1}.get),
        (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'XYZ': 1})),
        (IndexSetND(range(3), range(3)), ParamDictND({('ABC', 'XYZ'): 1})),
    ],
)
def test_add_variables_semix_valerr(mdl, indexset, var_type, lb):
    with pytest.raises(ValueError):
        add_variables(mdl, indexset, var_type, lb=lb)


@pytest.mark.parametrize(
    'indexset, bound',
    [
        (IndexSet1D(['A', 'B', 'C']), None),
        (IndexSet1D(['A', 'B', 'C']), 1),
        (IndexSet1D(['A', 'B', 'C']), 1.0),
        (IndexSet1D(['A', 'B', 'C']), [1, 1, 1]),
        (IndexSet1D(['A', 'B', 'C']), [1, 1, None]),
        (IndexSet1D(['A', 'B', 'C']), [1.0, 1.0, 1.0]),
        (IndexSet1D(['A', 'B', 'C']), [1.0, 1.0, None]),
        (IndexSet1D(['A', 'B', 'C']), [1, 1.0, None]),
        (IndexSet1D(['A', 'B', 'C']), {'A': 1, 'B': 1, 'C': 1}.get),
        (IndexSet1D(['A', 'B', 'C']), {'A': 1, 'B': 1}.get),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_add_variables_basic_bound(mdl, indexset, bound, bound_type):
    bound_kwargs = {bound_type: bound}
    one = add_variables(mdl, indexset, 'C', **bound_kwargs)
    two = mdl.continuous_var_dict(indexset, **bound_kwargs)

    assert repr(dict(one)) == repr(two)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDict1D({'A': 1, 'B': 1, 'C': 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_add_variables_paramdict_bound(mdl, indexset, paramdict, bound_type):
    bound_kwargs_1 = {bound_type: paramdict}
    one = add_variables(mdl, indexset, 'C', **bound_kwargs_1)

    bound_kwargs_2 = {bound_type: paramdict.get}
    two = mdl.continuous_var_dict(indexset, **bound_kwargs_2)

    assert repr(dict(one)) == repr(two)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSet1D(['A', 'B', 'C']), ParamDictND({('A', 0): 1, ('B', 0): 1, ('C', 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDict1D({0: 1, 1: 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_add_variables_paramdict_typerr(mdl, indexset, paramdict, bound_type):
    with pytest.raises(TypeError):
        bound_kwargs_1 = {bound_type: paramdict}
        add_variables(mdl, indexset, 'C', **bound_kwargs_1)


@pytest.mark.parametrize(
    'indexset, paramdict',
    [
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0): 1, (0, 1, 0): 1})),
        (IndexSetND(range(2), range(2)), ParamDictND({(0, 0, 0, 0): 1, (0, 1, 0, 0): 1})),
    ],
)
@pytest.mark.parametrize('bound_type', ['lb', 'ub'])
def test_add_variables_paramdict_difflen_valerr(mdl, indexset, paramdict, bound_type):
    with pytest.raises(ValueError):
        bound_kwargs_1 = {bound_type: paramdict}
        add_variables(mdl, indexset, 'C', **bound_kwargs_1)
