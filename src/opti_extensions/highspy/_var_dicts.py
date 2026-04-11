# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict data structures."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Literal, NoReturn, TypeVar, cast

from highspy import Highs as HighsModel
from highspy import HighsVarType
from highspy.highs import highs_linear_expression, highs_var

from .._dict_mixins import Dict1DMixin, DictNDMixin
from .._index_sets import Elem1DT, ElemNDT, ElemT, IndexSet1D, IndexSetBase, IndexSetND
from .._param_dicts import ParamDict1D, ParamDictND, ParamT
from .._var_dict_base import VarDictBase, _validate_for_dot_1d, _validate_for_dot_Nd

if TYPE_CHECKING:
    from .._misc_types import MinimalRepresentationPrinter

VarT = TypeVar('VarT', bound=highs_var)


class VarDictCore(VarDictBase[ElemT, VarT]):
    """Base class for custom subclasses of `dict` to define highspy model variables.

    Provides runtime type checks to ensure variables are `highspy.highs_var` objects.

    Parameters
    ----------
    highs_var_dict : dict
        Dictionary of variable objects associated with the highspy model.
    indexset : IndexSetBase
        Keys of dictionary encapsulated in an IndexSet.
    model : highspy.Highs
        The highspy model associated with the variable objects.
    type : highspy.HighsVarType
        Variable type for new variable (`HighsVarType.kContinuous`, `HighsVarType.kInteger`,
        `HighsVarType.kSemiContinuous`, or  `HighsVarType.kSemiInteger`).
    """

    __slots__ = ('_Highs', '_type')

    def __init__(
        self,
        highs_var_dict: dict[ElemT, VarT],
        /,
        *,
        indexset: IndexSetBase[ElemT],
        model: HighsModel,
        type: HighsVarType,
    ) -> None:
        self._validate_highs_var_dict(highs_var_dict)

        self._Highs = model
        self._type = type

        super().__init__(highs_var_dict, indexset)

    @property
    def Highs(self) -> HighsModel:
        """The highspy model associated with the variables.

        Returns
        -------
        highspy.Highs
        """
        return self._Highs

    @property
    def type(self) -> HighsVarType:
        """The variable type corresponding to the highspy variables.

        Returns
        -------
        HighsVarType
        """
        return self._type

    @staticmethod
    def _validate_highs_var_dict(highs_var_dict: dict[ElemT, VarT]) -> None:
        """Validate that the input is a populated dict of highspy variables.

        Parameters
        ----------
        highs_var_dict : dict
            Input dictionary for VarDict.
        """
        if not isinstance(highs_var_dict, dict):
            raise TypeError('input should be a dict')
        if not highs_var_dict:
            raise ValueError('dict should be populated')
        if any(not isinstance(x, highs_var) for x in highs_var_dict.values()):
            raise TypeError('dict values should be highspy.highs_var objects')


