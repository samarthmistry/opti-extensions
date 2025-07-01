# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict data structures."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Literal, TypeVar, cast

from gurobipy import LinExpr, Model, Var, quicksum

from .._dict_mixins import Dict1DMixin, DictNDMixin
from .._index_sets import Elem1DT, ElemNDT, ElemT, IndexSet1D, IndexSetBase, IndexSetND
from .._var_dict_base import VarDictBase

VarT = TypeVar('VarT', bound=Var)


class VarDictCore(VarDictBase[ElemT, VarT]):
    """Base class for custom subclasses of `dict` to define gurobipy model variables.

    Provides runtime type checks to ensure variables are `gurobipy.Var` objects.

    Parameters
    ----------
    gp_var_dict : dict
        Dictionary of variable objects associated with the gurobipy model.
    indexset : IndexSetBase
        Keys of dictionary encapsulated in an IndexSet.
    model : gurobipy.Model
        The gurobipy model associated with the variable objects.
    vtype : str
        Variable type for new variable (`GRB.CONTINUOUS`, `GRB.BINARY`, `GRB.INTEGER`,
        `GRB.SEMICONT`, or  `GRB.SEMIINT`).
    """

    __slots__ = ('_Model', '_VType')

    def __init__(
        self,
        gp_var_dict: dict[ElemT, VarT],
        /,
        *,
        indexset: IndexSetBase[ElemT],
        model: Model,
        vtype: str,
    ) -> None:
        self._validate_gp_var_dict(gp_var_dict)

        self._Model = model
        self._VType = vtype

        super().__init__(gp_var_dict, indexset)

    @property
    def Model(self) -> Model:
        """The gurobipy model associated with the variables.

        Returns
        -------
        gurobipy.Model
        """
        return self._Model

    @property
    def VType(self) -> str:
        """The variable type corresponding to the gurobipy variables.

        Returns
        -------
        str
        """
        return self._VType

    @staticmethod
    def _validate_gp_var_dict(gp_var_dict: dict[ElemT, VarT]) -> None:
        """Validate that the input is a populated dict of gurobipy variables.

        Parameters
        ----------
        gp_var_dict : dict
            Input dictionary for VarDict.
        """
        if not isinstance(gp_var_dict, dict):
            raise TypeError('input should be a dict')
        if not gp_var_dict:
            raise ValueError('dict should be populated')
        if any(not isinstance(x, Var) for x in gp_var_dict.values()):
            raise TypeError('dict values should be gurobipy.Var objects')


class VarDict1D(VarDictCore[Elem1DT, VarT], Dict1DMixin[Elem1DT, VarT]):
    """Custom subclasses of `dict` to define gurobipy model variables with 1-dim scalar keys.

    Parameters
    ----------
    gp_var_dict : dict
        Dictionary of variable objects from gurobipy.
    indexset : IndexSet1D
        Keys of dictionary encapsulated in IndexSet1D.
    model : gurobipy.Model
        The gurobipy model associated with the variable objects.
    vtype : str
        Variable type for new variable (`GRB.CONTINUOUS`, `GRB.BINARY`, `GRB.INTEGER`,
        `GRB.SEMICONT`, or  `GRB.SEMIINT`).
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
        gp_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: Model,
        vtype: str,
        value_name: str | None = None,
    ) -> None:
        self.key_name = indexset.name
        self.value_name = value_name

        super().__init__(gp_var_dict, indexset=indexset, model=model, vtype=vtype)

    def __new__(
        cls,
        gp_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: Model,
        vtype: str,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDict1D is built through the '
            'opti_extensions.gurobipy.addVars function'
        )

    @classmethod
    def _create(
        cls,
        gp_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: Model,
        vtype: str,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        # Private method to construct VarDict1D
        instance = super().__new__(cls)
        cls.__init__(
            instance, gp_var_dict, indexset, model=model, vtype=vtype, value_name=value_name
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
        gurobipy.Var or ``0``

        Examples
        --------
        Create gurobipy model:

        >>> from gurobipy import GRB, Model
        >>> mdl = Model()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from opti_extensions.gurobipy import addVars
        >>> node_select = addVars(mdl, nodes, vtype=GRB.BINARY, name='node-select')
        >>> mdl.update()

        Lookup for keys:

        >>> node_select.lookup('A')
        <gurobi.Var node-select[A]>

        >>> node_select.lookup('Z')
        0
        """
        return super().get(key, 0)

    def sum(self) -> LinExpr:
        """Sum all variables in a linear expression.

        Returns
        -------
        gurobipy.LinExpr

        Examples
        --------
        Create gurobipy model:

        >>> from gurobipy import GRB, Model
        >>> mdl = Model()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from opti_extensions.gurobipy import addVars
        >>> node_select = addVars(mdl, nodes, vtype=GRB.BINARY, name='node-select')
        >>> mdl.update()

        Sum all variables:

        >>> node_select.sum()
        <gurobi.LinExpr: node-select[A] + node-select[B] + node-select[C]>
        """
        return quicksum(self.values())


