# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Shared test logic for VarDict1D & VarDictND constructor and attributes.

Solver-specific conftest files provide the following fixtures:
- ``model``: The solver model instance
- ``add_vars_fn``: The function to create variables (e.g., ``add_variables``, ``addVars``)
- ``add_vars_kwargs``: Default kwargs for creating variables (vartype + name)
- ``VarDict1D_cls``, ``VarDictND_cls``: The VarDict classes
- ``create_kwargs``: Kwargs used with ``_create()`` (solver-specific vartype kwarg)
- ``model_attr_name``: Attribute name to access model on VarDict
- ``vartype_attr_name``: Attribute name to access vartype on VarDict
- ``all_vartypes``: List of (vartype_value, add_vars_extra_kwargs) for parameterization
"""

from collections import abc

import pytest

from opti_extensions import IndexSet1D, IndexSetND

# ---- Constructor error tests ----


CLS_INDEXSET_PAIRS = [
    ['1D', IndexSet1D(['A', 'B', 'C'])],
    ['ND', IndexSetND(range(2), range(2))],
]


@pytest.mark.parametrize('cls_key, indexset', CLS_INDEXSET_PAIRS)
def test_vardict_init_typerr0(
    model, add_vars_fn, add_vars_kwargs, vardict_classes, create_kwargs, cls_key, indexset
):
    """Direct construction (not via _create) should raise TypeError."""
    cls = vardict_classes[cls_key]
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(TypeError):
        cls(v, indexset, **create_kwargs)


@pytest.mark.parametrize('cls_key, indexset', CLS_INDEXSET_PAIRS)
@pytest.mark.parametrize('vardict', [0, int, [1, 2], 'A'])
def test_vardict_init_typerr1(model, vardict_classes, create_kwargs, cls_key, indexset, vardict):
    cls = vardict_classes[cls_key]
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, **create_kwargs)


@pytest.mark.parametrize('cls_key, indexset', CLS_INDEXSET_PAIRS)
def test_vardict_init_valerr1(model, vardict_classes, create_kwargs, cls_key, indexset):
    cls = vardict_classes[cls_key]
    with pytest.raises(ValueError):
        cls._create({}, indexset, **create_kwargs)


@pytest.mark.parametrize('cls_key, indexset', CLS_INDEXSET_PAIRS)
@pytest.mark.parametrize('vardict', [{'A': 0, 'B': 1}, {1: [1, 2], 2: [2, 3]}])
def test_vardict_init_typerr2(model, vardict_classes, create_kwargs, cls_key, indexset, vardict):
    cls = vardict_classes[cls_key]
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, **create_kwargs)


@pytest.mark.parametrize(
    'cls_key, indexset, incorrect',
    [
        ['1D', IndexSet1D(['A', 'B', 'C']), IndexSet1D(['A', 'B'])],
        ['ND', IndexSetND(range(2), range(2)), IndexSetND(range(1), range(2))],
    ],
)
def test_vardict_init_valerr2(
    model,
    add_vars_fn,
    add_vars_kwargs,
    vardict_classes,
    create_kwargs,
    cls_key,
    indexset,
    incorrect,
):
    cls = vardict_classes[cls_key]
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(ValueError):
        cls._create(v, incorrect, **create_kwargs)


# ---- key_name tests (VarDict1D) ----


@pytest.mark.parametrize('name', [None, 'KEY'])
def test_vardict1d_init_keyname_pass(model, add_vars_fn, add_vars_kwargs, name):
    indexset = IndexSet1D(['A', 'B', 'C'], name=name)
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    assert v.key_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_vardict1d_init_keyname_update_pass(model, add_vars_fn, add_vars_kwargs, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    v.key_name = input
    assert v.key_name == input


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict1d_init_keyname_update_typeerr(model, add_vars_fn, add_vars_kwargs, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(TypeError):
        v.key_name = input


# ---- key_names tests (VarDictND) ----


@pytest.mark.parametrize(
    'input, expected',
    [
        [None, None],
        [('KEY1', 'KEY2'), ['KEY1', 'KEY2']],
        [['KEY1', 'KEY2'], ['KEY1', 'KEY2']],
        [('KEY1', 'KEY2', 'KEY3'), ['KEY1', 'KEY2', 'KEY3']],
        # ^ valid because ParamDictND doesn't enforce the names to conform with len of keys
    ],
)
def test_vardictNd_init_keynames_pass(model, add_vars_fn, add_vars_kwargs, input, expected):
    indexset = IndexSetND(range(2), range(2), names=input)
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    assert v.key_names == expected


@pytest.mark.parametrize('input', [('C', 'D'), ['A', 'B', 'C']])
def test_vardictNd_init_keynames_update_pass(model, add_vars_fn, add_vars_kwargs, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    v.key_names = input
    assert v.key_names == list(input)


@pytest.mark.parametrize('input', ['CD', 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_vardictNd_init_keynames_update_typeerr(model, add_vars_fn, add_vars_kwargs, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(TypeError):
        v.key_names = input


# ---- value_name tests ----


@pytest.mark.parametrize('name', [None, 'VAL'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_pass(model, add_vars_fn, add_vars_kwargs_with_name, indexset, name):
    kwargs = add_vars_kwargs_with_name(name)
    v = add_vars_fn(model, indexset, **kwargs)
    assert v.value_name == name


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict_init_valname_update_typeerr(model, add_vars_fn, add_vars_kwargs, indexset, input):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(TypeError):
        v.value_name = input


# ---- model attribute tests ----


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_model_pass(model, add_vars_fn, add_vars_kwargs, model_attr_name, indexset):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    assert getattr(v, model_attr_name) is model


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_model_attrerr(model, add_vars_fn, add_vars_kwargs, model_attr_name, indexset):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(AttributeError):
        setattr(v, model_attr_name, 1)


# ---- vartype attribute tests ----


@pytest.mark.parametrize('indexset', [IndexSet1D(range(2)), IndexSetND(range(2), range(2))])
def test_vardict_attr_vartype_attrerr(
    model, add_vars_fn, add_vars_kwargs, vartype_attr_name, indexset
):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    with pytest.raises(AttributeError):
        setattr(v, vartype_attr_name, 1)


# ---- isinstance tests ----


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_isinstance_dict(model, add_vars_fn, add_vars_kwargs, indexset):
    v = add_vars_fn(model, indexset, **add_vars_kwargs)
    assert isinstance(v, dict)
    assert isinstance(v, abc.MutableMapping)