class VarDict1D(VarDictCore[Elem1DT, VarT], Dict1DMixin[Elem1DT, VarT]):
    """Custom subclasses of `dict` to define highspy model variables with 1-dim scalar keys.

    Parameters
    ----------
    highs_var_dict : dict
        Dictionary of variable objects from highspy.
    indexset : IndexSet1D
        Keys of dictionary encapsulated in IndexSet1D.
    model : highspy.Highs
        The highspy model associated with the variable objects.
    type : highspy.HighsVarType
        Variable type for new variable (`HighsVarType.kContinuous`, `HighsVarType.kInteger`,
        `HighsVarType.kSemiContinuous`, or  `HighsVarType.kSemiInteger`).
    value_name : str, optional
        Name to refer to variables - not used internally, and solely for user reference.
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSet1D
    #     Index-set of keys.

    __slots__ = ('_key_name', '_value_name')

    def __init__(
        self,
        highs_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: HighsModel,
        type: HighsVarType,
        value_name: str | None = None,
    ) -> None:
        self.key_name = indexset.name
        self.value_name = value_name

        super().__init__(highs_var_dict, indexset=indexset, model=model, type=type)

    def __new__(
        cls,
        highs_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: HighsModel,
        type: HighsVarType,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDict1D is built through the '
            'opti_extensions.highspy.addVariables function'
        )

    @classmethod
    def _create(
        cls,
        highs_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: HighsModel,
        type: HighsVarType,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        # Private method to construct VarDict1D
        instance = super().__new__(cls)
        cls.__init__(
            instance, highs_var_dict, indexset, model=model, type=type, value_name=value_name
        )
        return instance

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p: MinimalRepresentationPrinter, cycle: bool) -> None:
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(self, key: Elem1DT) -> VarT | Literal[0]:
        """Get the variable for the specified key, or zero if it is not found.

        Parameters
        ----------
        key : key

        Returns
        -------
        highspy.highs_var or ``0``

        Examples
        --------
        Create highspy model:

        >>> from highspy import Highs, HighsVarType
        >>> mdl = Highs()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from opti_extensions.highspy import addVariables
        >>> node_select = addVariables(
        ...     mdl, nodes, type=HighsVarType.kInteger, lb=0, ub=1, name_prefix='node-select_'
        ... )

        Lookup for keys:

        >>> node_select.lookup('A')
        highs_var(0)

        >>> node_select.lookup('Z')
        0
        """
        return super().get(key, 0)

    def sum(self) -> highs_linear_expression:
        """Sum all variables in an expression.

        Returns
        -------
        highspy.highs_linear_expression

        Examples
        --------
        Create highspy model:

        >>> from highspy import Highs, HighsVarType
        >>> mdl = Highs()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from opti_extensions.highspy import addVariables
        >>> node_select = addVariables(
        ...     mdl, nodes, type=HighsVarType.kInteger, lb=0, ub=1, name_prefix='node-select_'
        ... )

        Sum all variables:

        >>> node_select.sum()
        1.0_v0  1.0_v1  1.0_v2
        """
        return self.Highs.qsum(self.values())

    def sum_squares(self) -> NoReturn:
        """Sum squares of variables in an expression.

        Raises
        ------
        NotImplementedError
            This method is not implemented for highspy as it does not support quadratic expressions.
        """
        raise NotImplementedError(
            'sum_squares is not implemented for highspy as it does not support '
            'quadratic expressions'
        )

    def dot(self, paramdict: ParamDict1D[Elem1DT, ParamT]) -> highs_linear_expression:
        """Sum the products of variables with corresponding coef from ParamDict1D, in an expression.

        Assumes the coef to be zero if not found in the ParamDict1D.

        Equivalent to::

          highspy.Highs.qsum(paramdict.get(k, 0) * v for k, v in vardict.items())

        Parameters
        ----------
        paramdict : ParamDict1D
            ParamDict1D to be used for dot product.

        Returns
        -------
        highspy.highs_linear_expression

        Raises
        ------
        TypeError
            If the paramdict is not as instance of ParamDict1D.

        Notes
        -----
        This method is equivalent to using the matrix multiplication operator ``@``.

        Both ``ParamDict1D @ VarDict1D`` and ``VarDict1D @ ParamDict1D`` will also produce the same
        result.

        Examples
        --------
        Create highspy model:

        >>> from highspy import Highs, HighsVarType
        >>> mdl = Highs()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from opti_extensions.highspy import addVariables
        >>> node_select = addVariables(
        ...     mdl, nodes, type=HighsVarType.kInteger, lb=0, ub=1, name_prefix='node-select_'
        ... )

        Define parameter:

        >>> from opti_extensions import ParamDict1D
        >>> fixed_cost = ParamDict1D({'A': 100, 'B': 200})

        Compute dot product (three alternative ways):

        >>> node_select.dot(fixed_cost)
        100.0_v0  200.0_v1  0.0_v2

        >>> fixed_cost @ node_select
        100.0_v0  200.0_v1  0.0_v2

        >>> node_select @ fixed_cost
        100.0_v0  200.0_v1  0.0_v2
        """
        _validate_for_dot_1d(paramdict)
        return self.Highs.qsum(paramdict.get(k, 0) * v for k, v in self.items())

    __matmul__ = dot

    __rmatmul__ = dot


class VarDictND(VarDictCore[ElemNDT, VarT], DictNDMixin[ElemNDT, VarT]):
    """Custom subclasses of `dict` to define highspy model variables with N-dim tuple keys.

    Parameters
    ----------
    highs_var_dict : dict
        Dictionary of variable objects from highspy.
    indexset : IndexSetND
        Keys of dictionary encapsulated in IndexSetND.
    model : highspy.Highs
        The highspy model associated with the variable objects.
    type : highspy.HighsVarType
        Variable type for new variable (`HighsVarType.kContinuous`, `HighsVarType.kInteger`,
        `HighsVarType.kSemiContinuous`, or  `HighsVarType.kSemiInteger`).
    value_name : str, optional
        Name to refer to variables - not used internally, and solely for user reference.
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSetND
    #     Index-set of keys.

    __slots__ = ('_key_names', '_value_name')

    def __init__(
        self,
        highs_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: HighsModel,
        type: HighsVarType,
        value_name: str | None = None,
    ) -> None:
        self.key_names = indexset.names
        self.value_name = value_name

        super().__init__(highs_var_dict, indexset=indexset, model=model, type=type)

    def __new__(
        cls,
        highs_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: HighsModel,
        type: HighsVarType,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDictND is built through the '
            'opti_extensions.highspy.addVariables function'
        )

    @classmethod
    def _create(
        cls,
        highs_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: HighsModel,
        type: HighsVarType,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        # Private method to construct VarDictND
        instance = super().__new__(cls)
        cls.__init__(
            instance, highs_var_dict, indexset, model=model, type=type, value_name=value_name
        )
        return instance

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p: MinimalRepresentationPrinter, cycle: bool) -> None:
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(self, *key: Any) -> VarT | Literal[0]:
        """Get the variable for the specified key, or zero if it is not found.

        Parameters
        ----------
        *key : key

        Returns
        -------
        highspy.highs_var or ``0``

        Examples
        --------
        Create highspy model:

        >>> from highspy import Highs, HighsVarType
        >>> mdl = Highs()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from opti_extensions.highspy import addVariables
        >>> arc_flow = addVariables(
        ...     mdl, arcs, ub=10, type=HighsVarType.kContinuous, name_prefix='arc-flow_'
        ... )

        Lookup with keys:

        >>> arc_flow.lookup('A', 'B')
        highs_var(0)

        >>> arc_flow.lookup('X', 'Y')
        0
        """
        if any((isinstance(k, Iterable) and not isinstance(k, str)) for k in key):
            raise TypeError('lookup key must be scalars (no iterables except string)')
        if len(key) != self._indexset._tuplelen:
            raise ValueError('lookup key length must be the same as that of N-dim tuple keys')
        return super().get(cast('ElemNDT', key), 0)

    def sum(self, *pattern: Any) -> highs_linear_expression:
        """Sum all variables, or a subset based on wildcard pattern, in an expression.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        highspy.highs_linear_expression

        Raises
        ------
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        Create highspy model:

        >>> from highspy import Highs, HighsVarType
        >>> mdl = Highs()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from opti_extensions.highspy import addVariables
        >>> arc_flow = addVariables(
        ...     mdl, arcs, ub=10, type=HighsVarType.kContinuous, name_prefix='arc-flow_'
        ... )

        Sum all variables:

        >>> arc_flow.sum()
        1.0_v0  1.0_v1  1.0_v2

        Sum subset of variables having ``'B'`` at the second dimension index:

        >>> arc_flow.sum('*', 'B')
        1.0_v0  1.0_v2

        Sum subset of variables having ``'Z'`` at the first dimension index:

        >>> arc_flow.sum('Z', '*')
        <BLANKLINE>
        """
        if pattern:
            return self.Highs.qsum(self.subset_values(*pattern))

        res: highs_linear_expression = self.Highs.qsum(self.values())
        return res

    def sum_squares(self, *pattern: Any) -> NoReturn:
        """Sum squares of variables, or a subset based on wildcard pattern, in an expression.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Raises
        ------
        NotImplementedError
            This method is not implemented for highspy as it does not support quadratic expressions.
        """
        raise NotImplementedError(
            'sum_squares is not implemented for highspy as it does not support '
            'quadratic expressions'
        )

    def dot(self, paramdict: ParamDictND[ElemNDT, ParamT]) -> highs_linear_expression:
        """Sum the products of variables with corresponding coef from ParamDictND, in an expression.

        Assumes the coef to be zero if not found in the ParamDictND.

        Equivalent to::

          highspy.Highs.qsum(paramdict.get(k, 0) * v for k, v in vardict.items())

        Parameters
        ----------
        paramdict : ParamDictND
            ParamDictND to be used for dot product; should have tuple keys of same length as
            VarDictND.

        Returns
        -------
        highspy.highs_linear_expression

        Raises
        ------
        TypeError
            If the paramdict is not as instance of ParamDictND.
        ValueError
            If the paramdict does not have tuple keys of same length as VarDictND.

        Notes
        -----
        This method is equivalent to using the matrix multiplication operator ``@``.

        Both ``ParamDictND @ VarDictND`` and ``VarDictND @ ParamDictND`` will also produce the same
        result.

        Examples
        --------
        Create highspy model:

        >>> from highspy import Highs, HighsVarType
        >>> mdl = Highs()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from opti_extensions.highspy import addVariables
        >>> arc_flow = addVariables(
        ...     mdl, arcs, ub=10, type=HighsVarType.kContinuous, name_prefix='arc-flow_'
        ... )

        Define parameter:

        >>> from opti_extensions import ParamDictND
        >>> cost = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20})

        Compute dot product (three alternative ways):

        >>> arc_flow.dot(cost)
        10.0_v0  20.0_v1  0.0_v2

        >>> cost @ arc_flow
        10.0_v0  20.0_v1  0.0_v2

        >>> arc_flow @ cost
        10.0_v0  20.0_v1  0.0_v2
        """
        _validate_for_dot_Nd(self._indexset, paramdict)
        return self.Highs.qsum(paramdict.get(k, 0) * v for k, v in self.items())

    __matmul__ = dot

    __rmatmul__ = dot
