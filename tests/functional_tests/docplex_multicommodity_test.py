# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The multicommodity transportation problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
"""

from docplex.mp.model import Model

from opti_extensions import IndexSetND
from opti_extensions.docplex import add_variables, solve

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

    model = Model(name='multicommodity')

    ##### Add decision variables

    # Units of product to ship from an origin to a destination
    trans = add_variables(
        model,
        indexset=IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
        vartype='continuous',
        name='NUM-UNITS',
    )

    # Whether to ship from an origin to a destination
    use = add_variables(
        model,
        indexset=IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
        vartype='binary',
        name='USE-ROUTE',
    )

    ##### Set objective

    # Minimize the total shipping cost
    model.minimize(vcost @ trans + fcost @ use)

    ##### Add constraints

    # Total units of products shipped from each origin should be equal to its supply
    model.add_constraints_(
        (trans.sum(i, '*', p) == supply[i, p], f'supply_{i}_{p}') for i in ORIG for p in PROD
    )

    # Total units of products shipped to each destination should be equal to its demand
    model.add_constraints_(
        (trans.sum('*', j, p) == demand[j, p], f'demand_{j}_{p}') for j in DEST for p in PROD
    )

    # Total units of products shipped from an origin to a destination is limited
    model.add_constraints_(
        (trans.sum(i, j, '*') <= limit * use[i, j], f'multi_{i}_{j}') for i in ORIG for j in DEST
    )

    ##### Solve

    sol = solve(model)

    _obj = f'Objective={round(sol.objective_value, 2):.2f}'
    _val1 = '\n'.join(f'{idx}={int(round(var.sv, 3))}' for idx, var in use.items())
    _val2 = '\n'.join(f'{idx}={round(var.sv + 1e-6, 2):.2f}' for idx, var in trans.items())

    sol_str = f'{_obj}\n{_val1}\n{_val2}'
    assert sol_str.split('\n') == MULTICOMMODITY_EXPECTED_SOLUTION
