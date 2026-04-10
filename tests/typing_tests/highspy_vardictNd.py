# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from highspy import Highs, HighsVarType
from highspy.highs import highs_var
from typing_extensions import assert_type

from opti_extensions import IndexSetND
from opti_extensions.highspy import VarDictND, addVariables

mdl = Highs()

rng = range(3)
str_ = ['A', 'B', 'C']
dt = [date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]
dttm = [datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]
ts = pd.date_range('2024-01-01', '2024-03-01', freq='MS')
_2d = IndexSetND(rng, rng)
_3d = IndexSetND(rng, rng, rng)

# 2
assert_type(
    addVariables(mdl, IndexSetND((i, i) for i in rng), type=HighsVarType.kContinuous),
    VarDictND[tuple[int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(str_, ts), type=HighsVarType.kContinuous),
    VarDictND[tuple[str, pd.Timestamp], highs_var],
)

# 3
assert_type(
    addVariables(mdl, IndexSetND((i, i, i) for i in rng), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_2d, ts), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, pd.Timestamp], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(dt, _2d), type=HighsVarType.kInteger),
    VarDictND[tuple[date, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(rng, str_, ts), type=HighsVarType.kInteger),
    VarDictND[tuple[int, str, pd.Timestamp], highs_var],
)

# 4
assert_type(
    addVariables(mdl, IndexSetND((i, i, i, i) for i in rng), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_3d, dt), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, int, date], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_2d, _2d), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(_2d, dttm, ts), type=HighsVarType.kInteger),
    VarDictND[tuple[int, int, datetime, pd.Timestamp], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(dt, _3d), type=HighsVarType.kInteger),
    VarDictND[tuple[date, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(dttm, _2d, ts), type=HighsVarType.kInteger),
    VarDictND[tuple[datetime, int, int, pd.Timestamp], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(rng, str_, dttm, ts), type=HighsVarType.kInteger),
    VarDictND[tuple[int, str, datetime, pd.Timestamp], highs_var],
)

# 5
assert_type(
    addVariables(
        mdl, IndexSetND((i, i, i, i, i) for i in rng), lb=1, type=HighsVarType.kContinuous
    ),
    VarDictND[tuple[int, int, int, int, int], highs_var],
)
assert_type(
    addVariables(mdl, IndexSetND(rng, str_, dt, dttm, ts), lb=1, type=HighsVarType.kInteger),
    VarDictND[tuple[int, str, date, datetime, pd.Timestamp], highs_var],
)
