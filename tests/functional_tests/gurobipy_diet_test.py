# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The diet problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-lecture/diet_case_study.ipynb
"""

from gurobipy import GRB, Model, quicksum

from opti_extensions import IndexSet1D, ParamDict1D, ParamDictND
from opti_extensions.gurobipy import addVars


def test_diet():
    ##### Index-sets

    # Nutrients to consider
    NUTR = IndexSet1D(['A', 'B1', 'B2', 'C'], name='NUTRIENT')

    # Food items to consider
    FOOD = IndexSet1D(['BEEF', 'CHK', 'FISH', 'HAM', 'MCH', 'MTL', 'SPG', 'TUR'], name='FOOD')

    ##### Parameters

    # Cost of each food item
    cost = ParamDict1D(
        {
            'BEEF': 3.19,
            'CHK': 2.59,
            'FISH': 2.29,
            'HAM': 2.89,
            'MCH': 1.89,
            'MTL': 1.99,
            'SPG': 1.99,
            'TUR': 2.49,
        },
        key_name='FOOD',
        value_name='COST',
    )

    # Minimum purchase quantity for each food item
    f_min = ParamDict1D(
        {
            'BEEF': 0,
            'CHK': 0,
            'FISH': 0,
            'HAM': 0,
            'MCH': 0,
            'MTL': 0,
            'SPG': 0,
            'TUR': 0,
        },
        key_name='FOOD',
        value_name='MIN-QTY',
    )

    # Maximum purchase quantity for each food item
    f_max = ParamDict1D(
        {
            'BEEF': 100,
            'CHK': 100,
            'FISH': 100,
            'HAM': 100,
            'MCH': 100,
            'MTL': 100,
            'SPG': 100,
            'TUR': 100,
        },
        key_name='FOOD',
        value_name='MAX-QTY',
    )

    # Minimum amount required of each nutrient
    n_min = ParamDict1D(
        {'A': 700, 'C': 700, 'B1': 700, 'B2': 700},
        key_name='NUTRITION',
        value_name='MIN-AMT',
    )

    # Maximum amount allowed of each nutrient
    n_max = ParamDict1D(
        {'A': 10000, 'C': 10000, 'B1': 10000, 'B2': 10000},
        key_name='NUTRITION',
        value_name='MAX-AMT',
    )

    # Amount of each nutrient in each food item
    amt = ParamDictND(
        {
            ('A', 'BEEF'): 60,
            ('C', 'BEEF'): 20,
            ('B1', 'BEEF'): 10,
            ('B2', 'BEEF'): 15,
            ('A', 'CHK'): 8,
            ('C', 'CHK'): 0,
            ('B1', 'CHK'): 20,
            ('B2', 'CHK'): 20,
            ('A', 'FISH'): 8,
            ('C', 'FISH'): 10,
            ('B1', 'FISH'): 15,
            ('B2', 'FISH'): 10,
            ('A', 'HAM'): 40,
            ('C', 'HAM'): 40,
            ('B1', 'HAM'): 35,
            ('B2', 'HAM'): 10,
            ('A', 'MCH'): 15,
            ('C', 'MCH'): 35,
            ('B1', 'MCH'): 15,
            ('B2', 'MCH'): 15,
            ('A', 'MTL'): 70,
            ('C', 'MTL'): 30,
            ('B1', 'MTL'): 15,
            ('B2', 'MTL'): 15,
            ('A', 'SPG'): 25,
            ('C', 'SPG'): 50,
            ('B1', 'SPG'): 25,
            ('B2', 'SPG'): 15,
            ('A', 'TUR'): 60,
            ('C', 'TUR'): 20,
            ('B1', 'TUR'): 15,
            ('B2', 'TUR'): 10,
        },
        key_names=('FOOD', 'NUTR'),
        value_name='AMT',
    )

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
    _val = '\n'.join(f'{idx}={int(var.X)}' for idx, var in buy.items())

    sol_str = f'{_obj}\n{_val}'
    assert sol_str.split('\n') == [
        'Objective=88.20',
        'BEEF=0',
        'CHK=0',
        'FISH=0',
        'HAM=0',
        'MCH=46',
        'MTL=0',
        'SPG=0',
        'TUR=0',
    ]
