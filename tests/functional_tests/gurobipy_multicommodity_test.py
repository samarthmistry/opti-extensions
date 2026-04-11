# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The multicommodity transportation problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
"""

from gurobipy import GRB, Model

from opti_extensions import IndexSetND
from opti_extensions.gurobipy import addVars

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

    model = Model()

    ##### Add decision variables

    # Units of product to ship from an origin to a destination
    trans = addVars(
        model,
        IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
        vtype=GRB.CONTINUOUS,
        name='NUM-UNITS',
    )

    # Whether to ship from an origin to a destination
    use = addVars(
        model,
        IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
        vtype=GRB.BINARY,
        name='USE-ROUTE',
    )

    ##### Set objective

    # Minimize the total shipping cost
    model.setObjective(
        vcost @ trans + fcost @ use,
        GRB.MINIMIZE,
    )

    ##### Add constraints

    # Total units of products shipped from each origin should be equal to its supply
    model.addConstrs(
        (trans.sum(i, '*', p) == supply[i, p] for i in ORIG for p in PROD),
        name='supply',
    )

    # Total units of products shipped to each destination should be equal to its demand
    model.addConstrs(
        (trans.sum('*', j, p) == demand[j, p] for j in DEST for p in PROD),
        name='demand',
    )

    # Total units of products shipped from an origin to a destination is limited
    model.addConstrs(
        (trans.sum(i, j, '*') <= limit * use[i, j] for i in ORIG for j in DEST),
        name='multi',
    )

    ##### Solve

    model.optimize()

    _obj = f'Objective={round(model.ObjVal, 2):.2f}'
    _val1 = '\n'.join(f'{idx}={int(round(var.X, 3))}' for idx, var in use.items())
    _val2 = '\n'.join(f'{idx}={round(var.X + 1e-6, 2):.2f}' for idx, var in trans.items())

    sol_str = f'{_obj}\n{_val1}\n{_val2}'
    assert sol_str.split('\n') == MULTICOMMODITY_EXPECTED_SOLUTION
