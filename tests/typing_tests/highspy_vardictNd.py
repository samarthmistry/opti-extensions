# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

import pandas as pd
from highspy import Highs, HighsVarType
from highspy.highs import highs_linear_expression, highs_var
from typing_extensions import assert_type

from opti_extensions import IndexSetND, ParamDictND
from opti_extensions.highspy import VarDictND, addVariables


class Color(Enum):
    RED = 1
    BLUE = 2


mdl = Highs()

rng = range(3)
str_ = ['A', 'B', 'C']
dt = [date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]
dttm = [datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]
ts = pd.date_range('2024-01-01', '2024-03-01', freq='MS')
_2d = IndexSetND(rng, rng)
_3d = IndexSetND(rng, rng, rng)

# 2
assert_type(
    addVariables(mdl, IndexSetND((i, i) for i in rng), type=HighsVarType.kContinuous),
    VarDictND[tuple[int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(str_, ts), type=HighsVarType.kContinuous),
    VarDictND[tuple[str, pd.Timestamp], highs_var],
)

# 3
assert_type(
    addVariables(mdl, IndexSetND((i, i, i) for i in rng), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_2d, ts), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, pd.Timestamp], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(dt, _2d), type=HighsVarType.kInteger),
    VarDictND[tuple[date, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(rng, str_, ts), type=HighsVarType.kInteger),
    VarDictND[tuple[int, str, pd.Timestamp], highs_var],
)

# 4
assert_type(
    addVariables(mdl, IndexSetND((i, i, i, i) for i in rng), type=HighsVarType.kContinuous),
    VarDictND[tuple[int, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_3d, dt), type=HighsVarType.kContinuous),
    VarDictND[tuple[int, int, int, date], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_2d, _2d), type=HighsVarType.kContinuous),
    VarDictND[tuple[int, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_2d, dttm, ts), type=HighsVarType.kContinuous),
    VarDictND[tuple[int, int, datetime, pd.Timestamp], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(dt, _3d), type=HighsVarType.kContinuous),
    VarDictND[tuple[date, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(dttm, _2d, ts), type=HighsVarType.kContinuous),
    VarDictND[tuple[datetime, int, int, pd.Timestamp], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(rng, str_, dttm, ts), type=HighsVarType.kContinuous),
    VarDictND[tuple[int, str, datetime, pd.Timestamp], highs_var],
)

# 5
assert_type(
    addVariables(mdl, IndexSetND((i, i, i, i, i) for i in rng), lb=1, type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(rng, str_, dt, dttm, ts), lb=1, type=HighsVarType.kInteger),
    VarDictND[tuple[int, str, date, datetime, pd.Timestamp], highs_var],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(
    addVariables(mdl, IndexSetND([1.5], [Color.RED]), type=HighsVarType.kContinuous),
    VarDictND[tuple[float, Color], highs_var],
)
u1, u2 = uuid4(), uuid4()
assert_type(
    addVariables(mdl, IndexSetND([u1], ['A']), type=HighsVarType.kInteger),
    VarDictND[tuple[UUID, str], highs_var],
)

# Positive checks: Mapping assignability
v_2d = addVariables(mdl, IndexSetND(['A', 'B'], [1, 2]), type=HighsVarType.kContinuous)
m_vnd: Mapping[tuple[str, int], highs_var] = v_2d

# Positive checks: Exact arity lookup
assert_type(v_2d.lookup('A', 1), highs_var | Literal[0])

# Positive checks: Subset keys and values
assert_type(v_2d.subset_keys('*', 1), list[tuple[str, int]])
assert_type(v_2d.subset_keys('A', '*'), list[tuple[str, int]])
assert_type(v_2d.subset_values('*', 1), list[highs_var])
assert_type(v_2d.subset_values('A', '*'), list[highs_var])

# Positive checks: Sum (full and wildcard)
assert_type(v_2d.sum(), highs_linear_expression)
assert_type(v_2d.sum('*', 1), highs_linear_expression)

# Positive checks: Dot product / @
p_2d = ParamDictND({('A', 1): 1, ('B', 2): 2})
assert_type(v_2d.dot(p_2d), highs_linear_expression)
assert_type(v_2d @ p_2d, highs_linear_expression)
assert_type(p_2d @ v_2d, highs_linear_expression)

# Negative checks: Direct instantiation blocked
VarDictND()  # type: ignore[call-overload]

# Negative checks: Unsupported mutating methods blocked
v_2d.clear()  # type: ignore[call-overload]
v_2d.update({})  # type: ignore[call-overload]
v_2d.copy()  # type: ignore[call-overload]
v_2d.pop(('A', 1))  # type: ignore[call-overload]
v_2d.popitem()  # type: ignore[call-overload]
v_2d.setdefault(('A', 1), v_2d['A', 1])  # type: ignore[call-overload]
VarDictND.fromkeys([('A', 1)])  # type: ignore[deprecated,call-overload]
v_2d['A', 1] = v_2d['A', 1]  # type: ignore[call-overload]
del v_2d['A', 1]  # type: ignore[call-overload]
v_2d |= {}  # type: ignore[deprecated,arg-type]
_ = v_2d | {}  # type: ignore[deprecated]
_ = {} | v_2d  # type: ignore[deprecated]

# Negative checks: Wrong arity lookup
v_2d.lookup('A')  # type: ignore[call-arg]
v_2d.lookup('A', 1, 2)  # type: ignore[call-arg]

# Negative checks: Invalid wildcard patterns
v_2d_int = addVariables(mdl, IndexSetND([1, 2], [3, 4]), type=HighsVarType.kContinuous)
v_2d_int.subset_keys('*', '*')  # type: ignore[call-overload]
v_2d.subset_keys('A', 1)  # type: ignore[call-overload]
v_2d.subset_keys('A')  # type: ignore[call-overload]
v_2d.subset_values('A', 1)  # type: ignore[call-overload]
v_2d.sum('A', 1)  # type: ignore[call-overload]

# Negative checks: sum_squares not supported in highspy
v_2d.sum_squares()  # type: ignore[call-overload]
