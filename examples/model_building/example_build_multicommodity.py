# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Multicommodity transportation problem
=====================================

Please refer to chapters 4 & 20 in the `AMPL Book <https://ampl.com/learn/ampl-book>`_
for a detailed description of the problem. We demonstrate how to implement this model
with DOcplex, gurobipy, and Xpress along with the functionality from `opti-extensions`.

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
— Copyright (c) 2022-2022, AMPL Optimization inc. (licensed under the MIT License)
"""

# %%
# Mathematical formulation
# ------------------------
#
# **Index-sets**:
#
# -  | Origins to ship products from:
#    | :math:`i \in ORIG`
# -  | Destinations to ship products to:
#    | :math:`j \in DEST`
# -  | Products to be shipped:
#    | :math:`p \in PROD`
#
# **Parameters**:
#
# -  | Units of product :math:`p` available at origin :math:`i`:
#    | :math:`supply_{i, p} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in ORIG \; \& \; p \in PROD`
# -  | Units of product :math:`p` required at destination :math:`j`:
#    | :math:`demand_{j, p} \in \mathbb{R}_{0}^{+} \quad \forall \; j \in DEST \; \& \; p \in PROD`
# -  | Variable cost of shipping product :math:`p` from origin :math:`i` to destination :math:`j`:
#    | :math:`vcost_{i, j, p} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in ORIG \; \& \; j \in DEST \; \& \; p \in PROD`
# -  | Fixed cost of shipping from origin :math:`i` to destination :math:`j`:
#    | :math:`fcost_{i, j} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in ORIG \; \& \; j \in DEST`
# -  | Limit on shipping total units of products from any origin to any destination:
#    | :math:`limit \in \mathbb{R}_{0}^{+}`
#
# **Variables**:
#
# -  | Units of product :math:`p` to ship from origin :math:`i` to destination :math:`j`:
#    | :math:`trans_{i, j, p} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in ORIG \; \& \; j \in DEST \; \& \; p \in PROD`
# -  | Whether to ship from origin :math:`i` to destination :math:`j`:
#    | :math:`use_{i, j} \in \mathbb{B} \quad \forall \; i \in ORIG \; \& \; j \in DEST`
#
# **Objective**:
#
# -  | Minimize the total shipping cost:
#    | :math:`\sum_{i \in ORIG} \sum_{j \in DEST} \sum_{p \in PROD} vcost_{i, j, p} \times trans_{i, j, p} + \sum_{i \in ORIG} \sum_{j \in DEST} fcost_{i, j} \times use_{i, j}`
#
# **Constraints**:
#
# -  | Total units of product :math:`p` shipped from origin :math:`i` should be equal to its supply:
#    | :math:`\sum_{j \in DEST} trans_{i, j, p} = supply_{i, p}, \; \forall \; i \in ORIG \; \& \; p \in PROD`
# -  | Total units of product :math:`p` shipped to destination :math:`j` should be equal to its demand:
#    | :math:`\sum_{i \in ORIG} trans_{i, j, p} = demand_{j, p}, \; \forall \; j \in DEST \; \& \; p \in PROD`
# -  | Total units of products shipped from origin :math:`i` to destination :math:`j` is limited:
#    | :math:`\sum_{p \in PROD} trans_{i, j, p} \leq limit, \; \forall \; i \in ORIG \; \& \; j \in DEST`

# %%
# Input data in form of pandas dataframes
# ---------------------------------------

# %%
import pandas as pd

# %%
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

print(df_supply)

# %%

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

print(df_demand)

# %%

df_vcost = (
    pd.DataFrame(
        {
            ('CLEV', 'DET'): {'bands': 7, 'coils': 9, 'plate': 9},
            ('CLEV', 'FRA'): {'bands': 22, 'coils': 27, 'plate': 29},
            ('CLEV', 'FRE'): {'bands': 82, 'coils': 95, 'plate': 99},
            ('CLEV', 'LAF'): {'bands': 13, 'coils': 17, 'plate': 18},
            ('CLEV', 'LAN'): {'bands': 10, 'coils': 12, 'plate': 13},
            ('CLEV', 'STL'): {'bands': 21, 'coils': 26, 'plate': 28},
            ('CLEV', 'WIN'): {'bands': 7, 'coils': 9, 'plate': 9},
            ('GARY', 'DET'): {'bands': 10, 'coils': 14, 'plate': 15},
            ('GARY', 'FRA'): {'bands': 30, 'coils': 39, 'plate': 41},
            ('GARY', 'FRE'): {'bands': 71, 'coils': 82, 'plate': 86},
            ('GARY', 'LAF'): {'bands': 6, 'coils': 8, 'plate': 8},
            ('GARY', 'LAN'): {'bands': 8, 'coils': 11, 'plate': 12},
            ('GARY', 'STL'): {'bands': 11, 'coils': 16, 'plate': 17},
            ('GARY', 'WIN'): {'bands': 10, 'coils': 14, 'plate': 16},
            ('PITT', 'DET'): {'bands': 11, 'coils': 14, 'plate': 14},
            ('PITT', 'FRA'): {'bands': 19, 'coils': 24, 'plate': 26},
            ('PITT', 'FRE'): {'bands': 83, 'coils': 99, 'plate': 104},
            ('PITT', 'LAF'): {'bands': 15, 'coils': 20, 'plate': 20},
            ('PITT', 'LAN'): {'bands': 12, 'coils': 17, 'plate': 17},
            ('PITT', 'STL'): {'bands': 25, 'coils': 28, 'plate': 31},
            ('PITT', 'WIN'): {'bands': 10, 'coils': 13, 'plate': 13},
        }
    )
    .rename_axis('PROD', axis=0)
    .rename_axis(['ORI', 'DES'], axis=1)
    .transpose()
)

print(df_vcost)

# %%

df_fcost = (
    pd.DataFrame(
        {
            'DET': {'CLEV': 1000, 'GARY': 1200, 'PITT': 1200},
            'FRA': {'CLEV': 2000, 'GARY': 3000, 'PITT': 2000},
            'FRE': {'CLEV': 3000, 'GARY': 3500, 'PITT': 3500},
            'LAF': {'CLEV': 2200, 'GARY': 2500, 'PITT': 2200},
            'LAN': {'CLEV': 1500, 'GARY': 1200, 'PITT': 1500},
            'STL': {'CLEV': 2500, 'GARY': 2500, 'PITT': 2500},
            'WIN': {'CLEV': 1200, 'GARY': 1200, 'PITT': 1500},
        }
    )
    .rename_axis('ORI', axis=0)
    .rename_axis('DEST', axis=1)
)

print(df_fcost)
# fmt: off

# %%
# Set up problem data
# -------------------

# %%

# Need to import the package, in some form, to directly cast pandas objects to our data structures

# %%
# Index-sets
# ^^^^^^^^^^

ORIG = df_supply.index.opti.to_indexset()

DEST = df_demand.index.opti.to_indexset()

PROD = df_supply.columns.opti.to_indexset()

# %%
# Parameters
# ^^^^^^^^^^

supply = df_supply.stack().opti.to_paramdict()

demand = df_demand.stack().opti.to_paramdict()

vcost = df_vcost.stack().opti.to_paramdict()

fcost = df_fcost.stack().opti.to_paramdict()

limit = 625

# %%
# Implement with DOcplex
# ----------------------

# %%
from docplex.mp.model import Model

from opti_extensions import IndexSetND
from opti_extensions.docplex import add_variables, solve

# Instantiate model
model = Model(name='multicommodity')

# Add variables
# Use `add_variables` from opti-extensions instead of `model.continuous_var_dict`
# & `model.binary_var_dict`
trans = add_variables(
    model,
    indexset=IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
    vartype='continuous',
    name='NUM-UNITS',
)
use = add_variables(
    model,
    indexset=IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
    vartype='binary',
    name='USE-ROUTE',
)

# Set objective
model.minimize(
    vcost @ trans + fcost @ use
)

# Add constraints
model.add_constraints_(
    (
        trans.sum(i, '*', p) == supply[i, p],
        f'supply_{i}_{p}',
    )
    for i in ORIG for p in PROD
)
model.add_constraints_(
    (
        trans.sum('*', j, p) == demand[j, p],
        f'demand_{j}_{p}',
    )
    for j in DEST for p in PROD
)
model.add_constraints_(
    (
        trans.sum(i, j, '*') <= limit * use[i,j],
        f'multi_{i}_{j}',
    )
    for i in ORIG for j in DEST
)

# Solve with additional logging output for problem and solution statistics
# Use `solve` from opti-extensions instead of `model.solve`
sol = solve(model, log_output=True)

# %%
sol.display(print_zeros=False)

# %%
# Implement with gurobipy
# -----------------------

from gurobipy import GRB, Model

from opti_extensions.gurobipy import addVars

# Instantiate model
model = Model(name='multicommodity')

# Add variables
# Use `addVars` from opti-extensions instead of `model.addVars`
trans = addVars(
    model,
    IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
    vtype=GRB.CONTINUOUS,
    name='NUM-UNITS',
)
use = addVars(
    model,
    IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
    vtype=GRB.BINARY,
    name='USE-ROUTE',
)

# Set objective
model.setObjective(
    vcost @ trans + fcost @ use,
    sense=GRB.MINIMIZE,
)

# Add constraints
model.addConstrs(
    (
        trans.sum(i, '*', p) == supply[i, p]
        for i in ORIG for p in PROD
    ),
    name='supply',
)
model.addConstrs(
    (
        trans.sum('*', j, p) == demand[j, p]
        for j in DEST for p in PROD
    ),
    name='demand',
)
model.addConstrs(
    (
        trans.sum(i, j, '*') <= limit * use[i, j]
        for i in ORIG for j in DEST
    ),
    name='multi',
)

# Solve
model.optimize()

# %%
model.printAttr('X')

# %%
# Implement with Xpress
# ---------------------

import xpress as xp

from opti_extensions.xpress import addVariables

# Instantiate problem
prob = xp.problem(name='multicommodity')

# Add variables
# Use `addVariables` from opti-extensions instead of `prob.addVariables`
trans = addVariables(
    prob,
    IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
    vartype=xp.continuous,
    name='NUM-UNITS',
)
use = addVariables(
    prob,
    IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
    vartype=xp.binary,
    name='USE-ROUTE',
)

# Set objective
prob.setObjective(
    vcost @ trans + fcost @ use,
    sense=xp.minimize,
)

# Add constraints
prob.addConstraint(
    trans.sum(i, '*', p) == supply[i, p]
    for i in ORIG for p in PROD
)
prob.addConstraint(
    trans.sum('*', j, p) == demand[j, p]
    for j in DEST for p in PROD
)
prob.addConstraint(
    trans.sum(i, j, '*') <= limit * use[i, j]
    for i in ORIG for j in DEST
)

# Solve
prob.optimize()

# %%
print(f'var: {"value" :>20}')
print('-' * 25)
for vd in (trans, use):
    for k, v in prob.getSolution(vd).items():
        if abs(v) > 1e-6:
            name = f'{vd.value_name}[{k}]:'
            print(f'{name:<15}  {v :>8.4f}')
