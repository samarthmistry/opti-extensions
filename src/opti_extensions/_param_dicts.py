# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""ParamDict data structures."""

from __future__ import annotations

import statistics
from collections import abc
from collections.abc import Callable, Iterable, Mapping, Sequence
from functools import partial
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast, overload

from typing_extensions import Never, Self, TypeVarTuple, Unpack, deprecated

from ._dict_mixins import DefaultT, Dict1DMixin, DictBaseMixin, DictNDMixin
from ._index_sets import (
    _S1,
    _S2,
    _S3,
    _S4,
    Elem1DT,
    ElemNDT,
    ElemT,
    IndexSet1D,
    IndexSetBase,
    IndexSetND,
)

if TYPE_CHECKING:
    import pandas as pd

    from ._misc_types import MinimalRepresentationPrinter

ParamT = TypeVar('ParamT', bound=int | float)
Ts = TypeVarTuple('Ts')


class _RAISE_KEYERROR:
    __slots__ = ()


_raise_keyerror = _RAISE_KEYERROR()


_builtin_op: dict[str, Callable[..., int | float]] = {
    'sum': sum,
    'min': partial(min, default=0),
    'max': partial(max, default=0),
}


class ParamDictBase(dict[ElemT, ParamT], DictBaseMixin[ElemT, ParamT]):
    """Base class for custom subclasses of `dict` to define parameters.

    Provides runtime type checks to ensure parameter values are `int` or `float`.

    Parameters
    ----------
    mapping : dict or dict-like mapping, optional
        Input data to be encapsulated in the ParamDict.
    indexset : IndexSetBase
        Keys of mapping encapsulated in an IndexSet.
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSetBase
    #     Index-set of keys.

    __slots__ = ('_indexset',)

    def __init__(
        self, mapping: Mapping[ElemT, ParamT], /, *, indexset: IndexSetBase[ElemT]
    ) -> None:
        if any(not self._is_valid_value_type(x) for x in mapping.values()):
            raise TypeError("input mapping's values should be either int or float")

        self._indexset = indexset
        """Index-set of keys."""

        super().__init__(mapping)

    @staticmethod
    def _is_valid_value_type(value: ParamT) -> bool:
        """Check if the type of a value is valid (either int or float) or not.

        Parameters
        ----------
        value : Any

        Returns
        -------
        bool
        """
        return isinstance(value, int | float)

    def __setitem__(self, key: ElemT, value: ParamT, /) -> None:
        # Set `self[key]` to `value`.
        if self._is_valid_value_type(value):
            if key in self._indexset:
                super().__setitem__(key, value)
            else:
                try:
                    self._indexset.append(key)
                    super().__setitem__(key, value)
                except Exception as exc:
                    self._reraise_exc_from_indexset(exc)
        else:
            raise TypeError('`value` should be either int or float')

    def __delitem__(self, key: ElemT, /) -> None:
        # Remove `self[key]`.
        super().__delitem__(key)
        self._indexset.remove(key)

    def clear(self) -> None:
        """Remove all items from the ParamDict."""
        super().clear()
        self._indexset.clear()

    @overload  # type: ignore[override]
    @deprecated('`copy` is not supported by ParamDict.', category=None)
    def copy(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`copy` is not supported by ParamDict.', category=None)
    def copy(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`copy` is not supported by ParamDict.', category=None)
    def copy(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by ParamDict."""
        self._raise_not_supported_err('copy')

    @overload
    def get(self, key: ElemT, default: None = ..., /) -> ParamT | None: ...  # numpydoc ignore=GL08

    @overload
    def get(self, key: ElemT, default: ParamT = ..., /) -> ParamT: ...  # numpydoc ignore=GL08

    @overload
    def get(
        self, key: ElemT, default: DefaultT = ..., /
    ) -> ParamT | DefaultT: ...  # numpydoc ignore=GL08

    def get(self, key: ElemT, default: DefaultT | None = None, /) -> ParamT | DefaultT | None:
        """Get the parameter value for the specified key, or the default if not found.

        Parameters
        ----------
        key : key
        default : Any, optional

        Returns
        -------
        int or float or ``default``
        """
        return super().get(key, default)

    @overload
    def pop(self, key: ElemT, /) -> ParamT: ...  # numpydoc ignore=GL08

    @overload
    def pop(
        self, key: ElemT, default: DefaultT, /
    ) -> ParamT | DefaultT: ...  # numpydoc ignore=GL08

    def pop(
        self, key: ElemT, default: DefaultT | _RAISE_KEYERROR = _raise_keyerror, /
    ) -> ParamT | DefaultT:
        """Remove the specified key and return it's parameter value, or the default if not found.

        Parameters
        ----------
        key : key
        default : int or float, optional

        Returns
        -------
        int or float or ``default``

        Raises
        ------
        KeyError
            If key not found in the ParamDict.
        """
        if key in self:
            self._indexset.remove(key)
        if isinstance(default, _RAISE_KEYERROR):
            return super().pop(key)
        else:
            return super().pop(key, default)

    def popitem(self) -> tuple[ElemT, ParamT]:
        """Remove and return the last inserted key and parameter value pair from the ParamDict.

        Returns
        -------
        (key, int or float)
            Tuple of key, parameter value.
        """
        item = super().popitem()
        self._indexset.remove(item[0])
        return item

    def setdefault(self, key: ElemT, default: ParamT, /) -> ParamT:
        """Get the parameter value for the specified key, or the default if not found.

        If the key is not found, insert it with the parameter value of default in the ParamDict.

        Parameters
        ----------
        key : key
        default : int or float

        Returns
        -------
        int or float
        """
        if self._is_valid_value_type(default):
            if key not in self._indexset:
                try:
                    self._indexset.append(key)
                except Exception as exc:
                    self._reraise_exc_from_indexset(exc)
            return super().setdefault(key, default)
        raise TypeError('`default` should be either int or float')

    @overload  # type: ignore[override]
    @deprecated('`update` is not supported by ParamDict.', category=None)
    def update(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`update` is not supported by ParamDict.', category=None)
    def update(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`update` is not supported by ParamDict.', category=None)
    def update(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by ParamDict."""
        self._raise_not_supported_err('update')

    @overload  # type: ignore[override]
    @classmethod
    @deprecated('`fromkeys` is not supported by ParamDict.', category=None)
    def fromkeys(cls, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @classmethod
    @deprecated('`fromkeys` is not supported by ParamDict.', category=None)
    def fromkeys(
        cls, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @classmethod
    @deprecated('`fromkeys` is not supported by ParamDict.', category=None)
    def fromkeys(cls, *args: Any, **kwargs: Any) -> None:
        """Not supported by ParamDict."""
        raise AttributeError(f'`fromkeys` is not supported by {cls.__name__}')

    @deprecated('`|` is not supported by ParamDict.', category=None)
    def __or__(self, other: Never, /) -> Self:  # type: ignore[override]
        raise TypeError(f'`|` is not supported by {self.__class__.__name__}')

    @deprecated('`|` is not supported by ParamDict.', category=None)
    def __ror__(self, other: Never, /) -> Self:  # type: ignore[override]
        raise TypeError(f'`|` is not supported by {self.__class__.__name__}')

    @deprecated('`|=` is not supported by ParamDict.', category=None)
    def __ior__(self, other: Never, /) -> Self:  # type: ignore[override]
        raise TypeError(f'`|=` is not supported by {self.__class__.__name__}')

    def _check_for_calc_stat(self, stat_func: str) -> None:
        """Perform validation checks before calculating a statistic with parameter values.

        Parameters
        ----------
        stat_func : str
            Either `'sum'`, `'min'`, `'max'` or the name of the statistical function from the
            `statistics` module of the standard library.

        Raises
        ------
        ValueError
            If `stat_func` not found in the `statistics` module.
        StatisticsError
            If the ParamDict is empty.
        """
        if stat_func not in ('sum', 'min', 'max') and not hasattr(statistics, stat_func):
            raise ValueError('Given `stat_func` not found in the `statistics` module')
        if not self:
            raise statistics.StatisticsError(
                'Cannot calculate `%s` as the ParamDict is empty', stat_func
            )

    def _calc_stat_all(self, stat_func: str) -> int | float:
        """Calculate a statistic with all parameter values.

        Supports sum, min, max, and any statistical function provided in the `statistics` module of
        the standard library.

        Parameters
        ----------
        stat_func : str
            Either `'sum'`, `'min'`, `'max'` or the name of the statistical function from the
            `statistics` module of the standard library.

        Returns
        -------
        int or float
        """
        if stat_func in ('sum', 'min', 'max'):
            res: int | float = _builtin_op[stat_func](self.values())
        else:
            res = getattr(statistics, stat_func)(self.values())

        return res


class ParamDict1D(ParamDictBase[Elem1DT, ParamT], Dict1DMixin[Elem1DT, ParamT]):
    """Custom subclass of `dict` to define parameters with 1-dim scalar keys.

    Requires all keys to be unique scalars (such as `int`, `str`, `pd.Timestamp`, etc.) and all
    values to be `int` or `float`.

    Parameters
    ----------
    mapping : dict or dict-like mapping, optional
        Input data to be encapsulated in the ParamDict.
    key_name : str, optional
        Name to refer to 1-dim scalar keys - not used internally, and solely for user reference.
    value_name : str, optional
        Name to refer to parameter values - not used internally, and solely for user reference.

    Raises
    ------
    TypeError
        If input includes key(s) that are not scalar (any iterable except string).
    TypeError
        If input includes value(s) that are not int or float.

    See Also
    --------
    ParamDictND : For N-dim tuple keys.

    Examples
    --------
    Constructing empty to populate later:

    >>> ParamDict1D()
    ParamDict1D:
    {}

    Constructing with a mapping:

    >>> ParamDict1D(
    ...     {'JAN': 31, 'FEB': 28, 'MAR': 31},
    ...     key_name='MONTH',
    ...     value_name='DAYS',
    ... )
    ParamDict1D: MONTH -> DAYS
    {'JAN': 31, 'FEB': 28, 'MAR': 31}
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSet1D
    #     Index-set of 1-dim scalar keys.

    __slots__ = ('_key_name', '_value_name')

    @overload
    def __init__(
        self,
        mapping: None = None,
        /,
        *,
        key_name: str | None = None,
        value_name: str | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        mapping: Mapping[Elem1DT, ParamT],
        /,
        *,
        key_name: str | None = None,
        value_name: str | None = None,
    ) -> None: ...

    def __init__(
        self,
        mapping: Mapping[Elem1DT, ParamT] | None = None,
        /,
        *,
        key_name: str | None = None,
        value_name: str | None = None,
    ) -> None:
        self.key_name = key_name
        self.value_name = value_name

        if mapping is None:
            mapping = {}
            self._indexset: IndexSet1D[Elem1DT] = IndexSet1D(name=self.key_name)
            """Index-set of 1-dim scalar keys."""
        else:
            if not isinstance(mapping, abc.Mapping):
                raise TypeError('input should be a dict or dict-like mapping')
            try:
                self._indexset = IndexSet1D(mapping, name=self.key_name)
            except Exception as exc:
                self._reraise_exc_from_indexset(exc, caller='IndexSet1D')

        super().__init__(mapping, indexset=self._indexset)

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p: MinimalRepresentationPrinter, cycle: bool) -> None:
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(self, key: Elem1DT) -> ParamT | Literal[0]:
        """Get the parameter value for the specified key, or zero if it is not found.

        Parameters
        ----------
        key : key

        Returns
        -------
        int or float

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.lookup('chair')
        100
        >>> inventory.lookup('desk')
        0
        """
        return super().get(key, 0)

    @classmethod
    def from_series(
        cls,
        series: pd.Series[ParamT],
        *,
        key_name: str | None = None,
        value_name: str | None = None,
    ) -> ParamDict1D[Any, ParamT]:
        """Create a ParamDict1D from a pandas Series.

        Parameters
        ----------
        series : Series
            Input pandas Series whose index labels form keys and values form parameters.
        key_name : str, optional
            Name for the parameter keys. If not provided, defaults to the Series' `index.name`
            (as str) if set, or None.
        value_name : str, optional
            Name for the parameter values. If not provided, defaults to the Series' `name`
            (as str) if set, or None.

        Returns
        -------
        ParamDict1D

        Raises
        ------
        ValueError
            If the Series is empty.
        ValueError
            If the Series index contains duplicate labels.
        TypeError
            If the Series has a MultiIndex (multi-level index).
        TypeError
            If the Series index contains non-scalar labels (any iterable except string).
        TypeError
            If the Series values are not int or float.

        See Also
        --------
        ParamDict1D.from_dataframe : Create a ParamDict1D from DataFrame columns.
        ParamDictND.from_series : Create a ParamDictND from a MultiIndex Series.
        ParamDictND.from_dataframe : Create a ParamDictND from DataFrame columns.

        Examples
        --------
        >>> import pandas as pd
        >>> from opti_extensions import ParamDict1D
        >>> s = pd.Series(
        ...     [200, 500], index=pd.Index(['chair', 'desk'], name='PRODUCT'), name='UNITS'
        ... )
        >>> ParamDict1D.from_series(s)
        ParamDict1D: PRODUCT -> UNITS
        {'chair': 200, 'desk': 500}
        >>> ParamDict1D.from_series(s, key_name='ITEM', value_name='QTY')
        ParamDict1D: ITEM -> QTY
        {'chair': 200, 'desk': 500}
        """
        if series.empty:
            raise ValueError(f'{series.__class__.__name__} is empty')
        if getattr(series.index, 'nlevels', 1) > 1:
            raise TypeError(
                'MultiIndex is not supported by ParamDict1D; use ParamDictND.from_series'
            )
        if series.index.size > len(set(series.index)):
            raise ValueError(f'{series.__class__.__name__} has duplicate index-label(s)')
        if key_name is None and series.index.name is not None:
            key_name = str(series.index.name)
        if value_name is None and series.name is not None:
            value_name = str(series.name)
        return cls(series.to_dict(), key_name=key_name, value_name=value_name)

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        *,
        key_col: str,
        value_col: str,
        key_name: str | None = None,
        value_name: str | None = None,
    ) -> ParamDict1D[Any, int | float]:
        """Create a ParamDict1D from two columns of a pandas DataFrame.

        Parameters
        ----------
        df : DataFrame
            Input pandas DataFrame.
        key_col : str
            Name of column to use for parameter keys.
        value_col : str
            Name of column to use for parameter values.
        key_name : str, optional
            Name for the parameter keys. If not provided, defaults to `key_col`.
        value_name : str, optional
            Name for the parameter values. If not provided, defaults to `value_col`.

        Returns
        -------
        ParamDict1D

        Raises
        ------
        ValueError
            If the DataFrame is empty.
        ValueError
            If the `key_col` contains duplicate values.
        KeyError
            If `key_col` or `value_col` is not found in DataFrame columns.
        TypeError
            If `key_col` contains non-scalar values (any iterable except string).
        TypeError
            If `value_col` contains values that are not int or float.

        See Also
        --------
        ParamDict1D.from_series : Create a ParamDict1D from a pandas Series.
        ParamDictND.from_dataframe : Create a ParamDictND from DataFrame columns.
        ParamDictND.from_series : Create a ParamDictND from a MultiIndex Series.

        Examples
        --------
        >>> import pandas as pd
        >>> from opti_extensions import ParamDict1D
        >>> df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'UNITS': [200, 500]})
        >>> ParamDict1D.from_dataframe(df, key_col='PRODUCT', value_col='UNITS')
        ParamDict1D: PRODUCT -> UNITS
        {'chair': 200, 'desk': 500}
        >>> ParamDict1D.from_dataframe(
        ...     df, key_col='PRODUCT', value_col='UNITS', key_name='ITEM', value_name='QTY'
        ... )
        ParamDict1D: ITEM -> QTY
        {'chair': 200, 'desk': 500}
        """
        if df.empty:
            raise ValueError(f'{df.__class__.__name__} is empty')
        s = df.set_index(key_col, drop=False)[value_col]
        k_name = key_name if key_name is not None else str(key_col)
        v_name = value_name if value_name is not None else str(value_col)
        return cast(
            'ParamDict1D[Any, int | float]', cls.from_series(s, key_name=k_name, value_name=v_name)
        )

    def _calc_stat(self, stat_func: str) -> int | float:
        """Calculate a statistic with all parameter values.

        Supports sum, min, max, and any statistical function provided in the `statistics` module of
        the standard library.

        Parameters
        ----------
        stat_func : str
            Either `'sum'`, `'min'`, `'max'` or the name of the statistical function from the
            `statistics` module of the standard library.

        Returns
        -------
        int or float

        Raises
        ------
        ValueError
            If `stat_func` not found in the `statistics` module.
        StatisticsError
            If the ParamDict is empty.
        """
        self._check_for_calc_stat(stat_func)
        res = self._calc_stat_all(stat_func)

        return res

    def sum(self) -> ParamT:
        """Calculate the sum of parameter values.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.sum()
        118
        """
        return cast('ParamT', self._calc_stat('sum'))

    def min(self) -> ParamT:
        """Calculate the minimum of parameter values.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.min()
        3
        """
        return cast('ParamT', self._calc_stat('min'))

    def max(self) -> ParamT:
        """Calculate the maximum of parameter values.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.max()
        100
        """
        return cast('ParamT', self._calc_stat('max'))

    def mean(self) -> int | float:
        """Calculate the mean of parameter values.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.mean()
        29.5
        """
        return self._calc_stat('mean')

    def median(self) -> int | float:
        """Calculate the median of parameter values.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.median()
        7.5
        """
        return self._calc_stat('median')

    def median_high(self) -> ParamT:
        """Calculate the high median of parameter values.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.median_high()
        10
        """
        return cast('ParamT', self._calc_stat('median_high'))

    def median_low(self) -> ParamT:
        """Calculate the low median of parameter values.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.

        Examples
        --------
        >>> inventory = ParamDict1D({'chair': 100, 'table': 10, 'shelf': 5, 'sofa': 3})
        >>> inventory.median_low()
        5
        """
        return cast('ParamT', self._calc_stat('median_low'))


class ParamDictND(ParamDictBase[ElemNDT, ParamT], DictNDMixin[ElemNDT, ParamT]):
    """Custom subclass of `dict` to define parameters with N-dim tuple keys.

    Requires all keys to be unique tuples of the same length, each containing 'N' scalars (such as
    `int`, `str`, `pd.Timestamp`, etc.) and all values to be `int` or `float`.

    Parameters
    ----------
    mapping : dict or dict-like mapping, optional
        Input data to be encapsulated in the ParamDict.
    key_names : sequence[str], optional
        Names to refer to each dimension of N-dim tuple keys - not used internally but solely for
        user reference.
    value_name : str, optional
        Name to refer to parameter values - not used internally, and solely for user reference.

    Raises
    ------
    TypeError
        If input includes key(s) that are not tuples.
    ValueError
        If input includes tuple keys of different lengths.
    TypeError
        If input includes values that are not int or float.

    See Also
    --------
    ParamDict1D : For 1-dim scalar keys.

    Examples
    --------
    Constructing empty to populate later:

    >>> ParamDictND()
    ParamDictND:
    {}

    Constructing with a mapping:

    >>> ParamDictND(
    ...     {('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15},
    ...     key_names=('ORI', 'DES'),
    ...     value_name='DEMAND',
    ... )
    ParamDictND: (ORI, DES) -> DEMAND
    {('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15}
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSetND
    #     Index-set of N-dim tuple keys.

    __slots__ = ('_key_names', '_value_name')

    @overload
    def __init__(
        self,
        mapping: None = None,
        /,
        *,
        key_names: Sequence[str] | None = None,
        value_name: str | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        mapping: Mapping[ElemNDT, ParamT],
        /,
        *,
        key_names: Sequence[str] | None = None,
        value_name: str | None = None,
    ) -> None: ...

    def __init__(
        self,
        mapping: Mapping[ElemNDT, ParamT] | None = None,
        /,
        *,
        key_names: Sequence[str] | None = None,
        value_name: str | None = None,
    ) -> None:
        self.key_names = key_names
        self.value_name = value_name

        if mapping is None:
            mapping = {}
            self._indexset: IndexSetND[ElemNDT] = IndexSetND(names=self.key_names)
            """Index-set of N-dim tuple keys."""
        else:
            if not isinstance(mapping, abc.Mapping):
                raise TypeError('input should be a dict or dict-like mapping')
            try:
                self._indexset = IndexSetND(mapping, names=self.key_names)
            except Exception as exc:
                self._reraise_exc_from_indexset(exc, caller='IndexSetND')

        super().__init__(mapping, indexset=self._indexset)

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p: MinimalRepresentationPrinter, cycle: bool) -> None:
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(
        self: ParamDictND[tuple[Unpack[Ts]], ParamT], *key: Unpack[Ts]
    ) -> ParamT | Literal[0]:
        """Get the parameter value for the specified key, or zero if it is not found.

        Parameters
        ----------
        *key : key

        Returns
        -------
        int or float

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})
        >>> demand.lookup('A', 'B')
        10
        >>> demand.lookup('B', 'A')
        0
        """
        if any((isinstance(k, Iterable) and not isinstance(k, str)) for k in key):
            raise TypeError('lookup key must be scalars (no iterables except string)')
        if len(key) != self._indexset._tuplelen:
            raise ValueError('lookup key length must be the same as that of N-dim tuple keys')
        return self.get(key, 0)

    @classmethod
    def from_series(
        cls,
        series: pd.Series[ParamT],
        *,
        key_names: Sequence[str] | None = None,
        value_name: str | None = None,
    ) -> ParamDictND[tuple[Any, ...], ParamT]:
        """Create a ParamDictND from a MultiIndex pandas Series.

        Parameters
        ----------
        series : Series
            Input pandas Series with a MultiIndex whose tuples form keys and values form parameters.
        key_names : sequence of str, optional
            Dimension names for the parameter keys. If not provided, defaults to the Series'
            `index.names` (as strings) if set, or None.
        value_name : str, optional
            Name for the parameter values. If not provided, defaults to the Series' `name`
            (as str) if set, or None.

        Returns
        -------
        ParamDictND

        Raises
        ------
        ValueError
            If the Series is empty.
        ValueError
            If the Series index contains duplicate labels.
        TypeError
            If the Series does not have a MultiIndex (multi-level index).
        TypeError
            If the Series index contains non-scalar labels (any iterable except string).
        TypeError
            If the Series values are not int or float.

        See Also
        --------
        ParamDictND.from_dataframe : Create a ParamDictND from DataFrame columns.
        ParamDict1D.from_series : Create a ParamDict1D from a single-index Series.
        ParamDict1D.from_dataframe : Create a ParamDict1D from DataFrame columns.

        Examples
        --------
        >>> import pandas as pd
        >>> from opti_extensions import ParamDictND
        >>> mi = pd.MultiIndex.from_tuples(
        ...     [('Delhi', 'Seattle'), ('Delhi', 'Tokyo')],
        ...     names=['ORI', 'DES'],
        ... )
        >>> s = pd.Series([11303, 5836], index=mi, name='DIST')
        >>> ParamDictND.from_series(s)
        ParamDictND: (ORI, DES) -> DIST
        {('Delhi', 'Seattle'): 11303, ('Delhi', 'Tokyo'): 5836}
        >>> ParamDictND.from_series(s, key_names=['ORIGIN', 'DEST'], value_name='MILES')
        ParamDictND: (ORIGIN, DEST) -> MILES
        {('Delhi', 'Seattle'): 11303, ('Delhi', 'Tokyo'): 5836}
        """
        if series.empty:
            raise ValueError(f'{series.__class__.__name__} is empty')
        if getattr(series.index, 'nlevels', 1) <= 1:
            raise TypeError(
                'Single-level index is not supported by ParamDictND; use ParamDict1D.from_series'
            )
        if series.index.size > len(set(series.index)):
            raise ValueError(f'{series.__class__.__name__} has duplicate index-label(s)')
        if key_names is None:
            key_names = (
                None
                if any(x is None for x in series.index.names)
                else list(map(str, series.index.names))
            )
        if value_name is None and series.name is not None:
            value_name = str(series.name)
        return cls(
            cast(Mapping[tuple[Any, ...], ParamT], series.to_dict()),
            key_names=key_names,
            value_name=value_name,
        )

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        *,
        key_cols: Sequence[str],
        value_col: str,
        key_names: Sequence[str] | None = None,
        value_name: str | None = None,
    ) -> ParamDictND[tuple[Any, ...], int | float]:
        """Create a ParamDictND from key columns and a value column of a pandas DataFrame.

        Parameters
        ----------
        df : DataFrame
            Input pandas DataFrame.
        key_cols : sequence of str
            Names of columns to use for parameter key tuples.
        value_col : str
            Name of column to use for parameter values.
        key_names : sequence of str, optional
            Dimension names for the parameter keys. If not provided, defaults to `key_cols`.
        value_name : str, optional
            Name for the parameter values. If not provided, defaults to `value_col`.

        Returns
        -------
        ParamDictND

        Raises
        ------
        ValueError
            If the DataFrame is empty.
        ValueError
            If the combination of `key_cols` contains duplicate rows.
        KeyError
            If any column in `key_cols` or `value_col` is not found in DataFrame columns.
        TypeError
            If any column in `key_cols` contains non-scalar values (any iterable except string).
        TypeError
            If `value_col` contains values that are not int or float.

        See Also
        --------
        ParamDictND.from_series : Create a ParamDictND from a MultiIndex Series.
        ParamDict1D.from_dataframe : Create a ParamDict1D from DataFrame columns.
        ParamDict1D.from_series : Create a ParamDict1D from a pandas Series.

        Examples
        --------
        >>> import pandas as pd
        >>> from opti_extensions import ParamDictND
        >>> df = pd.DataFrame(
        ...     {
        ...         'ORI': ['Delhi', 'Seattle'],
        ...         'DES': ['Seattle', 'Tokyo'],
        ...         'DIST': [11303, 7695],
        ...     }
        ... )
        >>> ParamDictND.from_dataframe(df, key_cols=['ORI', 'DES'], value_col='DIST')
        ParamDictND: (ORI, DES) -> DIST
        {('Delhi', 'Seattle'): 11303, ('Seattle', 'Tokyo'): 7695}
        >>> ParamDictND.from_dataframe(
        ...     df,
        ...     key_cols=['ORI', 'DES'],
        ...     value_col='DIST',
        ...     key_names=['ORIGIN', 'DEST'],
        ...     value_name='MILES',
        ... )
        ParamDictND: (ORIGIN, DEST) -> MILES
        {('Delhi', 'Seattle'): 11303, ('Seattle', 'Tokyo'): 7695}
        """
        if df.empty:
            raise ValueError(f'{df.__class__.__name__} is empty')
        cols = list(key_cols)
        if len(cols) < 2:
            raise ValueError(
                '`key_cols` should contain at least two column names for ParamDictND; '
                'use ParamDict1D.from_dataframe for a single key column'
            )
        s = df.set_index(cols, drop=False)[value_col]
        k_names = key_names if key_names is not None else list(map(str, cols))
        v_name = value_name if value_name is not None else str(value_col)
        return cast(
            'ParamDictND[tuple[Any, ...], int | float]',
            cls.from_series(s, key_names=k_names, value_name=v_name),
        )

    def _calc_stat(self, *pattern: Any, stat_func: str) -> int | float:
        """Calculate a statistic with all parameter values or a subset based on wildcard pattern.

        Supports sum, min, max, and any statistical function provided in the `statistics` module of
        the standard library.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.
        stat_func : str
            Either `'sum'`, `'min'`, `'max'` or the name of the statistical function from the
            `statistics` module of the standard library.

        Returns
        -------
        int or float

        Raises
        ------
        ValueError
            If `stat_func` not found in the `statistics` module.
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.
        """
        self._check_for_calc_stat(stat_func)
        if stat_func in ('sum', 'min', 'max') and pattern:
            res: int | float = _builtin_op[stat_func](self.subset_values(*pattern))
        elif pattern:
            try:
                res = getattr(statistics, stat_func)(self.subset_values(*pattern))
            except statistics.StatisticsError:
                res = 0
        else:
            res = self._calc_stat_all(stat_func)

        return res

    # ---- sum overloads ----
    @overload
    def sum(self) -> ParamT: ...  # numpydoc ignore=GL08

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: _S1, __d2: Literal['*']
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: Literal['*'], __d2: _S2
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def sum(  # numpydoc ignore=GL08
        self,
        __d1: Any,
        __d2: Any,
        __d3: Any,
        __d4: Any,
        __d5: Any,
        *pattern: Any,
    ) -> ParamT | Literal[0]: ...

    def sum(self, *pattern: Any) -> ParamT | Literal[0]:
        """Calculate the sum of all parameter values or a subset based on wildcard pattern.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})

        Sum of all parameter values:

        >>> demand.sum()
        61

        Sum of a subset based on wildcard pattern:

        >>> demand.sum('A', '*')
        25
        >>> demand.sum('*', 'A')
        16
        """
        return cast('ParamT | Literal[0]', self._calc_stat(*pattern, stat_func='sum'))

    # ---- min overloads ----
    @overload
    def min(self) -> ParamT: ...  # numpydoc ignore=GL08

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: _S1, __d2: Literal['*']
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: Literal['*'], __d2: _S2
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def min(  # numpydoc ignore=GL08
        self,
        __d1: Any,
        __d2: Any,
        __d3: Any,
        __d4: Any,
        __d5: Any,
        *pattern: Any,
    ) -> ParamT | Literal[0]: ...

    def min(self, *pattern: Any) -> ParamT | Literal[0]:
        """Calculate the minimum of all parameter values or a subset based on wildcard pattern.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})

        Minimum of all parameter values:

        >>> demand.min()
        10

        Minimum of a subset based on wildcard pattern:

        >>> demand.min('A', '*')
        10
        >>> demand.min('*', 'A')
        16
        """
        return cast('ParamT | Literal[0]', self._calc_stat(*pattern, stat_func='min'))

    # ---- max overloads ----
    @overload
    def max(self) -> ParamT: ...  # numpydoc ignore=GL08

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: _S1, __d2: Literal['*']
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: Literal['*'], __d2: _S2
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def max(  # numpydoc ignore=GL08
        self,
        __d1: Any,
        __d2: Any,
        __d3: Any,
        __d4: Any,
        __d5: Any,
        *pattern: Any,
    ) -> ParamT | Literal[0]: ...

    def max(self, *pattern: Any) -> ParamT | Literal[0]:
        """Calculate the maximum of all parameter values or a subset based on wildcard pattern.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})

        Maximum of all parameter values:

        >>> demand.max()
        20

        Maximum of a subset based on wildcard pattern:

        >>> demand.max('A', '*')
        15
        >>> demand.max('*', 'A')
        16
        """
        return cast('ParamT | Literal[0]', self._calc_stat(*pattern, stat_func='max'))

    # ---- mean overloads ----
    @overload
    def mean(self) -> int | float: ...  # numpydoc ignore=GL08

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: _S1, __d2: Literal['*']
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: Literal['*'], __d2: _S2
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def mean(  # numpydoc ignore=GL08
        self,
        __d1: Any,
        __d2: Any,
        __d3: Any,
        __d4: Any,
        __d5: Any,
        *pattern: Any,
    ) -> int | float: ...

    def mean(self, *pattern: Any) -> int | float:
        """Calculate the mean of all parameter values or a subset based on wildcard pattern.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})

        Mean of all parameter values:

        >>> demand.mean()
        15.25

        Mean of a subset based on wildcard pattern:

        >>> demand.mean('A', '*')
        12.5
        >>> demand.mean('*', 'A')
        16
        """
        return self._calc_stat(*pattern, stat_func='mean')

    # ---- median overloads ----
    @overload
    def median(self) -> int | float: ...  # numpydoc ignore=GL08

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: _S1, __d2: Literal['*']
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: Literal['*'], __d2: _S2
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: _S4,
    ) -> int | float: ...

    @overload
    def median(  # numpydoc ignore=GL08
        self,
        __d1: Any,
        __d2: Any,
        __d3: Any,
        __d4: Any,
        __d5: Any,
        *pattern: Any,
    ) -> int | float: ...

    def median(self, *pattern: Any) -> int | float:
        """Calculate the median of all parameter values or a subset based on wildcard pattern.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})

        Median of all parameter values:

        >>> demand.median()
        15.5

        Median of a subset based on wildcard pattern:

        >>> demand.median('A', '*')
        12.5
        >>> demand.median('*', 'A')
        16
        """
        return self._calc_stat(*pattern, stat_func='median')

    # ---- median_high overloads ----
    @overload
    def median_high(self) -> ParamT: ...  # numpydoc ignore=GL08

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: _S1, __d2: Literal['*']
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: Literal['*'], __d2: _S2
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_high(  # numpydoc ignore=GL08
        self,
        __d1: Any,
        __d2: Any,
        __d3: Any,
        __d4: Any,
        __d5: Any,
        *pattern: Any,
    ) -> ParamT | Literal[0]: ...

    def median_high(self, *pattern: Any) -> ParamT | Literal[0]:
        """Calculate the high median of all parameter values or a subset based on wildcard pattern.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})

        High median of all parameter values:

        >>> demand.median_high()
        16

        High median of a subset based on wildcard pattern:

        >>> demand.median_high('A', '*')
        15
        >>> demand.median_high('*', 'A')
        16
        """
        return cast('ParamT | Literal[0]', self._calc_stat(*pattern, stat_func='median_high'))

    # ---- median_low overloads ----
    @overload
    def median_low(self) -> ParamT: ...  # numpydoc ignore=GL08

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: _S1, __d2: Literal['*']
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2], ParamT], __d1: Literal['*'], __d2: _S2
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: _S3,
        __d4: Literal['*'],
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: _S2,
        __d3: Literal['*'],
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: _S1,
        __d2: Literal['*'],
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self: ParamDictND[tuple[_S1, _S2, _S3, _S4], ParamT],
        __d1: Literal['*'],
        __d2: _S2,
        __d3: _S3,
        __d4: _S4,
    ) -> ParamT | Literal[0]: ...

    @overload
    def median_low(  # numpydoc ignore=GL08
        self,
        __d1: Any,
        __d2: Any,
        __d3: Any,
        __d4: Any,
        __d5: Any,
        *pattern: Any,
    ) -> ParamT | Literal[0]: ...

    def median_low(self, *pattern: Any) -> ParamT | Literal[0]:
        """Calculate the low median of all parameter values or a subset based on wildcard pattern.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        int or float

        Raises
        ------
        StatisticsError
            If the ParamDict is empty.
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        >>> demand = ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15, ('C', 'A'): 16})

        Low median of all parameter values:

        >>> demand.median_low()
        15

        Low median of a subset based on wildcard pattern:

        >>> demand.median_low('A', '*')
        10
        >>> demand.median_low('*', 'A')
        16
        """
        return cast('ParamT | Literal[0]', self._calc_stat(*pattern, stat_func='median_low'))
