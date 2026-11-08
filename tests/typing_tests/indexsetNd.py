# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from collections.abc import MutableSequence, Sequence
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import IndexSet1D, IndexSetND


class Color(Enum):
    RED = 1
    BLUE = 2


rng = range(3)
str_ = ['A', 'B', 'C']
dt = [date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]
dttm = [datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]
ts = pd.date_range('2024-01-01', '2024-03-01', freq='MS')
_2d = IndexSetND(rng, rng)
_3d = IndexSetND(rng, rng, rng)

# 2D Cartesian products
assert_type(IndexSetND((i, i) for i in rng), IndexSetND[tuple[int, int]])
assert_type(IndexSetND(str_, ts), IndexSetND[tuple[str, pd.Timestamp]])

# 3D Cartesian products
assert_type(IndexSetND((i, i, i) for i in rng), IndexSetND[tuple[int, int, int]])
assert_type(IndexSetND(_2d, ts), IndexSetND[tuple[int, int, pd.Timestamp]])
assert_type(IndexSetND(dt, _2d), IndexSetND[tuple[date, int, int]])
assert_type(IndexSetND(rng, str_, ts), IndexSetND[tuple[int, str, pd.Timestamp]])

# 4D Cartesian products
assert_type(IndexSetND((i, i, i, i) for i in rng), IndexSetND[tuple[int, int, int, int]])
assert_type(IndexSetND(_3d, dt), IndexSetND[tuple[int, int, int, date]])
assert_type(IndexSetND(_2d, _2d), IndexSetND[tuple[int, int, int, int]])
assert_type(IndexSetND(_2d, dttm, ts), IndexSetND[tuple[int, int, datetime, pd.Timestamp]])
assert_type(IndexSetND(dt, _3d), IndexSetND[tuple[date, int, int, int]])
assert_type(IndexSetND(dttm, _2d, ts), IndexSetND[tuple[datetime, int, int, pd.Timestamp]])
assert_type(IndexSetND(rng, str_, dttm, ts), IndexSetND[tuple[int, str, datetime, pd.Timestamp]])

# 5D Cartesian products
assert_type(IndexSetND((i, i, i, i, i) for i in rng), IndexSetND[tuple[int, int, int, int, int]])
assert_type(
    IndexSetND(rng, str_, dt, dttm, ts), IndexSetND[tuple[int, str, date, datetime, pd.Timestamp]]
)

# Positive checks: Non-whitelisted scalars (Enum, float, UUID)
assert_type(IndexSetND([1.5], [Color.RED]), IndexSetND[tuple[float, Color]])
u1, u2 = uuid4(), uuid4()
assert_type(IndexSetND([Color.RED], [u1]), IndexSetND[tuple[Color, UUID]])

# Positive checks: 0-arg constructor with target annotation
arcs: IndexSetND[tuple[str, int]] = IndexSetND()
assert_type(arcs, IndexSetND[tuple[str, int]])

# Positive checks: MutableSequence / Sequence assignability
seq_nd: Sequence[tuple[str, int]] = arcs
mut_seq_nd: MutableSequence[tuple[str, int]] = arcs

# Positive checks: count, pop, and __contains__ with object
assert_type(arcs.count(('A', 1)), int)
assert_type(arcs.count(123), int)
assert_type(arcs.pop(), tuple[str, int])
assert_type(arcs.pop(0), tuple[str, int])
val_nd: object = ('A', 1)
if val_nd in arcs:
    pass

# Positive checks: Concatenation and set operations
assert_type(arcs + arcs, IndexSetND[tuple[str, int]])
assert_type(arcs + [('B', 2)], IndexSetND[tuple[str, int]])
assert_type(arcs.intersection([('A', 1)]), IndexSetND[tuple[str, int]])
assert_type(arcs.difference([('A', 1)]), IndexSetND[tuple[str, int]])
assert_type(arcs.isdisjoint([('A', 1)]), bool)

# Positive checks: Arity-typed __le__
s_2d_typed = IndexSetND(['A', 'B'], [1, 2])
assert_type(s_2d_typed <= s_2d_typed, bool)
assert_type(s_2d_typed <= (IndexSet1D(['A']), IndexSet1D([1])), bool)

# Positive checks: Squeeze with Literal dimension indices
assert_type(s_2d_typed.squeeze(0), IndexSet1D[str])
assert_type(s_2d_typed.squeeze(1), IndexSet1D[int])
s_3d_typed = IndexSetND(['A'], [1], [1.5])
assert_type(s_3d_typed.squeeze(0), IndexSet1D[str])
assert_type(s_3d_typed.squeeze(1), IndexSet1D[int])
assert_type(s_3d_typed.squeeze(2), IndexSet1D[float])
assert_type(s_3d_typed.squeeze(0, 1), IndexSetND[tuple[str, int]])
assert_type(s_3d_typed.squeeze(0, 2), IndexSetND[tuple[str, float]])
assert_type(s_3d_typed.squeeze(1, 2), IndexSetND[tuple[int, float]])

# Positive checks: Subset with Literal['*'] wildcards
assert_type(s_2d_typed.subset('*', 1), list[tuple[str, int]])
assert_type(s_2d_typed.subset('A', '*'), list[tuple[str, int]])
assert_type(s_3d_typed.subset('*', 1, 1.5), list[tuple[str, int, float]])
assert_type(s_3d_typed.subset('A', '*', 1.5), list[tuple[str, int, float]])
assert_type(s_3d_typed.subset('A', 1, '*'), list[tuple[str, int, float]])

# Negative checks: Cross-arity union
s_2d_typed.union(s_3d_typed)  # type: ignore[arg-type]
s_2d_typed | s_3d_typed  # type: ignore[operator]

# Negative checks: Heap-polluting +=
bad_nd: list[tuple[str, str]] = [('A', 'B')]
s_2d_typed += bad_nd  # type: ignore[arg-type]

# Negative checks: Invalid wildcard patterns
s_2d_int = IndexSetND([1, 2], [3, 4])
s_2d_int.subset('*', '*')  # type: ignore[call-overload]
s_2d_typed.subset('A', 1)  # type: ignore[call-overload]
s_2d_typed.subset('A')  # type: ignore[call-overload]
s_2d_typed.subset('A', 'wrong')  # type: ignore[call-overload]

# Negative checks: Wrong arity on <=
_ = s_2d_typed <= (IndexSet1D(['A']),)  # type: ignore[operator]
