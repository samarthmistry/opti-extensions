# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The multicommodity transportation problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
"""

import pandas as pd
from docplex.mp.model import Model

from opti_extensions import IndexSetND
from opti_extensions.docplex import add_variables, solve


def test_multicommodity():
    ##### Input data
    # Units of products available at origins
    df_supply = (
        pd.DataFrame(
            {
                'CLEV': {'bands': 700, 'coils': 1600, 'plate': 300},
                'GARY': {'bands': 400, 'coils': 800, 'plate': 200},
                'PITT': {'bands': 800, 'coils': 1800, 'plate': 300},
            }
        )
        .rename_axis('PROD', axis=0)
        .rename_axis('ORI', axis=1)
        .transpose()
    )

    # Units of products required at destinations
    df_demand = (
        pd.DataFrame(
            {
                'DET': {'bands': 300, 'coils': 750, 'plate': 100},
                'FRA': {'bands': 300, 'coils': 500, 'plate': 100},
                'FRE': {'bands': 225, 'coils': 850, 'plate': 100},
                'LAF': {'bands': 250, 'coils': 500, 'plate': 250},
                'LAN': {'bands': 100, 'coils': 400, 'plate': 0},
                'STL': {'bands': 650, 'coils': 950, 'plate': 200},
                'WIN': {'bands': 75, 'coils': 250, 'plate': 50},
            }
        )
        .rename_axis('PROD', axis=0)
        .rename_axis('DES', axis=1)
        .transpose()
    )

    # Variable cost of shipping a product from an origin to a destination
    df_vcost = (
        pd.DataFrame(
            {
                ('CLEV', 'DET'): {'bands': 41, 'coils': 46, 'plate': 5},
                ('CLEV', 'FRA'): {'bands': 17, 'coils': 17, 'plate': 41},
                ('CLEV', 'FRE'): {'bands': 39, 'coils': 47, 'plate': 21},
                ('CLEV', 'LAF'): {'bands': 31, 'coils': 25, 'plate': 37},
                ('CLEV', 'LAN'): {'bands': 19, 'coils': 45, 'plate': 28},
                ('CLEV', 'STL'): {'bands': 10, 'coils': 26, 'plate': 35},
                ('CLEV', 'WIN'): {'bands': 13, 'coils': 45, 'plate': 28},
                ('GARY', 'DET'): {'bands': 31, 'coils': 30, 'plate': 5},
                ('GARY', 'FRA'): {'bands': 7, 'coils': 39, 'plate': 30},
                ('GARY', 'FRE'): {'bands': 45, 'coils': 23, 'plate': 24},
                ('GARY', 'LAF'): {'bands': 41, 'coils': 9, 'plate': 41},
                ('GARY', 'LAN'): {'bands': 15, 'coils': 34, 'plate': 45},
                ('GARY', 'STL'): {'bands': 15, 'coils': 37, 'plate': 17},
                ('GARY', 'WIN'): {'bands': 40, 'coils': 39, 'plate': 19},
                ('PITT', 'DET'): {'bands': 38, 'coils': 24, 'plate': 6},
                ('PITT', 'FRA'): {'bands': 33, 'coils': 34, 'plate': 8},
                ('PITT', 'FRE'): {'bands': 17, 'coils': 41, 'plate': 29},
                ('PITT', 'LAF'): {'bands': 48, 'coils': 6, 'plate': 38},
                ('PITT', 'LAN'): {'bands': 44, 'coils': 38, 'plate': 49},
                ('PITT', 'STL'): {'bands': 22, 'coils': 17, 'plate': 35},
                ('PITT', 'WIN'): {'bands': 45, 'coils': 37, 'plate': 48},
            }
        )
        .rename_axis('PROD', axis=0)
        .rename_axis(['ORI', 'DES'], axis=1)
        .transpose()
    )

    # Fixed cost of shipping from an origin to a destination
    df_fcost = (
        pd.DataFrame(
            {
                'DET': {'CLEV': 1891, 'GARY': 1928, 'PITT': 1453},
                'FRA': {'CLEV': 1540, 'GARY': 1042, 'PITT': 1728},
                'FRE': {'CLEV': 1108, 'GARY': 1628, 'PITT': 1746},
                'LAF': {'CLEV': 1907, 'GARY': 1934, 'PITT': 1816},
                'LAN': {'CLEV': 1432, 'GARY': 1733, 'PITT': 1818},
                'STL': {'CLEV': 1470, 'GARY': 1645, 'PITT': 1563},
                'WIN': {'CLEV': 1447, 'GARY': 1446, 'PITT': 1977},
            }
        )
        .rename_axis('ORI', axis=0)
        .rename_axis('DEST', axis=1)
    )

    ##### Index-sets

    ORIG = df_supply.index.opti.to_indexset()
    DEST = df_demand.index.opti.to_indexset()
    PROD = df_supply.columns.opti.to_indexset()

    ##### Parameters

    supply = df_supply.stack().opti.to_paramdict()
    demand = df_demand.stack().opti.to_paramdict()
    vcost = df_vcost.stack().opti.to_paramdict()
    fcost = df_fcost.stack().opti.to_paramdict()

    # Limit on shipping total units of products from an origin to a destination
    limit = 625

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
    model.minimize(
        model.sum(vcost[i, j, p] * trans[i, j, p] for i in ORIG for j in DEST for p in PROD)
        + model.sum(fcost[i, j] * use[i, j] for i in ORIG for j in DEST)
    )

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
    _val1 = '\n'.join(f'{idx}={int(var.sv)}' for idx, var in use.items())
    _val2 = '\n'.join(f'{idx}={round(var.sv + 1e-6, 2):.2f}' for idx, var in trans.items())

    sol_str = f'{_obj}\n{_val1}\n{_val2}'
    assert sol_str.split('\n') == [
        'Objective=192644.00',
        "('CLEV', 'DET')=1",
        "('CLEV', 'FRA')=1",
        "('CLEV', 'FRE')=0",
        "('CLEV', 'LAF')=1",
        "('CLEV', 'LAN')=1",
        "('CLEV', 'STL')=1",
        "('CLEV', 'WIN')=1",
        "('GARY', 'DET')=1",
        "('GARY', 'FRA')=0",
        "('GARY', 'FRE')=1",
        "('GARY', 'LAF')=0",
        "('GARY', 'LAN')=0",
        "('GARY', 'STL')=1",
        "('GARY', 'WIN')=0",
        "('PITT', 'DET')=1",
        "('PITT', 'FRA')=1",
        "('PITT', 'FRE')=1",
        "('PITT', 'LAF')=1",
        "('PITT', 'LAN')=0",
        "('PITT', 'STL')=1",
        "('PITT', 'WIN')=0",
        "('CLEV', 'DET', 'bands')=0.00",
        "('CLEV', 'DET', 'coils')=125.00",
        "('CLEV', 'DET', 'plate')=100.00",
        "('CLEV', 'FRA', 'bands')=0.00",
        "('CLEV', 'FRA', 'coils')=500.00",
        "('CLEV', 'FRA', 'plate')=0.00",
        "('CLEV', 'FRE', 'bands')=0.00",
        "('CLEV', 'FRE', 'coils')=0.00",
        "('CLEV', 'FRE', 'plate')=0.00",
        "('CLEV', 'LAF', 'bands')=225.00",
        "('CLEV', 'LAF', 'coils')=0.00",
        "('CLEV', 'LAF', 'plate')=150.00",
        "('CLEV', 'LAN', 'bands')=100.00",
        "('CLEV', 'LAN', 'coils')=400.00",
        "('CLEV', 'LAN', 'plate')=0.00",
        "('CLEV', 'STL', 'bands')=300.00",
        "('CLEV', 'STL', 'coils')=325.00",
        "('CLEV', 'STL', 'plate')=0.00",
        "('CLEV', 'WIN', 'bands')=75.00",
        "('CLEV', 'WIN', 'coils')=250.00",
        "('CLEV', 'WIN', 'plate')=50.00",
        "('GARY', 'DET', 'bands')=50.00",
        "('GARY', 'DET', 'coils')=250.00",
        "('GARY', 'DET', 'plate')=0.00",
        "('GARY', 'FRA', 'bands')=0.00",
        "('GARY', 'FRA', 'coils')=0.00",
        "('GARY', 'FRA', 'plate')=0.00",
        "('GARY', 'FRE', 'bands')=0.00",
        "('GARY', 'FRE', 'coils')=550.00",
        "('GARY', 'FRE', 'plate')=0.00",
        "('GARY', 'LAF', 'bands')=0.00",
        "('GARY', 'LAF', 'coils')=0.00",
        "('GARY', 'LAF', 'plate')=0.00",
        "('GARY', 'LAN', 'bands')=0.00",
        "('GARY', 'LAN', 'coils')=0.00",
        "('GARY', 'LAN', 'plate')=0.00",
        "('GARY', 'STL', 'bands')=350.00",
        "('GARY', 'STL', 'coils')=0.00",
        "('GARY', 'STL', 'plate')=200.00",
        "('GARY', 'WIN', 'bands')=0.00",
        "('GARY', 'WIN', 'coils')=0.00",
        "('GARY', 'WIN', 'plate')=0.00",
        "('PITT', 'DET', 'bands')=250.00",
        "('PITT', 'DET', 'coils')=375.00",
        "('PITT', 'DET', 'plate')=0.00",
        "('PITT', 'FRA', 'bands')=300.00",
        "('PITT', 'FRA', 'coils')=0.00",
        "('PITT', 'FRA', 'plate')=100.00",
        "('PITT', 'FRE', 'bands')=225.00",
        "('PITT', 'FRE', 'coils')=300.00",
        "('PITT', 'FRE', 'plate')=100.00",
        "('PITT', 'LAF', 'bands')=25.00",
        "('PITT', 'LAF', 'coils')=500.00",
        "('PITT', 'LAF', 'plate')=100.00",
        "('PITT', 'LAN', 'bands')=0.00",
        "('PITT', 'LAN', 'coils')=0.00",
        "('PITT', 'LAN', 'plate')=0.00",
        "('PITT', 'STL', 'bands')=0.00",
        "('PITT', 'STL', 'coils')=625.00",
        "('PITT', 'STL', 'plate')=0.00",
        "('PITT', 'WIN', 'bands')=0.00",
        "('PITT', 'WIN', 'coils')=0.00",
        "('PITT', 'WIN', 'plate')=0.00",
    ]
