# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict data structures."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Literal, TypeVar, cast

import xpress as xp

from .._dict_mixins import Dict1DMixin, DictNDMixin
from .._index_sets import Elem1DT, ElemNDT, ElemT, IndexSet1D, IndexSetBase, IndexSetND
from .._var_dict_base import VarDictBase

VarT = TypeVar('VarT', bound=xp.var)


class VarDictCore(VarDictBase[ElemT, VarT]):
    """Base class for custom subclasses of `dict` to define xpress problem variables.

    Provides runtime type checks to ensure variables are `xpress.var` objects.

    Parameters
    ----------
    xp_var_dict : dict
        Dictionary of variable objects associated with the xpress problem.
    indexset : IndexSetBase
        Keys of dictionary encapsulated in an IndexSet.
    problem : xpress.problem
        Xpress problem associated with the variable objects.
    vartype : int
        Variable type for new variable (`xpress.continuous`, `xpress.binary`, `xpress.integer`,
        `xpress.semicontinuous`, `xpress.semiinteger`, or `xpress.partiallyinteger`).
    """

    __slots__ = ('_problem', '_vartype')

    def __init__(
        self,
        xp_var_dict: dict[ElemT, VarT],
        /,
        *,
        indexset: IndexSetBase[ElemT],
        problem: xp.problem,
        vartype: int,
    ) -> None:
        self._validate_xp_var_dict(xp_var_dict)

        self._problem = problem
        self._vartype = vartype

        super().__init__(xp_var_dict, indexset)

    @property
    def problem(self) -> xp.problem:
        """The Xpress problem associated with the variables.

        Returns
        -------
        xpress.problem
        """
        return self._problem

    @property
    def vartype(self) -> int:
        """The variable type corresponding to the xpress variables.

        Returns
        -------
        int
        """
        return self._vartype

    @staticmethod
    def _validate_xp_var_dict(xp_var_dict: dict[ElemT, VarT]) -> None:
        """Validate that the input is a populated dict of xpress variables.

        Parameters
        ----------
        xp_var_dict : dict
            Input dictionary for VarDict.
        """
        if not isinstance(xp_var_dict, dict):
            raise TypeError('input should be a dict')
        if not xp_var_dict:
            raise ValueError('dict should be populated')
        if any(not isinstance(x, xp.var) for x in xp_var_dict.values()):
            raise TypeError('dict values should be xpress.var objects')


