# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import ParamDict1D

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
