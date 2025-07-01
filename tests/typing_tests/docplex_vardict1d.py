# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from docplex.mp.dvar import Var
from docplex.mp.model import Model
from typing_extensions import assert_type

from opti_extensions import IndexSet1D
from opti_extensions.docplex import VarDict1D, add_variables

mdl = Model()

assert_type(add_variables(mdl, IndexSet1D(range(3)), 'C'), VarDict1D[int, Var])
assert_type(add_variables(mdl, IndexSet1D([0, 1, 2]), 'C'), VarDict1D[int, Var])
assert_type(add_variables(mdl, IndexSet1D(['A', 'B', 'C']), 'B'), VarDict1D[str, Var])
assert_type(
    add_variables(mdl, IndexSet1D([date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]), 'I'),
    VarDict1D[date, Var],
)
assert_type(
    add_variables(
        mdl,
        IndexSet1D([datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]),
        'SC',
        lb=1,
    ),
    VarDict1D[datetime, Var],
)
assert_type(
    add_variables(
        mdl, IndexSet1D(pd.date_range('2024-01-01', '2024-03-01', freq='MS')), 'SI', lb=1
    ),
    VarDict1D[pd.Timestamp, Var],
)
