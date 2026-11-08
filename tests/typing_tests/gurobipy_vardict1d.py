# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

import pandas as pd
from gurobipy import GRB, LinExpr, Model, Var
from typing_extensions import assert_type

from opti_extensions import IndexSet1D, ParamDict1D
from opti_extensions.gurobipy import VarDict1D, addVars


class Color(Enum):
    RED = 1
    BLUE = 2


mdl = Model()

# Builtin types
assert_type(addVars(mdl, IndexSet1D(range(3)), vtype=GRB.CONTINUOUS), VarDict1D[int, Var])
assert_type(addVars(mdl, IndexSet1D([0, 1, 2]), vtype=GRB.CONTINUOUS), VarDict1D[int, Var])
assert_type(addVars(mdl, IndexSet1D(['A', 'B', 'C']), vtype=GRB.BINARY), VarDict1D[str, Var])
assert_type(
    addVars(
        mdl, IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]), vtype=GRB.INTEGER
    ),
    VarDict1D[date, Var],
)
assert_type(
    addVars(
        mdl,
        IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
        lb=1,
        vtype=GRB.SEMICONT,
    ),
    VarDict1D[datetime, Var],
)
assert_type(
    addVars(
        mdl,
        IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')),
        lb=1,
        vtype=GRB.SEMIINT,
    ),
    VarDict1D[pd.Timestamp, Var],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(addVars(mdl, IndexSet1D([1.5, 2.5]), vtype=GRB.CONTINUOUS), VarDict1D[float, Var])
assert_type(
    addVars(mdl, IndexSet1D([Color.RED, Color.BLUE]), vtype=GRB.BINARY), VarDict1D[Color, Var]
)
u1, u2 = uuid4(), uuid4()
assert_type(addVars(mdl, IndexSet1D([u1, u2]), vtype=GRB.INTEGER), VarDict1D[UUID, Var])

# Positive checks: Mapping assignability
v_str = addVars(mdl, IndexSet1D(['A', 'B']), vtype=GRB.CONTINUOUS)
m_v: Mapping[str, Var] = v_str

# Positive checks: Dot product / @
p_str = ParamDict1D({'A': 1, 'B': 2})
assert_type(v_str.dot(p_str), LinExpr)
assert_type(v_str @ p_str, LinExpr)
assert_type(p_str @ v_str, LinExpr)

# Negative checks: Direct instantiation blocked
VarDict1D()  # type: ignore[call-overload]

# Negative checks: Unsupported mutating methods blocked
v_str.clear()  # type: ignore[call-overload]
v_str.update({})  # type: ignore[call-overload]
v_str.copy()  # type: ignore[call-overload]
v_str.pop('A')  # type: ignore[call-overload]
v_str.popitem()  # type: ignore[call-overload]
v_str.setdefault('A', v_str['A'])  # type: ignore[call-overload]
VarDict1D.fromkeys(['A'])  # type: ignore[deprecated,call-overload]
v_str['A'] = v_str['A']  # type: ignore[call-overload]
del v_str['A']  # type: ignore[call-overload]
v_str |= {}  # type: ignore[deprecated,arg-type]
_ = v_str | {}  # type: ignore[deprecated]
_ = {} | v_str  # type: ignore[deprecated]
