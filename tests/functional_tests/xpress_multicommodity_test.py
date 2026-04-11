# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The multicommodity transportation problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
"""

import warnings

import xpress as xp

from opti_extensions import IndexSetND
from opti_extensions.xpress import addVariables

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

    with warnings.catch_warnings():
        # Filter out warnings here instead of general pytest settings because
        # tox will run several configurations where xpress is not a dep
        #   filterwarnings = ["ignore::xpress.LicenseWarning"]
        warnings.filterwarnings('ignore', category=xp.LicenseWarning)
        prob = xp.problem()

    ##### Add decision variables

    # Units of product to ship from an origin to a destination
    trans = addVariables(
        prob,
        IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
        vartype=xp.continuous,
        name='NUM-UNITS',
    )

    # Whether to ship from an origin to a destination
    use = addVariables(
        prob,
        IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
        vartype=xp.binary,
        name='USE-ROUTE',
    )

    ##### Set objective

    # Minimize the total shipping cost
    prob.setObjective(
        vcost @ trans + fcost @ use,
        sense=xp.minimize,
    )

    ##### Add constraints

    # Total units of products shipped from each origin should be equal to its supply
    prob.addConstraint(trans.sum(i, '*', p) == supply[i, p] for i in ORIG for p in PROD)

    # Total units of products shipped to each destination should be equal to its demand
    prob.addConstraint(trans.sum('*', j, p) == demand[j, p] for j in DEST for p in PROD)

    # Total units of products shipped from an origin to a destination is limited
    prob.addConstraint(trans.sum(i, j, '*') <= limit * use[i, j] for i in ORIG for j in DEST)

    ##### Solve

    solvestatus, solstatus = prob.optimize()

    _obj = f'Objective={round(prob.attributes.objval, 2):.2f}'
    _val1 = '\n'.join(f'{idx}={int(round(prob.getSolution(var), 3))}' for idx, var in use.items())
    _val2 = '\n'.join(
        f'{idx}={round(prob.getSolution(var) + 1e-6, 2):.2f}' for idx, var in trans.items()
    )

    sol_str = f'{_obj}\n{_val1}\n{_val2}'
    assert sol_str.split('\n') == MULTICOMMODITY_EXPECTED_SOLUTION
