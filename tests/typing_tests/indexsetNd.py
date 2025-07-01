# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import IndexSetND

rng = range(3)
str_ = ['A', 'B', 'C']
dt = [date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]
dttm = [datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]
ts = pd.date_range('2024-01-01', '2024-03-01', freq='MS')
_2d = IndexSetND(rng, rng)
_3d = IndexSetND(rng, rng, rng)

# 2
assert_type(IndexSetND((i, i) for i in rng), IndexSetND[tuple[int, int]])
assert_type(IndexSetND(str_, ts), IndexSetND[tuple[str, pd.Timestamp]])

# 3
assert_type(IndexSetND((i, i, i) for i in rng), IndexSetND[tuple[int, int, int]])
assert_type(IndexSetND(_2d, ts), IndexSetND[tuple[int, int, pd.Timestamp]])
assert_type(IndexSetND(dt, _2d), IndexSetND[tuple[date, int, int]])
assert_type(IndexSetND(rng, str_, ts), IndexSetND[tuple[int, str, pd.Timestamp]])

# 4
assert_type(IndexSetND((i, i, i, i) for i in rng), IndexSetND[tuple[int, int, int, int]])
assert_type(IndexSetND(_3d, dt), IndexSetND[tuple[int, int, int, date]])
assert_type(IndexSetND(_2d, _2d), IndexSetND[tuple[int, int, int, int]])
assert_type(IndexSetND(_2d, dttm, ts), IndexSetND[tuple[int, int, datetime, pd.Timestamp]])
assert_type(IndexSetND(dt, _3d), IndexSetND[tuple[date, int, int, int]])
assert_type(IndexSetND(dttm, _2d, ts), IndexSetND[tuple[datetime, int, int, pd.Timestamp]])
assert_type(IndexSetND(rng, str_, dttm, ts), IndexSetND[tuple[int, str, datetime, pd.Timestamp]])

# 5
assert_type(IndexSetND((i, i, i, i, i) for i in rng), IndexSetND[tuple[int, int, int, int, int]])
assert_type(
    IndexSetND(rng, str_, dt, dttm, ts), IndexSetND[tuple[int, str, date, datetime, pd.Timestamp]]
)
