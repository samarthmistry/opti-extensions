# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The diet problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-lecture/diet_case_study.ipynb
"""

from gurobipy import GRB, Model, quicksum

from opti_extensions.gurobipy import addVars

from .conftest import DIET_EXPECTED_SOLUTION


def test_diet(diet_data):
    NUTR = diet_data['NUTR']
    FOOD = diet_data['FOOD']
    cost = diet_data['cost']
    f_min = diet_data['f_min']
    f_max = diet_data['f_max']
    n_min = diet_data['n_min']
    n_max = diet_data['n_max']
    amt = diet_data['amt']

    ##### Instantiate

    model = Model(name='diet')

    ##### Add decision variables

    # Amount of food to purchase
    buy = addVars(model, indexset=FOOD, lb=f_min, ub=f_max, vtype=GRB.CONTINUOUS, name='BUY-QTY')

    ##### Set objective

    # Minimize the total cost of the diet
    model.setObjective(cost @ buy, GRB.MINIMIZE)

    ##### Add constraints

    # Ensure that the nutritional requirements are satisfied by the diet
    model.addConstrs(
        (quicksum(amt[i, j] * buy[j] for j in FOOD) >= n_min[i] for i in NUTR),
        name='min-nutr-reqd',
    )
    model.addConstrs(
        (quicksum(amt[i, j] * buy[j] for j in FOOD) <= n_max[i] for i in NUTR),
        name='max-nutr-allwd',
    )

    ##### Solve

    model.optimize()

    _obj = f'Objective={round(model.ObjVal, 2):.2f}'
    _val = '\n'.join(f'{idx}={int(round(var.X, 3))}' for idx, var in buy.items())

    sol_str = f'{_obj}\n{_val}'
    assert sol_str.split('\n') == DIET_EXPECTED_SOLUTION
