# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Functions to add variable(s) to a highspy model."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Literal, overload

from highspy import Highs, HighsVarType, kHighsInf
from highspy.highs import highs_var

from .._index_sets import Elem1DT, ElemNDT, IndexSet1D, IndexSetND
from .._param_dicts import ParamDict1D, ParamDictND, ParamT
from ._var_dicts import VarDict1D, VarDictND


def _paramdictNd_as_attr(
    indexset: IndexSetND[ElemNDT],
    attr: ParamDictND[ElemNDT, ParamT],
    attr_type: Literal['lb', 'ub', 'obj'],
) -> ParamDictND[ElemNDT, ParamT]:
    """Use ParamDictND as highspy variable attribute.

    Parameters
    ----------
    indexset : IndexSetND
        Index-set for defining the variables.
    attr : ParamDictND
        ParamDict to be used as the attribute.
    attr_type : str
        Attribute type, ``'lb'`` or ``'ub'`` or ``'obj'``.

    Returns
    -------
    ParamDictND
        ParamDictND that can be used as highspy variable attribute for the `Highs.addVariables`
        method.

    Raises
    ------
    ValueError
        ParamDict keys and indexset have tuple elements of different lengths.
    """
    if (not attr) or (attr and attr._indexset._tuplelen == indexset._tuplelen):
        return attr
    else:
        raise ValueError(f'{attr_type} keys and indexset have tuple elements of different lengths')


