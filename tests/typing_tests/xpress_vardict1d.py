# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

import pandas as pd
import xpress as xp
from typing_extensions import assert_type

from opti_extensions import IndexSet1D, ParamDict1D
from opti_extensions.xpress import VarDict1D, addVariables


class Color(Enum):
    RED = 1
    BLUE = 2


prob = xp.problem()

# Builtin types
assert_type(
    addVariables(prob, IndexSet1D(range(3)), vartype=xp.continuous),
    VarDict1D[int, xp.var],
)
assert_type(
    addVariables(prob, IndexSet1D([0, 1, 2]), vartype=xp.continuous),
    VarDict1D[int, xp.var],
)
assert_type(
    addVariables(prob, IndexSet1D(['A', 'B', 'C']), vartype=xp.binary),
    VarDict1D[str, xp.var],
)
assert_type(
    addVariables(
        prob, IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]), vartype=xp.integer
    ),
    VarDict1D[date, xp.var],
)
assert_type(
    addVariables(
        prob,
        IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
        lb=1,
        vartype=xp.semicontinuous,
    ),
    VarDict1D[datetime, xp.var],
)
assert_type(
    addVariables(
        prob,
        IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')),
        lb=1,
        vartype=xp.semiinteger,
    ),
    VarDict1D[pd.Timestamp, xp.var],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(
    addVariables(prob, IndexSet1D([1.5, 2.5]), vartype=xp.continuous),
    VarDict1D[float, xp.var],
)
assert_type(
    addVariables(prob, IndexSet1D([Color.RED, Color.BLUE]), vartype=xp.binary),
    VarDict1D[Color, xp.var],
)
u1, u2 = uuid4(), uuid4()
assert_type(
    addVariables(prob, IndexSet1D([u1, u2]), vartype=xp.integer),
    VarDict1D[UUID, xp.var],
)

# Positive checks: Mapping assignability
v_str = addVariables(prob, IndexSet1D(['A', 'B']), vartype=xp.continuous)
m_v: Mapping[str, xp.var] = v_str

# Positive checks: Dot product / @
p_str = ParamDict1D({'A': 1, 'B': 2})
assert_type(v_str.dot(p_str), xp.expression)
assert_type(v_str @ p_str, xp.expression)
assert_type(p_str @ v_str, xp.expression)

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