class VarDict1D(VarDictCore[Elem1DT, VarT], Dict1DMixin[Elem1DT, VarT]):
    """Custom subclasses of `dict` to define xpress problem variables with 1-dim scalar keys.

    Parameters
    ----------
    xp_var_dict : dict
        Dictionary of variable objects from xpress.
    indexset : IndexSet1D
        Keys of dictionary encapsulated in IndexSet1D.
    problem : xpress.problem
        Xpress problem associated with the variable objects.
    vartype : int
        Variable type for new variable (`xpress.continuous`, `xpress.binary`, `xpress.integer`,
        `xpress.semicontinuous`, `xpress.semiinteger`, or `xpress.partiallyinteger`).
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
        xp_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        problem: xp.problem,
        vartype: int,
        value_name: str | None = None,
    ) -> None:
        self.key_name = indexset.name
        self.value_name = value_name

        super().__init__(xp_var_dict, indexset=indexset, problem=problem, vartype=vartype)

    def __new__(
        cls,
        xp_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        problem: xp.problem,
        vartype: int,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDict1D is built through the '
            'opti_extensions.xpress.addVariables function'
        )

    @classmethod
    def _create(
        cls,
        xp_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        problem: xp.problem,
        vartype: int,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        # Private method to construct VarDict1D
        instance = super().__new__(cls)
        cls.__init__(
            instance, xp_var_dict, indexset, problem=problem, vartype=vartype, value_name=value_name
        )
        return instance

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p, cycle: bool) -> None:  # type: ignore[no-untyped-def]
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        # Since IPython is not typed, we'll add a type ignore comment here
        # The annotation for arg `p` is `IPython.lib.pretty.RepresentationPrinter`
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(self, key: Elem1DT) -> VarT | Literal[0]:
        """Get the variable for the specified key, or zero if it is not found.

        Parameters
        ----------
        key : key

        Returns
        -------
        xpress.var or ``0``

        Examples
        --------
        Create xpress problem:

        >>> import xpress as xp
        >>> import warnings
        >>> warnings.filterwarnings('ignore', category=xp.LicenseWarning)

        >>> prob = xp.problem()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from opti_extensions.xpress import addVariables
        >>> node_select = addVariables(prob, nodes, name='node-select', vartype=xp.binary)

        Lookup for keys:

        >>> node_select.lookup('A')
        node-select(A)

        >>> node_select.lookup('Z')
        0
        """
        return super().get(key, 0)

    def sum(self) -> xp.expression:
        """Sum all variables in a linear expression.

        Returns
        -------
        xpress.expression

        Examples
        --------
        Create xpress problem:

        >>> import xpress as xp
        >>> import warnings
        >>> warnings.filterwarnings('ignore', category=xp.LicenseWarning)

        >>> prob = xp.problem()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from opti_extensions.xpress import addVariables
        >>> node_select = addVariables(prob, nodes, name='node-select', vartype=xp.binary)

        Sum all variables:

        >>> node_select.sum()
        node-select(A) + node-select(B) + node-select(C)
        """
        return xp.Sum(self)


class VarDictND(VarDictCore[ElemNDT, VarT], DictNDMixin[ElemNDT, VarT]):
    """Custom subclasses of `dict` to define xpress problem variables with N-dim tuple keys.

    Parameters
    ----------
    xp_var_dict : dict
        Dictionary of variable objects from xpress.
    indexset : IndexSetND
        Keys of dictionary encapsulated in IndexSetND.
    problem : xpress.problem
        Xpress problem associated with the variable objects.
    vartype : int
        Variable type for new variable (`xpress.continuous`, `xpress.binary`, `xpress.integer`,
        `xpress.semicontinuous`, `xpress.semiinteger`, or `xpress.partiallyinteger`).
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
        xp_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        problem: xp.problem,
        vartype: int,
        value_name: str | None = None,
    ) -> None:
        self.key_names = indexset.names
        self.value_name = value_name

        super().__init__(xp_var_dict, indexset=indexset, problem=problem, vartype=vartype)

    def __new__(
        cls,
        xp_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        problem: xp.problem,
        vartype: int,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDictND is built through the '
            'opti_extensions.xpress.addVariables function'
        )

    @classmethod
    def _create(
        cls,
        xp_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        problem: xp.problem,
        vartype: int,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        # Private method to construct VarDictND
        instance = super().__new__(cls)
        cls.__init__(
            instance, xp_var_dict, indexset, problem=problem, vartype=vartype, value_name=value_name
        )
        return instance

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p, cycle: bool) -> None:  # type: ignore[no-untyped-def]
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        # Since IPython is not typed, we'll add a type ignore comment here
        # The annotation for arg `p` is `IPython.lib.pretty.RepresentationPrinter`
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(self, *key: Any) -> VarT | Literal[0]:
        """Get the variable for the specified key, or zero if it is not found.

        Parameters
        ----------
        *key : key

        Returns
        -------
        xpress.var or ``0``

        Examples
        --------
        Create xpress problem:

        >>> import xpress as xp
        >>> import warnings
        >>> warnings.filterwarnings('ignore', category=xp.LicenseWarning)

        >>> prob = xp.problem()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from opti_extensions.xpress import addVariables
        >>> arc_flow = addVariables(prob, arcs, name='arc-flow', ub=10, vartype=xp.continuous)

        Lookup with keys:

        >>> arc_flow.lookup('A', 'B')
        arc-flow(('A', 'B'))

        >>> arc_flow.lookup('X', 'Y')
        0
        """
        if any((isinstance(k, Iterable) and not isinstance(k, str)) for k in key):
            raise TypeError('lookup key must be scalars (no iterables except string)')
        if len(key) != self._indexset._tuplelen:
            raise ValueError('lookup key length must be the same as that of N-dim tuple keys')
        return super().get(cast('ElemNDT', key), 0)

    def sum(self, *pattern: Any) -> xp.expression:
        """Sum all variables, or a subset based on wildcard pattern, in a linear expression.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        xpress.expression

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
        Create xpress problem:

        >>> import xpress as xp
        >>> import warnings
        >>> warnings.filterwarnings('ignore', category=xp.LicenseWarning)

        >>> prob = xp.problem()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from opti_extensions.xpress import addVariables
        >>> arc_flow = addVariables(prob, arcs, name='arc-flow', ub=10, vartype=xp.continuous)

        Sum all variables:

        >>> arc_flow.sum()
        arc-flow(('A', 'B')) + arc-flow(('B', 'C')) + arc-flow(('C', 'B'))

        Sum subset of variables having ``'B'`` at the second dimension index:

        >>> arc_flow.sum('*', 'B')
        arc-flow(('A', 'B')) + arc-flow(('C', 'B'))

        Sum subset of variables having ``'Z'`` at the first dimension index:

        >>> arc_flow.sum('Z', '*')
        0
        """
        if pattern:
            return xp.Sum(self.subset_values(*pattern))

        return xp.Sum(self)
