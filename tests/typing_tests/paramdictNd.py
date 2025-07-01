# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import ParamDictND

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
