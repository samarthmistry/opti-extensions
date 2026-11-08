# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

import pandas as pd
from highspy import Highs, HighsVarType
from highspy.highs import highs_linear_expression, highs_var
from typing_extensions import assert_type

from opti_extensions import IndexSet1D, ParamDict1D
from opti_extensions.highspy import VarDict1D, addVariables


class Color(Enum):
    RED = 1
    BLUE = 2


mdl = Highs()

# Builtin types
assert_type(
    addVariables(mdl, IndexSet1D(range(3)), type=HighsVarType.kContinuous),
    VarDict1D[int, highs_var],
)
assert_type(
    addVariables(mdl, IndexSet1D([0, 1, 2]), type=HighsVarType.kContinuous),
    VarDict1D[int, highs_var],
)
assert_type(
    addVariables(mdl, IndexSet1D(['A', 'B', 'C']), type=HighsVarType.kInteger),
    VarDict1D[str, highs_var],
)
assert_type(
    addVariables(
        mdl,
        IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]),
        type=HighsVarType.kInteger,
    ),
    VarDict1D[date, highs_var],
)
assert_type(
    addVariables(
        mdl,
        IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
        lb=1,
        type=HighsVarType.kContinuous,
    ),
    VarDict1D[datetime, highs_var],
)
assert_type(
    addVariables(
        mdl,
        IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')),
        lb=1,
        type=HighsVarType.kInteger,
    ),
    VarDict1D[pd.Timestamp, highs_var],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(
    addVariables(mdl, IndexSet1D([1.5, 2.5]), type=HighsVarType.kContinuous),
    VarDict1D[float, highs_var],
)
assert_type(
    addVariables(mdl, IndexSet1D([Color.RED, Color.BLUE]), type=HighsVarType.kInteger),
    VarDict1D[Color, highs_var],
)
u1, u2 = uuid4(), uuid4()
assert_type(
    addVariables(mdl, IndexSet1D([u1, u2]), type=HighsVarType.kInteger),
    VarDict1D[UUID, highs_var],
)

# Positive checks: Mapping assignability
v_str = addVariables(mdl, IndexSet1D(['A', 'B']), type=HighsVarType.kContinuous)
m_v: Mapping[str, highs_var] = v_str

# Positive checks: Dot product / @
p_str = ParamDict1D({'A': 1, 'B': 2})
assert_type(v_str.dot(p_str), highs_linear_expression)
assert_type(v_str @ p_str, highs_linear_expression)
assert_type(p_str @ v_str, highs_linear_expression)

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

# Negative checks: sum_squares not supported in highspy
v_str.sum_squares()  # type: ignore[call-overload]
