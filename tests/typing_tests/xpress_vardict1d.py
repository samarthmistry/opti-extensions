# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
import xpress as xp
from typing_extensions import assert_type

from opti_extensions import IndexSet1D
from opti_extensions.xpress import VarDict1D, addVariables

prob = xp.problem()


assert_type(
    addVariables(prob, IndexSet1D(range(3)), vartype=xp.continuous, name=''), VarDict1D[int, xp.var]
)
assert_type(
    addVariables(prob, IndexSet1D([0, 1, 2]), vartype=xp.continuous, name=''),
    VarDict1D[int, xp.var],
)
assert_type(
    addVariables(prob, IndexSet1D(['A', 'B', 'C']), vartype=xp.binary, name=''),
    VarDict1D[str, xp.var],
)
assert_type(
    addVariables(
        prob,
        IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]),
        vartype=xp.integer,
        name='',
    ),
    VarDict1D[date, xp.var],
)
assert_type(
    addVariables(
        prob,
        IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
        lb=1,
        vartype=xp.semicontinuous,
        name='',
    ),
    VarDict1D[datetime, xp.var],
)
assert_type(
    addVariables(
        prob,
        IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')),
        lb=1,
        vartype=xp.semiinteger,
        name='',
    ),
    VarDict1D[pd.Timestamp, xp.var],
)
