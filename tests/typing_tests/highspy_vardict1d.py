# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from highspy import Highs, HighsVarType
from highspy.highs import highs_var
from typing_extensions import assert_type

from opti_extensions import IndexSet1D
from opti_extensions.highspy import VarDict1D, addVariables

mdl = Highs()

assert_type(
    addVariables(mdl, IndexSet1D(range(3)), type=HighsVarType.kContinuous),
    VarDict1D[int, highs_var],
)
assert_type(
    addVariables(mdl, IndexSet1D([0, 1, 2]), type=HighsVarType.kContinuous),
    VarDict1D[int, highs_var],
)
assert_type(
    addVariables(mdl, IndexSet1D(['A', 'B', 'C']), type=HighsVarType.kInteger),
    VarDict1D[str, highs_var],
)
assert_type(
    addVariables(
        mdl,
        IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]),
        type=HighsVarType.kInteger,
    ),
    VarDict1D[date, highs_var],
)
assert_type(
    addVariables(
        mdl,
        IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
        lb=1,
        type=HighsVarType.kContinuous,
    ),
    VarDict1D[datetime, highs_var],
)
assert_type(
    addVariables(
        mdl,
        IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')),
        lb=1,
        type=HighsVarType.kInteger,
    ),
    VarDict1D[pd.Timestamp, highs_var],
)
