# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from typing_extensions import assert_type

from opti_extensions import IndexSet1D

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
