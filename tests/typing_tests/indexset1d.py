# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import MutableSequence, Sequence
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import IndexSet1D


class Color(Enum):
    RED = 1
    BLUE = 2


# Positive checks: Builtin whitelisted types
assert_type(IndexSet1D(range(3)), IndexSet1D[int])
assert_type(IndexSet1D([0, 1, 2]), IndexSet1D[int])
assert_type(IndexSet1D(['A', 'B', 'C']), IndexSet1D[str])
assert_type(IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]), IndexSet1D[date])
assert_type(
    IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
    IndexSet1D[datetime],
)
assert_type(
    IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')), IndexSet1D[pd.Timestamp]
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(IndexSet1D([1.5, 2.5]), IndexSet1D[float])
assert_type(IndexSet1D([Color.RED, Color.BLUE]), IndexSet1D[Color])
u1, u2 = uuid4(), uuid4()
assert_type(IndexSet1D([u1, u2]), IndexSet1D[UUID])

# Positive checks: 0-arg constructor with target annotation
s_empty: IndexSet1D[str] = IndexSet1D()
assert_type(s_empty, IndexSet1D[str])

# Positive checks: MutableSequence / Sequence assignability
s_str = IndexSet1D(['A', 'B', 'C'])
seq: Sequence[str] = s_str
mut_seq: MutableSequence[str] = s_str

# Positive checks: count, pop, and __contains__ with object
assert_type(s_str.count('A'), int)
assert_type(s_str.count(123), int)
assert_type(s_str.pop(), str)
assert_type(s_str.pop(0), str)
val_obj: object = 'A'
if val_obj in s_str:
    pass

# Positive checks: Concatenation and set operations widening
s_int = IndexSet1D([1, 2])
assert_type(s_str + s_int, IndexSet1D[str | int])
assert_type(s_str + [1.5], IndexSet1D[str | float])
assert_type(s_str | s_int, IndexSet1D[str | int])
assert_type(s_str.union(s_int), IndexSet1D[str | int])
assert_type(s_str.intersection([1, 2]), IndexSet1D[str])
assert_type(s_str.difference([1, 2]), IndexSet1D[str])
assert_type(s_str.isdisjoint([1, 2]), bool)

# Negative checks
IndexSet1D([[1, 2]])  # type: ignore[type-var]
s_typed: IndexSet1D[str] = IndexSet1D(['A', 'B'])
bad_list: list[int] = [123]
s_typed += bad_list  # type: ignore[arg-type]
