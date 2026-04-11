# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The diet problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-lecture/diet_case_study.ipynb
"""

from docplex.mp.model import Model

from opti_extensions.docplex import add_variables, solve

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
    buy = add_variables(
        model, indexset=FOOD, vartype='continuous', lb=f_min, ub=f_max, name='BUY-QTY'
    )

    ##### Set objective

    # Minimize the total cost of the diet
    model.minimize(cost @ buy)

    ##### Add constraints

    # Ensure that the nutritional requirements are satisfied by the diet
    model.add_constraints_(
        (model.sum(amt[i, j] * buy[j] for j in FOOD) >= n_min[i], f'min-nutr-reqd_{i}')
        for i in NUTR
    )
    model.add_constraints_(
        (model.sum(amt[i, j] * buy[j] for j in FOOD) <= n_max[i], f'max-nutr-allwd_{i}')
        for i in NUTR
    )

    ##### Solve

    sol = solve(model, log_output=True)

    _obj = f'Objective={round(sol.objective_value, 2):.2f}'
    _val = '\n'.join(f'{idx}={int(round(var.sv, 3))}' for idx, var in buy.items())

    sol_str = f'{_obj}\n{_val}'
    assert sol_str.split('\n') == DIET_EXPECTED_SOLUTION
