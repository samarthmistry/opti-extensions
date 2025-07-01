# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Base class for VarDict data structures."""

from __future__ import annotations

from typing import Any, NoReturn, TypeVar, overload

from ._dict_mixins import DefaultT, DictBaseMixin
from ._index_sets import ElemT, IndexSetBase

VarT = TypeVar('VarT')
ModelT = TypeVar('ModelT')


class VarDictBase(dict[ElemT, VarT], DictBaseMixin[ElemT, VarT]):
    """Base class for custom subclasses of `dict` to define optimization model variables.

    Disables all mutable mapping operations.

    Parameters
    ----------
    var_dict : dict
        Dictionary of variable objects associated with the optimization model.
    indexset : IndexSetBase
        Keys of dictionary encapsulated in an IndexSet.
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSetBase
    #     Index-set of keys.

    __slots__ = ('_indexset',)

    def __init__(self, var_dict: dict[ElemT, VarT], indexset: IndexSetBase[ElemT]) -> None:
        if indexset._set != set(var_dict.keys()):
            raise ValueError(
                f'{indexset.__class__.__name__} elements and {self.__class__.__name__} keys are not'
                ' the same.'
            )

        self._indexset = indexset
        """Index-set of keys."""

        super().__init__(var_dict)

    def __setitem__(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('__setitem__')

    def __delitem__(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('__delitem__')

    def clear(self) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('clear')

    def copy(self) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('copy')

    @overload
    def get(self, key: ElemT, default: None = ..., /) -> VarT | None: ...  # numpydoc ignore=GL08

    @overload
    def get(self, key: ElemT, default: VarT = ..., /) -> VarT: ...  # numpydoc ignore=GL08

    @overload
    def get(
        self, key: ElemT, default: DefaultT = ..., /
    ) -> VarT | DefaultT: ...  # numpydoc ignore=GL08

    def get(self, key: ElemT, default: DefaultT | None = None, /) -> VarT | DefaultT | None:
        """Get the variable for the specified key, or the default if not found.

        Parameters
        ----------
        key : key
        default : Any, optional

        Returns
        -------
        Var or ``default``
        """
        return super().get(key, default)

    def pop(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('pop')

    def popitem(self) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('popitem')

    def setdefault(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('setdefault')

    def update(self, *args: Any, **kwargs: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('update')

    @classmethod
    def fromkeys(cls, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        raise AttributeError(f'`fromkeys` is not supported by {cls.__name__}')
