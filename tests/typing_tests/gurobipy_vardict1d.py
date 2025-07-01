# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from gurobipy import GRB, Model, Var
from typing_extensions import assert_type

from opti_extensions import IndexSet1D
from opti_extensions.gurobipy import VarDict1D, addVars

mdl = Model()

assert_type(addVars(mdl, IndexSet1D(range(3)), vtype=GRB.CONTINUOUS), VarDict1D[int, Var])
assert_type(addVars(mdl, IndexSet1D([0, 1, 2]), vtype=GRB.CONTINUOUS), VarDict1D[int, Var])
assert_type(addVars(mdl, IndexSet1D(['A', 'B', 'C']), vtype=GRB.BINARY), VarDict1D[str, Var])
assert_type(
    addVars(
        mdl, IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]), vtype=GRB.INTEGER
    ),
    VarDict1D[date, Var],
)
assert_type(
    addVars(
        mdl,
        IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
        lb=1,
        vtype=GRB.SEMICONT,
    ),
    VarDict1D[datetime, Var],
)
assert_type(
    addVars(
        mdl,
        IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')),
        lb=1,
        vtype=GRB.SEMIINT,
    ),
    VarDict1D[pd.Timestamp, Var],
)
