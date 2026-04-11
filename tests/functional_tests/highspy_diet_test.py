# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The diet problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-lecture/diet_case_study.ipynb
"""

from highspy import Highs, HighsVarType

from opti_extensions.highspy import addVariables

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

    model = Highs()
    model.silent()

    ##### Add decision variables

    # Amount of food to purchase
    buy = addVariables(
        model,
        indexset=FOOD,
        lb=f_min,
        ub=f_max,
        type=HighsVarType.kContinuous,
        name_prefix='BUY-QTY',
    )

    ##### Set objective

    # Minimize the total cost of the diet
    model.minimize(cost @ buy)

    ##### Add constraints

    # Ensure that the nutritional requirements are satisfied by the diet
    model.addConstrs(
        (Highs.qsum(amt[i, j] * buy[j] for j in FOOD) >= n_min[i] for i in NUTR),
    )
    model.addConstrs(
        (Highs.qsum(amt[i, j] * buy[j] for j in FOOD) <= n_max[i] for i in NUTR),
    )

    ##### Solve

    model.solve()

    ##### Verify solution

    _obj = f'Objective={round(model.getObjectiveValue(), 2):.2f}'
    _val = '\n'.join(f'{idx}={int(round(model.val(var), 3))}' for idx, var in buy.items())

    sol_str = f'{_obj}\n{_val}'
    assert sol_str.split('\n') == DIET_EXPECTED_SOLUTION