def _preprocess_attr(
    indexset: IndexSet1D[Elem1DT] | IndexSetND[ElemNDT],
    attr: int
    | float
    | Sequence[int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | ParamDictND[ElemNDT, ParamT]
    | Mapping[Elem1DT, int | float]
    | Mapping[ElemNDT, int | float],
    attr_type: Literal['lb', 'ub', 'obj'],
) -> (
    int
    | float
    | Sequence[int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | ParamDictND[ElemNDT, ParamT]
    | Mapping[Elem1DT, int | float]
    | Mapping[ElemNDT, int | float]
):
    """Preprocess highspy variable attribute.

    Parameters
    ----------
    indexset : IndexSet1D or IndexSetND
        Index-set for defining the variables.
    attr : int or float or Sequence or Mapping or ParamDict
        Variable attribute.
    attr_type : str
        Attribute type, ``'lb'`` or ``'ub'`` or ``'obj'``.

    Returns
    -------
    int or float or Sequence or Mapping or ParamDict
        The highspy variable attribute for the `Highs.addVariables` method.

    Raises
    ------
    ValueError
        ParamDict keys and indexset have tuple elements of different lengths.
    TypeError
        If paramdict is ParamDictND and indexset is IndexSet1D, or vice versa.
    """
    # Validate if ParamDict is used as variable attribute
    if isinstance(attr, ParamDict1D):
        if isinstance(indexset, IndexSet1D):
            return attr
        else:
            raise TypeError(f'`{attr_type}` should be ParamDictND when indexset is IndexSetND')
    elif isinstance(attr, ParamDictND):
        if isinstance(indexset, IndexSetND):
            return _paramdictNd_as_attr(indexset, attr, attr_type)
        else:
            raise TypeError(f'`{attr_type}` should be ParamDict1D when indexset is IndexSet1D')
    # Let highspy handle everything else, so return as is
    else:
        return attr


@overload
def addVariables(  # numpydoc ignore=GL08
    model: Highs,
    indexset: IndexSet1D[Elem1DT],
    lb: int
    | float
    | Sequence[int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | Mapping[Elem1DT, int | float] = ...,
    ub: int
    | float
    | Sequence[int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | Mapping[Elem1DT, int | float] = ...,
    obj: int
    | float
    | Sequence[int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | Mapping[Elem1DT, int | float] = ...,
    type: HighsVarType = ...,
    name: Sequence[str] | None = ...,
    name_prefix: str | None = ...,
) -> VarDict1D[Elem1DT, highs_var]: ...


@overload
def addVariables(  # numpydoc ignore=GL08
    model: Highs,
    indexset: IndexSetND[ElemNDT],
    lb: int
    | float
    | Sequence[int | float]
    | ParamDictND[ElemNDT, ParamT]
    | Mapping[ElemNDT, int | float] = ...,
    ub: int
    | float
    | Sequence[int | float]
    | ParamDictND[ElemNDT, ParamT]
    | Mapping[ElemNDT, int | float] = ...,
    obj: int
    | float
    | Sequence[int | float]
    | ParamDictND[ElemNDT, ParamT]
    | Mapping[ElemNDT, int | float] = ...,
    type: HighsVarType = ...,
    name: Sequence[str] | None = ...,
    name_prefix: str | None = ...,
) -> VarDictND[ElemNDT, highs_var]: ...


def addVariables(
    model: Highs,
    indexset: IndexSet1D[Elem1DT] | IndexSetND[ElemNDT],
    lb: int
    | float
    | Sequence[int | float]
    | Mapping[Elem1DT, int | float]
    | Mapping[ElemNDT, int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | ParamDictND[ElemNDT, ParamT] = 0.0,
    ub: int
    | float
    | Sequence[int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | ParamDictND[ElemNDT, ParamT]
    | Mapping[Elem1DT, int | float]
    | Mapping[ElemNDT, int | float] = kHighsInf,
    obj: int
    | float
    | Sequence[int | float]
    | ParamDict1D[Elem1DT, ParamT]
    | ParamDictND[ElemNDT, ParamT]
    | Mapping[Elem1DT, int | float]
    | Mapping[ElemNDT, int | float] = 0.0,
    type: HighsVarType = HighsVarType.kContinuous,
    name: Sequence[str] | None = None,
    name_prefix: str | None = None,
) -> VarDict1D[Elem1DT, highs_var] | VarDictND[ElemNDT, highs_var]:
    """Create and add multiple variables (corresponding to an index-set) to the highspy model.

    This function extends highspy's `Highs.addVariables` method by wrapping it and returning
    VarDict1D/VarDictND data structures - that can efficiently sum subsets of variables with
    a user-friendly syntax based on wildcard patterns. The ``out_array`` argument is not supported.

    Parameters
    ----------
    model : highspy.Highs
        The highspy model.
    indexset : IndexSet1D or IndexSetND
        Index-set for defining the variables. The ``name``/``names`` attribute of
        IndexSet1D/IndexSetND will be set as the ``key_name``/``key_names`` attribute of
        VarDict1D/VarDictND.
    lb : int or float or sequence or dict or ParamDict, optional
        Lower bound, in one of the following forms:

        * A number - if all variables share the same lower bound.
        * A sequence of numbers - one for each variable.
        * A dict/ParamDict - with keys following the same structute as the index-set elements and
          values representing the lower bound; will fallback to the default for index-set elements
          not found in dict/ParamDict keys.

        Default is ``0.0``.
    ub : int or float or sequence or dict or ParamDict, optional
        Upper bound, in one of the following forms:

        * A number - if all variables share the same upper bound.
        * A sequence of numbers - one for each variable.
        * A dict/ParamDict - with keys following the same structute as the index-set elements and
          values representing the upper bound; will fallback to the default for index-set elements
          not found in dict/ParamDict keys.

        Default is ``infinity`` for other types.
    obj : int or float or sequence or dict or ParamDict, optional
        Objective coefficient, in one of the following forms:

        * A number - if all variables share the same objective coefficient.
        * A sequence of numbers - one for each variable.
        * A dict/ParamDict - with keys following the same structute as the index-set elements and
          values representing the objective coefficient; will fallback to the default for index-set
          elements not found in dict/ParamDict keys.

        Default is ``0.0``.
    type : HighsVarType, optional
        Variable type, in one of the following forms:

        * ``HighsVarType.kContinuous``
        * ``HighsVarType.kInteger``
        * ``HighsVarType.kSemiContinuous``
        * ``HighsVarType.kSemiInteger``

        Default is ``HighsVarType.kContinuous``.
    name : sequence, optional
        Sequence of names for variables.

        Default is ``None``.
    name_prefix : str, optional
        Prefix for variable names if argument name not provided, by default None.  Constructed name
        will be name_prefix + index. It will also be used as the ``value_name`` attribute of
        VarDict1D/VarDictND.

    Returns
    -------
    VarDict1D or VarDictND

    Raises
    ------
    ValueError
        If the index-set is empty.

    Examples
    --------
    Create highspy model:

    >>> from highspy import Highs, HighsVarType
    >>> mdl = Highs()

    Create index-sets:

    >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')
    >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

    Add variables:

    >>> node_select = addVariables(
    ...     mdl, nodes, type=HighsVarType.kInteger, lb=0, ub=1, name_prefix='select'
    ... )
    >>> node_select
    VarDict1D: node -> select
    {'A': highs_var(0), 'B': highs_var(1), 'C': highs_var(2)}

    >>> arc_flow = addVariables(mdl, arcs, ub=10, type=HighsVarType.kContinuous, name_prefix='flow')
    >>> arc_flow
    VarDictND: (ori, des) -> flow
    {('A', 'B'): highs_var(3), ('B', 'C'): highs_var(4), ('C', 'B'): highs_var(5)}
    """
    if not isinstance(model, Highs):
        raise TypeError('`model` should be highspy.Highs')
    if not isinstance(indexset, IndexSet1D | IndexSetND):
        raise TypeError('`indexset` should be either IndexSet1D or IndexSetND')
    if not indexset:
        raise ValueError(f'{indexset.__class__.__name__} is empty')

    lb = _preprocess_attr(indexset, lb, 'lb')  # type: ignore[misc]
    ub = _preprocess_attr(indexset, ub, 'ub')  # type: ignore[misc]
    obj = _preprocess_attr(indexset, obj, 'obj')  # type: ignore[misc]

    highs_var_dict = model.addVariables(
        indexset, lb=lb, ub=ub, obj=obj, type=type, name_prefix=name_prefix, out_array=False
    )

    value_name = name_prefix if isinstance(name_prefix, str) else None

    if isinstance(indexset, IndexSet1D):
        return VarDict1D._create(
            highs_var_dict, indexset, model=model, type=type, value_name=value_name
        )
    return VarDictND._create(
        highs_var_dict, indexset, model=model, type=type, value_name=value_name
    )
