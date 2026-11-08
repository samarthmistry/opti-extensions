# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from typing import Any

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND
from opti_extensions._pandas_accessors import DataFrameAccessor, IndexAccessor, SeriesAccessor

# Setup test objects
s_str: pd.Series[str] = pd.Series(['A', 'B', 'C'])
s_int: pd.Series[int] = pd.Series([1, 2, 3])
s_float: pd.Series[float] = pd.Series([1.5, 2.5, 3.5])
idx_str: pd.Index[str] = pd.Index(['A', 'B', 'C'])
multi_idx: pd.MultiIndex = pd.MultiIndex.from_tuples([('A', 1), ('B', 2)])
df: pd.DataFrame = pd.DataFrame({'k': ['A', 'B'], 'k2': [1, 2], 'v': [10, 20]})

# Positive checks: IndexSet1D / IndexSetND constructors
assert_type(IndexSet1D.from_series(s_str), IndexSet1D[str])
assert_type(IndexSet1D.from_series(s_int), IndexSet1D[int])
assert_type(IndexSet1D.from_index(idx_str), IndexSet1D[str])
assert_type(IndexSetND.from_dataframe(df), IndexSetND[tuple[Any, ...]])
assert_type(IndexSetND.from_index(multi_idx), IndexSetND[tuple[Any, ...]])

# Positive checks: ParamDict1D / ParamDictND constructors
assert_type(ParamDict1D.from_series(s_int), ParamDict1D[Any, int])
assert_type(ParamDict1D.from_series(s_float), ParamDict1D[Any, float])
assert_type(ParamDictND.from_series(s_int), ParamDictND[tuple[Any, ...], int])
assert_type(ParamDictND.from_series(s_float), ParamDictND[tuple[Any, ...], float])
assert_type(
    ParamDict1D.from_dataframe(df, key_col='k', value_col='v'),
    ParamDict1D[Any, int | float],
)
assert_type(
    ParamDictND.from_dataframe(df, key_cols=['k', 'k2'], value_col='v'),
    ParamDictND[tuple[Any, ...], int | float],
)

# Positive checks: Generic SeriesAccessor & IndexAccessor
sa_str: SeriesAccessor[str] = SeriesAccessor(s_str)
assert_type(sa_str.to_indexset(), IndexSet1D[str])
sa_float: SeriesAccessor[float] = SeriesAccessor(s_float)
assert_type(
    sa_float.to_paramdict(),
    ParamDict1D[Any, float] | ParamDictND[tuple[Any, ...], float],
)

ia_str: IndexAccessor[str] = IndexAccessor(idx_str)
assert_type(ia_str.to_indexset(), IndexSet1D[str])

ia_multi: IndexAccessor[tuple[Any, ...]] = IndexAccessor(multi_idx)
assert_type(ia_multi.to_indexset(), IndexSetND[tuple[Any, ...]])

df_acc: DataFrameAccessor = DataFrameAccessor(df)
assert_type(df_acc.to_indexset(), IndexSet1D[Any] | IndexSetND[tuple[Any, ...]])
assert_type(
    df_acc.to_paramdict(),
    ParamDict1D[Any, int | float] | ParamDictND[tuple[Any, ...], int | float],
)

# Negative checks: Wrong argument types
IndexSet1D.from_series(df)  # type: ignore[arg-type]
IndexSet1D.from_index(df)  # type: ignore[arg-type]
IndexSetND.from_dataframe(s_str)  # type: ignore[arg-type]
IndexSetND.from_dataframe(df, columns=123)  # type: ignore[arg-type]
ParamDict1D.from_dataframe(df, key_col=123, value_col='v')  # type: ignore[arg-type]
ParamDictND.from_dataframe(df, key_cols=123, value_col='v')  # type: ignore[arg-type]
