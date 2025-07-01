# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from datetime import date, datetime

import pandas as pd
from docplex.mp.dvar import Var
from docplex.mp.model import Model
from typing_extensions import assert_type

from opti_extensions import IndexSetND
from opti_extensions.docplex import VarDictND, add_variables

mdl = Model()

rng = range(3)
str_ = ['A', 'B', 'C']
dt = [date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)]
dttm = [datetime(2024, 1, 1, 0), datetime(2024, 2, 1, 1), datetime(2024, 3, 1, 2)]
ts = pd.date_range('2024-01-01', '2024-03-01', freq='MS')
_2d = IndexSetND(rng, rng)
_3d = IndexSetND(rng, rng, rng)

# 2
assert_type(
    add_variables(mdl, IndexSetND((i, i) for i in rng), 'C'), VarDictND[tuple[int, int], Var]
)
assert_type(add_variables(mdl, IndexSetND(str_, ts), 'C'), VarDictND[tuple[str, pd.Timestamp], Var])

# 3
assert_type(
    add_variables(mdl, IndexSetND((i, i, i) for i in rng), 'B'),
    VarDictND[tuple[int, int, int], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(_2d, ts), 'B'), VarDictND[tuple[int, int, pd.Timestamp], Var]
)
assert_type(add_variables(mdl, IndexSetND(dt, _2d), 'B'), VarDictND[tuple[date, int, int], Var])
assert_type(
    add_variables(mdl, IndexSetND(rng, str_, ts), 'B'),
    VarDictND[tuple[int, str, pd.Timestamp], Var],
)

# 4
assert_type(
    add_variables(mdl, IndexSetND((i, i, i, i) for i in rng), 'I'),
    VarDictND[tuple[int, int, int, int], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(_3d, dt), 'I'), VarDictND[tuple[int, int, int, date], Var]
)
assert_type(
    add_variables(mdl, IndexSetND(_2d, _2d), 'I'), VarDictND[tuple[int, int, int, int], Var]
)
assert_type(
    add_variables(mdl, IndexSetND(_2d, dttm, ts), 'I'),
    VarDictND[tuple[int, int, datetime, pd.Timestamp], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(dt, _3d), 'I'), VarDictND[tuple[date, int, int, int], Var]
)
assert_type(
    add_variables(mdl, IndexSetND(dttm, _2d, ts), 'I'),
    VarDictND[tuple[datetime, int, int, pd.Timestamp], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(rng, str_, dttm, ts), 'I'),
    VarDictND[tuple[int, str, datetime, pd.Timestamp], Var],
)

# 5
assert_type(
    add_variables(mdl, IndexSetND((i, i, i, i, i) for i in rng), 'SC', lb=1),
    VarDictND[tuple[int, int, int, int, int], Var],
)
assert_type(
    add_variables(mdl, IndexSetND(rng, str_, dt, dttm, ts), 'SI', lb=1),
    VarDictND[tuple[int, str, date, datetime, pd.Timestamp], Var],
)
