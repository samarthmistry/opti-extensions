# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import Mapping, MutableMapping
from datetime import date, datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import ParamDictND


class Color(Enum):
    RED = 1
    BLUE = 2


assert_type(
    ParamDictND({('A', 'B'): 10, ('B', 'C'): 20, ('A', 'C'): 15}), ParamDictND[tuple[str, str], int]
)
assert_type(
    ParamDictND({('A', 'B'): 1.0, ('B', 'C'): 2.0, ('A', 'C'): 1.5}),
    ParamDictND[tuple[str, str], float],
)

assert_type(
    ParamDictND({('A', 1): 10, ('B', 1): 20, ('A', 2): 15}), ParamDictND[tuple[str, int], int]
)
assert_type(
    ParamDictND({('A', 1): 1.0, ('B', 1): 2.0, ('A', 2): 15}), ParamDictND[tuple[str, int], float]
)

assert_type(
    ParamDictND(
        {
            ('A', pd.Timestamp('2024-01-01')): 10,
            ('B', pd.Timestamp('2024-01-01')): 20,
            ('A', pd.Timestamp('2024-02-01')): 5,
        }
    ),
    ParamDictND[tuple[str, pd.Timestamp], int],
)
assert_type(
    ParamDictND(
        {
            ('A', pd.Timestamp('2024-01-01')): 1.0,
            ('B', pd.Timestamp('2024-01-01')): 2.0,
            ('A', pd.Timestamp('2024-02-01')): 0.5,
        }
    ),
    ParamDictND[tuple[str, pd.Timestamp], float],
)

assert_type(
    ParamDictND(
        {('A', date(2024, 1, 1)): 10, ('B', date(2024, 1, 1)): 20, ('A', date(2024, 2, 1)): 5}
    ),
    ParamDictND[tuple[str, date], int],
)
assert_type(
    ParamDictND(
        {('A', date(2024, 1, 1)): 1.0, ('B', date(2024, 1, 1)): 2.0, ('A', date(2024, 2, 1)): 0.5}
    ),
    ParamDictND[tuple[str, date], float],
)

assert_type(
    ParamDictND(
        {
            ('A', datetime(2024, 1, 1, 0)): 10,
            ('B', datetime(2024, 1, 1, 1)): 20,
            ('A', datetime(2024, 2, 1, 0)): 5,
        }
    ),
    ParamDictND[tuple[str, datetime], int],
)
assert_type(
    ParamDictND(
        {
            ('A', datetime(2024, 1, 1, 0)): 1.0,
            ('B', datetime(2024, 1, 1, 1)): 2.0,
            ('A', datetime(2024, 2, 1, 0)): 0.5,
        }
    ),
    ParamDictND[tuple[str, datetime], float],
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(ParamDictND({(Color.RED, 1.5): 10}), ParamDictND[tuple[Color, float], int])
u1, u2 = uuid4(), uuid4()
assert_type(ParamDictND({(u1, 'A'): 20}), ParamDictND[tuple[UUID, str], int])

# Positive checks: 0-arg constructor with target annotation
p_empty: ParamDictND[tuple[str, int], float] = ParamDictND()
assert_type(p_empty, ParamDictND[tuple[str, int], float])

# Positive checks: Covariant Mapping initialization
d_nd: dict[tuple[str, int], int] = {('A', 1): 10}
p_nd_float: ParamDictND[tuple[str, int], float] = ParamDictND(d_nd)
assert_type(p_nd_float, ParamDictND[tuple[str, int], float])

# Positive checks: Mapping / MutableMapping assignability
p_2d = ParamDictND({('A', 1): 10, ('B', 2): 20})
m_nd: Mapping[tuple[str, int], int] = p_2d
mut_m_nd: MutableMapping[tuple[str, int], int] = p_2d

# Positive checks: Supported dict methods
assert_type(p_2d.pop(('A', 1)), int)
assert_type(p_2d.popitem(), tuple[tuple[str, int], int])
assert_type(p_2d.setdefault(('C', 3), 30), int)
p_2d.clear()

# Positive checks: Exact arity lookup
p_num = ParamDictND({('A', 1): 10, ('B', 2): 20})
assert_type(p_num.lookup('A', 1), int | Literal[0])

# Positive checks: Subset keys and values
assert_type(p_num.subset_keys('*', 1), list[tuple[str, int]])
assert_type(p_num.subset_keys('A', '*'), list[tuple[str, int]])
assert_type(p_num.subset_values('*', 1), list[int])
assert_type(p_num.subset_values('A', '*'), list[int])

# Positive checks: Value-type-preserving aggregations (0-arg and wildcard)
assert_type(p_num.sum(), int)
assert_type(p_num.sum('*', 1), int | Literal[0])
assert_type(p_num.min(), int)
assert_type(p_num.min('A', '*'), int | Literal[0])
assert_type(p_num.max(), int)
assert_type(p_num.max('*', 1), int | Literal[0])
assert_type(p_num.mean(), int | float)
assert_type(p_num.mean('*', 1), int | float)
assert_type(p_num.median(), int | float)
assert_type(p_num.median_high(), int)
assert_type(p_num.median_low(), int)

# Negative checks: Unsupported dict methods flagged with deprecated / call-overload / operator
p_num.copy()  # type: ignore[call-overload]
p_num.update({('A', 1): 2})  # type: ignore[call-overload]
ParamDictND.fromkeys([('A', 1)])  # type: ignore[deprecated,call-overload]
p_num |= {('A', 1): 2}  # type: ignore[deprecated,arg-type]
_ = p_num | {('A', 1): 2}  # type: ignore[deprecated]
_ = {('A', 1): 2} | p_num  # type: ignore[deprecated]

# Negative checks: Wrong arity lookup
p_num.lookup('A')  # type: ignore[call-arg]
p_num.lookup('A', 1, 2)  # type: ignore[call-arg]

# Negative checks: Invalid wildcard patterns
p_2d_int = ParamDictND({(1, 2): 10})
p_2d_int.subset_keys('*', '*')  # type: ignore[call-overload]
p_num.subset_keys('A', 1)  # type: ignore[call-overload]
p_num.subset_keys('A')  # type: ignore[call-overload]
p_num.subset_values('A', 1)  # type: ignore[call-overload]
p_num.sum('A', 1)  # type: ignore[call-overload]
