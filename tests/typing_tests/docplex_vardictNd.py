# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

import pandas as pd
from docplex.mp.dvar import Var
from docplex.mp.linear import LinearExpr, ZeroExpr
from docplex.mp.model import Model
from docplex.mp.quad import QuadExpr
from typing_extensions import assert_type

from opti_extensions import IndexSetND, ParamDictND
from opti_extensions.docplex import VarDictND, add_variables


class Color(Enum):
    RED = 1
    BLUE = 2


mdl = Model()

rng = range(3)
str_ = ['A', 'B', 'C']
dt = [date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]
dttm = [datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]
ts = pd.date_range('2024-01-01', '2024-03-01', freq='MS')
_2d = IndexSetND(rng, rng)
_3d = IndexSetND(rng, rng, rng)

# 2D
assert_type(
    add_variables(mdl, IndexSetND((i, i) for i in rng), 'C'), VarDictND[tuple[int, int], Var]
)
assert_type(add_variables(mdl, IndexSetND(str_, ts), 'C'), VarDictND[tuple[str, pd.Timestamp], Var])

# 3D
assert_type(
    add_variables(mdl, IndexSetND((i, i, i) for i in rng), 'B'),
    VarDictND[tuple[int, int, int], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(_2d, ts), 'B'), VarDictND[tuple[int, int, pd.Timestamp], Var]
)
assert_type(add_variables(mdl, IndexSetND(dt, _2d), 'B'), VarDictND[tuple[date, int, int], Var])
assert_type(
    add_variables(mdl, IndexSetND(rng, str_, ts), 'B'),
    VarDictND[tuple[int, str, pd.Timestamp], Var],
)

# 4D
assert_type(
    add_variables(mdl, IndexSetND((i, i, i, i) for i in rng), 'I'),
    VarDictND[tuple[int, int, int, int], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(_3d, dt), 'I'), VarDictND[tuple[int, int, int, date], Var]
)
assert_type(
    add_variables(mdl, IndexSetND(_2d, _2d), 'I'), VarDictND[tuple[int, int, int, int], Var]
)
assert_type(
    add_variables(mdl, IndexSetND(_2d, dttm, ts), 'I'),
    VarDictND[tuple[int, int, datetime, pd.Timestamp], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(dt, _3d), 'I'), VarDictND[tuple[date, int, int, int], Var]
)
assert_type(
    add_variables(mdl, IndexSetND(dttm, _2d, ts), 'I'),
    VarDictND[tuple[datetime, int, int, pd.Timestamp], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(rng, str_, dttm, ts), 'I'),
    VarDictND[tuple[int, str, datetime, pd.Timestamp], Var],
)

# 5D
assert_type(
    add_variables(mdl, IndexSetND((i, i, i, i, i) for i in rng), 'SC', lb=1),
    VarDictND[tuple[int, int, int, int, int], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(rng, str_, dt, dttm, ts), 'SI', lb=1),
    VarDictND[tuple[int, str, date, datetime, pd.Timestamp], Var],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(
    add_variables(mdl, IndexSetND([1.5], [Color.RED]), 'C'),
    VarDictND[tuple[float, Color], Var],
)
u1, u2 = uuid4(), uuid4()
assert_type(
    add_variables(mdl, IndexSetND([u1], ['A']), 'B'),
    VarDictND[tuple[UUID, str], Var],
)

# Positive checks: Mapping assignability
v_2d = add_variables(mdl, IndexSetND(['A', 'B'], [1, 2]), 'C')
m_vnd: Mapping[tuple[str, int], Var] = v_2d

# Positive checks: Exact arity lookup
assert_type(v_2d.lookup('A', 1), Var | Literal[0])

# Positive checks: Subset keys and values
assert_type(v_2d.subset_keys('*', 1), list[tuple[str, int]])
assert_type(v_2d.subset_keys('A', '*'), list[tuple[str, int]])
assert_type(v_2d.subset_values('*', 1), list[Var])
assert_type(v_2d.subset_values('A', '*'), list[Var])

# Positive checks: Sum and sum_squares (full and wildcard)
assert_type(v_2d.sum(), LinearExpr | ZeroExpr)
assert_type(v_2d.sum('*', 1), LinearExpr | ZeroExpr)
assert_type(v_2d.sum_squares(), QuadExpr | ZeroExpr)
assert_type(v_2d.sum_squares('*', 1), QuadExpr | ZeroExpr)

# Positive checks: Dot product / @
p_2d = ParamDictND({('A', 1): 1, ('B', 2): 2})
assert_type(v_2d.dot(p_2d), LinearExpr | ZeroExpr)
assert_type(v_2d @ p_2d, LinearExpr | ZeroExpr)
assert_type(p_2d @ v_2d, LinearExpr | ZeroExpr)

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
v_2d_int = add_variables(mdl, IndexSetND([1, 2], [3, 4]), 'C')
v_2d_int.subset_keys('*', '*')  # type: ignore[call-overload]
v_2d.subset_keys('A', 1)  # type: ignore[call-overload]
v_2d.subset_keys('A')  # type: ignore[call-overload]
v_2d.subset_values('A', 1)  # type: ignore[call-overload]
v_2d.sum('A', 1)  # type: ignore[call-overload]
v_2d.sum_squares('A', 1)  # type: ignore[call-overload]
