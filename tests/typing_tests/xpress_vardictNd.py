# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
import xpress as xp
from typing_extensions import assert_type

from opti_extensions import IndexSetND
from opti_extensions.xpress import VarDictND, addVariables

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
    addVariables(prob, IndexSetND((i, i) for i in rng), vartype=xp.continuous, name=''),
    VarDictND[tuple[int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(str_, ts), vartype=xp.continuous, name=''),
    VarDictND[tuple[str, pd.Timestamp], xp.var],
)

# 3
assert_type(
    addVariables(prob, IndexSetND((i, i, i) for i in rng), vartype=xp.binary, name=''),
    VarDictND[tuple[int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_2d, ts), vartype=xp.binary, name=''),
    VarDictND[tuple[int, int, pd.Timestamp], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(dt, _2d), vartype=xp.binary, name=''),
    VarDictND[tuple[date, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(rng, str_, ts), vartype=xp.binary, name=''),
    VarDictND[tuple[int, str, pd.Timestamp], xp.var],
)

# 4
assert_type(
    addVariables(prob, IndexSetND((i, i, i, i) for i in rng), vartype=xp.integer, name=''),
    VarDictND[tuple[int, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_3d, dt), vartype=xp.integer, name=''),
    VarDictND[tuple[int, int, int, date], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_2d, _2d), vartype=xp.integer, name=''),
    VarDictND[tuple[int, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(_2d, dttm, ts), vartype=xp.integer, name=''),
    VarDictND[tuple[int, int, datetime, pd.Timestamp], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(dt, _3d), vartype=xp.integer, name=''),
    VarDictND[tuple[date, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(dttm, _2d, ts), vartype=xp.integer, name=''),
    VarDictND[tuple[datetime, int, int, pd.Timestamp], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(rng, str_, dttm, ts), vartype=xp.integer, name=''),
    VarDictND[tuple[int, str, datetime, pd.Timestamp], xp.var],
)

# 5
assert_type(
    addVariables(
        prob, IndexSetND((i, i, i, i, i) for i in rng), lb=1, vartype=xp.semicontinuous, name=''
    ),
    VarDictND[tuple[int, int, int, int, int], xp.var],
)
assert_type(
    addVariables(prob, IndexSetND(rng, str_, dt, dttm, ts), lb=1, vartype=xp.semiinteger, name=''),
    VarDictND[tuple[int, str, date, datetime, pd.Timestamp], xp.var],
)
