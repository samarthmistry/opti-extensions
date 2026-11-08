# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

import pandas as pd
import xpress as xp
from typing_extensions import assert_type

from opti_extensions import IndexSetND, ParamDictND
from opti_extensions.xpress import VarDictND, addVariables


class Color(Enum):
    RED = 1
    BLUE = 2


prob = xp.problem()

rng = range(3)
str_ = ['A', 'B', 'C']
dt = [date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]
dttm = [datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]
ts = pd.date_range('2024-01-01', '2024-03-01', freq='MS')
_2d = IndexSetND(rng, rng)
_3d = IndexSetND(rng, rng, rng)

# 2
assert_type(
    addVariables(prob, IndexSetND((i, i) for i in rng), vartype=xp.continuous),
    VarDictND[tuple[int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(str_, ts), vartype=xp.continuous),
    VarDictND[tuple[str, pd.Timestamp], xp.var],
)

# 3
assert_type(
    addVariables(prob, IndexSetND((i, i, i) for i in rng), vartype=xp.binary),
    VarDictND[tuple[int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_2d, ts), vartype=xp.binary),
    VarDictND[tuple[int, int, pd.Timestamp], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(dt, _2d), vartype=xp.binary),
    VarDictND[tuple[date, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(rng, str_, ts), vartype=xp.binary),
    VarDictND[tuple[int, str, pd.Timestamp], xp.var],
)

# 4
assert_type(
    addVariables(prob, IndexSetND((i, i, i, i) for i in rng), vartype=xp.integer),
    VarDictND[tuple[int, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_3d, dt), vartype=xp.integer),
    VarDictND[tuple[int, int, int, date], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_2d, _2d), vartype=xp.integer),
    VarDictND[tuple[int, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_2d, dttm, ts), vartype=xp.integer),
    VarDictND[tuple[int, int, datetime, pd.Timestamp], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(dt, _3d), vartype=xp.integer),
    VarDictND[tuple[date, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(dttm, _2d, ts), vartype=xp.integer),
    VarDictND[tuple[datetime, int, int, pd.Timestamp], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(rng, str_, dttm, ts), vartype=xp.integer),
    VarDictND[tuple[int, str, datetime, pd.Timestamp], xp.var],
)

# 5
assert_type(
    addVariables(prob, IndexSetND((i, i, i, i, i) for i in rng), lb=1, vartype=xp.semicontinuous),
    VarDictND[tuple[int, int, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(rng, str_, dt, dttm, ts), lb=1, vartype=xp.semiinteger),
    VarDictND[tuple[int, str, date, datetime, pd.Timestamp], xp.var],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(
    addVariables(prob, IndexSetND([1.5], [Color.RED]), vartype=xp.continuous),
    VarDictND[tuple[float, Color], xp.var],
)
u1, u2 = uuid4(), uuid4()
assert_type(
    addVariables(prob, IndexSetND([u1], ['A']), vartype=xp.integer),
    VarDictND[tuple[UUID, str], xp.var],
)

# Positive checks: Mapping assignability
v_2d = addVariables(prob, IndexSetND(['A', 'B'], [1, 2]), vartype=xp.continuous)
m_vnd: Mapping[tuple[str, int], xp.var] = v_2d

# Positive checks: Exact arity lookup
assert_type(v_2d.lookup('A', 1), xp.var | Literal[0])

# Positive checks: Subset keys and values
assert_type(v_2d.subset_keys('*', 1), list[tuple[str, int]])
assert_type(v_2d.subset_keys('A', '*'), list[tuple[str, int]])
assert_type(v_2d.subset_values('*', 1), list[xp.var])
assert_type(v_2d.subset_values('A', '*'), list[xp.var])

# Positive checks: Sum and sum_squares (full and wildcard)
assert_type(v_2d.sum(), xp.expression)
assert_type(v_2d.sum('*', 1), xp.expression)
assert_type(v_2d.sum_squares(), xp.expression)
assert_type(v_2d.sum_squares('*', 1), xp.expression)

# Positive checks: Dot product / @
p_2d = ParamDictND({('A', 1): 1, ('B', 2): 2})
assert_type(v_2d.dot(p_2d), xp.expression)
assert_type(v_2d @ p_2d, xp.expression)
assert_type(p_2d @ v_2d, xp.expression)

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
v_2d_int = addVariables(prob, IndexSetND([1, 2], [3, 4]), vartype=xp.continuous)
v_2d_int.subset_keys('*', '*')  # type: ignore[call-overload]
v_2d.subset_keys('A', 1)  # type: ignore[call-overload]
v_2d.subset_keys('A')  # type: ignore[call-overload]
v_2d.subset_values('A', 1)  # type: ignore[call-overload]
v_2d.sum('A', 1)  # type: ignore[call-overload]
v_2d.sum_squares('A', 1)  # type: ignore[call-overload]
