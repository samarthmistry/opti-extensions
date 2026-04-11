# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The multicommodity transportation problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
"""

from highspy import Highs, HighsVarType, ObjSense

from opti_extensions import IndexSetND
from opti_extensions.highspy import addVariables

from .conftest import MULTICOMMODITY_EXPECTED_SOLUTION


def test_multicommodity(multicommodity_data):
    ORIG = multicommodity_data['ORIG']
    DEST = multicommodity_data['DEST']
    PROD = multicommodity_data['PROD']
    supply = multicommodity_data['supply']
    demand = multicommodity_data['demand']
    vcost = multicommodity_data['vcost']
    fcost = multicommodity_data['fcost']
    limit = multicommodity_data['limit']

    ##### Instantiate

    model = Highs()
    model.silent()

    ##### Add decision variables

    # Units of product to ship from an origin to a destination
    trans = addVariables(
        model,
        IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
        type=HighsVarType.kContinuous,
        name_prefix='NUM-UNITS',
    )

    # Whether to ship from an origin to a destination
    use = addVariables(
        model,
        IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
        type=HighsVarType.kInteger,
        lb=0,
        ub=1,
        name_prefix='USE-ROUTE',
    )

    ##### Set objective

    # Minimize the total shipping cost
    model.setObjective(
        vcost @ trans + fcost @ use,
        ObjSense.kMinimize,
    )

    ##### Add constraints

    # Total units of products shipped from each origin should be equal to its supply
    model.addConstrs(
        (trans.sum(i, '*', p) == supply[i, p] for i in ORIG for p in PROD),
    )

    # Total units of products shipped to each destination should be equal to its demand
    model.addConstrs(
        (trans.sum('*', j, p) == demand[j, p] for j in DEST for p in PROD),
    )

    # Total units of products shipped from an origin to a destination is limited
    model.addConstrs(
        (trans.sum(i, j, '*') <= limit * use[i, j] for i in ORIG for j in DEST),
    )

    ##### Solve

    model.solve()

    _obj = f'Objective={round(model.getObjectiveValue(), 2):.2f}'
    _val1 = '\n'.join(f'{idx}={int(round(model.val(var), 3))}' for idx, var in use.items())
    _val2 = '\n'.join(f'{idx}={round(model.val(var) + 1e-6, 2):.2f}' for idx, var in trans.items())

    sol_str = f'{_obj}\n{_val1}\n{_val2}'
    assert sol_str.split('\n') == MULTICOMMODITY_EXPECTED_SOLUTION