class VarDictND(VarDictCore[ElemNDT, VarT], DictNDMixin[ElemNDT, VarT]):
    """Custom subclasses of `dict` to define gurobipy model variables with N-dim tuple keys.

    Parameters
    ----------
    gp_var_dict : dict
        Dictionary of variable objects from gurobipy.
    indexset : IndexSetND
        Keys of dictionary encapsulated in IndexSetND.
    model : gurobipy.Model
        The gurobipy model associated with the variable objects.
    vtype : str
        Variable type for new variable (`GRB.CONTINUOUS`, `GRB.BINARY`, `GRB.INTEGER`,
        `GRB.SEMICONT`, or  `GRB.SEMIINT`).
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
        gp_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: Model,
        vtype: str,
        value_name: str | None = None,
    ) -> None:
        self.key_names = indexset.names
        self.value_name = value_name

        super().__init__(gp_var_dict, indexset=indexset, model=model, vtype=vtype)

    def __new__(
        cls,
        gp_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: Model,
        vtype: str,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDictND is built through the '
            'opti_extensions.gurobipy.addVars function'
        )

    @classmethod
    def _create(
        cls,
        gp_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: Model,
        vtype: str,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        # Private method to construct VarDictND
        instance = super().__new__(cls)
        cls.__init__(
            instance, gp_var_dict, indexset, model=model, vtype=vtype, value_name=value_name
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
        gurobipy.Var or ``0``

        Examples
        --------
        Create gurobipy model:

        >>> from gurobipy import GRB, Model
        >>> mdl = Model()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from opti_extensions.gurobipy import addVars
        >>> arc_flow = addVars(mdl, arcs, ub=10, vtype=GRB.CONTINUOUS, name='arc-flow')
        >>> mdl.update()

        Lookup with keys:

        >>> arc_flow.lookup('A', 'B')
        <gurobi.Var arc-flow[A,B]>

        >>> arc_flow.lookup('X', 'Y')
        0
        """
        if any((isinstance(k, Iterable) and not isinstance(k, str)) for k in key):
            raise TypeError('lookup key must be scalars (no iterables except string)')
        if len(key) != self._indexset._tuplelen:
            raise ValueError('lookup key length must be the same as that of N-dim tuple keys')
        return super().get(cast('ElemNDT', key), 0)

    def sum(self, *pattern: Any) -> LinExpr:
        """Sum all variables, or a subset based on wildcard pattern, in a linear expression.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        gurobipy.LinExpr

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
        Create gurobipy model:

        >>> from gurobipy import GRB, Model
        >>> mdl = Model()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from opti_extensions.gurobipy import addVars
        >>> arc_flow = addVars(mdl, arcs, ub=10, vtype=GRB.CONTINUOUS, name='arc-flow')
        >>> mdl.update()

        Sum all variables:

        >>> arc_flow.sum()
        <gurobi.LinExpr: arc-flow[A,B] + arc-flow[B,C] + arc-flow[C,B]>

        Sum subset of variables having ``'B'`` at the second dimension index:

        >>> arc_flow.sum('*', 'B')
        <gurobi.LinExpr: arc-flow[A,B] + arc-flow[C,B]>

        Sum subset of variables having ``'Z'`` at the first dimension index:

        >>> arc_flow.sum('Z', '*')
        <gurobi.LinExpr: 0.0>
        """
        if pattern:
            return quicksum(self.subset_values(*pattern))

        res: LinExpr = quicksum(self.values())
        return res
