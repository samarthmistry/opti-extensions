# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Base class for VarDict data structures."""

from __future__ import annotations

from typing import Any, TypeVar, overload

from typing_extensions import Never, Self, deprecated

from ._dict_mixins import DefaultT, DictBaseMixin
from ._index_sets import Elem1DT, ElemNDT, ElemT, IndexSetBase, IndexSetND
from ._param_dicts import ParamDict1D, ParamDictND, ParamT

VarT = TypeVar('VarT')
ModelT = TypeVar('ModelT')


def _validate_for_dot_1d(paramdict: ParamDict1D[Elem1DT, ParamT]) -> None:
    """Validate ParamDict for dot product with VarDict1D.

    Parameters
    ----------
    paramdict : ParamDict1D
        ParamDict1D to be used for dot product.

    Raises
    ------
    TypeError
        If the paramdict is not as instance of ParamDict1D.
    """
    if not isinstance(paramdict, ParamDict1D):
        raise TypeError('Dot product only allowed with ParamDict1D')


def _validate_for_dot_Nd(
    indexset: IndexSetND[ElemNDT], paramdict: ParamDictND[ElemNDT, ParamT]
) -> None:
    """Validate ParamDict for dot product with VarDictND.

    Parameters
    ----------
    indexset : IndexSetND
        Index-set of keys of VarDictND.
    paramdict : ParamDictND
        ParamDictND to be used for dot product.

    Raises
    ------
    TypeError
        If the paramdict is not as instance of ParamDictND.
    ValueError
        If the paramdict does not have tuple keys of same length as VarDictND.
    """
    if not isinstance(paramdict, ParamDictND):
        raise TypeError(
            'Dot product only allowed with ParamDictND (having tuple keys of same length as '
            'VarDictND)'
        )
    elif paramdict._indexset._tuplelen != indexset._tuplelen:
        raise ValueError('ParamDictND should have tuple keys of same length as VarDictND')


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

    @overload  # type: ignore[override]
    @deprecated('`__setitem__` is not supported by VarDict.', category=None)
    def __setitem__(self, __k: Never, __v: Never, /) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`__setitem__` is not supported by VarDict.', category=None)
    def __setitem__(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`__setitem__` is not supported by VarDict.', category=None)
    def __setitem__(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        self._raise_not_supported_err('__setitem__')

    @overload  # type: ignore[override]
    @deprecated('`__delitem__` is not supported by VarDict.', category=None)
    def __delitem__(self, __k: Never, /) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`__delitem__` is not supported by VarDict.', category=None)
    def __delitem__(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`__delitem__` is not supported by VarDict.', category=None)
    def __delitem__(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        self._raise_not_supported_err('__delitem__')

    @overload  # type: ignore[override]
    @deprecated('`clear` is not supported by VarDict.', category=None)
    def clear(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`clear` is not supported by VarDict.', category=None)
    def clear(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`clear` is not supported by VarDict.', category=None)
    def clear(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        self._raise_not_supported_err('clear')

    @overload  # type: ignore[override]
    @deprecated('`copy` is not supported by VarDict.', category=None)
    def copy(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`copy` is not supported by VarDict.', category=None)
    def copy(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`copy` is not supported by VarDict.', category=None)
    def copy(self, *args: Any, **kwargs: Any) -> None:
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

    @overload  # type: ignore[override]
    @deprecated('`pop` is not supported by VarDict.', category=None)
    def pop(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`pop` is not supported by VarDict.', category=None)
    def pop(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`pop` is not supported by VarDict.', category=None)
    def pop(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        self._raise_not_supported_err('pop')

    @overload  # type: ignore[override]
    @deprecated('`popitem` is not supported by VarDict.', category=None)
    def popitem(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`popitem` is not supported by VarDict.', category=None)
    def popitem(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`popitem` is not supported by VarDict.', category=None)
    def popitem(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        self._raise_not_supported_err('popitem')

    @overload  # type: ignore[override]
    @deprecated('`setdefault` is not supported by VarDict.', category=None)
    def setdefault(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`setdefault` is not supported by VarDict.', category=None)
    def setdefault(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`setdefault` is not supported by VarDict.', category=None)
    def setdefault(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        self._raise_not_supported_err('setdefault')

    @overload  # type: ignore[override]
    @deprecated('`update` is not supported by VarDict.', category=None)
    def update(self, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @deprecated('`update` is not supported by VarDict.', category=None)
    def update(
        self, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @deprecated('`update` is not supported by VarDict.', category=None)
    def update(self, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        self._raise_not_supported_err('update')

    @overload  # type: ignore[override]
    @classmethod
    @deprecated('`fromkeys` is not supported by VarDict.', category=None)
    def fromkeys(cls, __disallow: Never) -> None: ...  # numpydoc ignore=GL08

    @overload
    @classmethod
    @deprecated('`fromkeys` is not supported by VarDict.', category=None)
    def fromkeys(
        cls, __d1: Never, __d2: Never, *args: Never, **kwargs: Never
    ) -> None: ...  # numpydoc ignore=GL08

    @classmethod
    @deprecated('`fromkeys` is not supported by VarDict.', category=None)
    def fromkeys(cls, *args: Any, **kwargs: Any) -> None:
        """Not supported by VarDict."""
        raise AttributeError(f'`fromkeys` is not supported by {cls.__name__}')

    @deprecated('`|` is not supported by VarDict.', category=None)
    def __or__(self, other: Never, /) -> Self:  # type: ignore[override]
        raise TypeError(f'`|` is not supported by {self.__class__.__name__}')

    @deprecated('`|` is not supported by VarDict.', category=None)
    def __ror__(self, other: Never, /) -> Self:  # type: ignore[override]
        raise TypeError(f'`|` is not supported by {self.__class__.__name__}')

    @deprecated('`|=` is not supported by VarDict.', category=None)
    def __ior__(self, other: Never, /) -> Self:  # type: ignore[override]
        raise TypeError(f'`|=` is not supported by {self.__class__.__name__}')
