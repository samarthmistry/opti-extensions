# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping, MutableMapping
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import ParamDict1D


class Color(Enum):
    RED = 1
    BLUE = 2


# Builtin types
assert_type(ParamDict1D({'JAN': 31, 'FEB': 28, 'MAR': 31}), ParamDict1D[str, int])
assert_type(ParamDict1D({'A': 1.0, 'B': 2.0, 'C': 3.0}), ParamDict1D[str, float])

assert_type(ParamDict1D({1: 100, 2: 200, 3: 300}), ParamDict1D[int, int])
assert_type(ParamDict1D({1: 1.5, 2: 2.5, 3: 3.5}), ParamDict1D[int, float])

assert_type(
    ParamDict1D({date(2024, 1, 1): 31, date(2024, 2, 1): 28, date(2024, 3, 1): 31}),
    ParamDict1D[date, int],
)
assert_type(
    ParamDict1D({date(2024, 1, 1): 1.0, date(2024, 2, 1): 0.9, date(2024, 3, 1): 1.0}),
    ParamDict1D[date, float],
)

assert_type(
    ParamDict1D(
        {datetime(2024, 1, 1, 0): 31, datetime(2024, 2, 1, 1): 28, datetime(2024, 3, 1, 2): 31}
    ),
    ParamDict1D[datetime, int],
)
assert_type(
    ParamDict1D(
        {datetime(2024, 1, 1, 0): 1.0, datetime(2024, 2, 1, 1): 0.9, datetime(2024, 3, 1, 2): 1.0}
    ),
    ParamDict1D[datetime, float],
)

assert_type(
    ParamDict1D(
        {
            pd.Timestamp('2024-01-01'): 31,
            pd.Timestamp('2024-02-01'): 28,
            pd.Timestamp('2024-03-01'): 31,
        }
    ),
    ParamDict1D[pd.Timestamp, int],
)
assert_type(
    ParamDict1D(
        {
            pd.Timestamp('2024-01-01'): 1.0,
            pd.Timestamp('2024-02-01'): 0.9,
            pd.Timestamp('2024-03-01'): 1.0,
        }
    ),
    ParamDict1D[pd.Timestamp, float],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(ParamDict1D({Color.RED: 1.5, Color.BLUE: 2.5}), ParamDict1D[Color, float])
u1, u2 = uuid4(), uuid4()
assert_type(ParamDict1D({u1: 10, u2: 20}), ParamDict1D[UUID, int])

# Positive checks: 0-arg constructor with target annotation
p_empty: ParamDict1D[str, int] = ParamDict1D()
assert_type(p_empty, ParamDict1D[str, int])

# Positive checks: Covariant Mapping initialization
d_int: dict[str, int] = {'a': 1}
p_float: ParamDict1D[str, float] = ParamDict1D(d_int)
assert_type(p_float, ParamDict1D[str, float])

# Positive checks: Mapping / MutableMapping assignability
p_i = ParamDict1D({'A': 1, 'B': 2})
m_p: Mapping[str, int] = p_i
mut_m_p: MutableMapping[str, int] = p_i

# Positive checks: Supported dict methods
assert_type(p_i.pop('A'), int)
assert_type(p_i.popitem(), tuple[str, int])
assert_type(p_i.setdefault('C', 3), int)
p_i.clear()

# Positive checks: Value-type-preserving aggregations
p_num = ParamDict1D({'A': 1, 'B': 2})
assert_type(p_num.sum(), int)
assert_type(p_num.min(), int)
assert_type(p_num.max(), int)
assert_type(p_num.median_high(), int)
assert_type(p_num.median_low(), int)
assert_type(p_num.mean(), int | float)
assert_type(p_num.median(), int | float)

p_f = ParamDict1D({'A': 1.5, 'B': 2.5})
assert_type(p_f.sum(), float)
assert_type(p_f.min(), float)
assert_type(p_f.max(), float)

# Negative checks: Unsupported dict methods flagged with deprecated / call-overload / operator
p_num.copy()  # type: ignore[call-overload]
p_num.update({'A': 2})  # type: ignore[call-overload]
ParamDict1D.fromkeys(['A', 'B'])  # type: ignore[deprecated,call-overload]
p_num |= {'A': 2}  # type: ignore[deprecated,arg-type]
_ = p_num | {'A': 2}  # type: ignore[deprecated]
_ = {'A': 2} | p_num  # type: ignore[deprecated]
