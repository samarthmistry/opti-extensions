# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Diet problem
============

Please refer to chapter 2 in the `AMPL Book <https://ampl.com/learn/ampl-book>`_ for a
detailed description of the problem. We demonstrate how to implement this model
with DOcplex, gurobipy, and Xpress along with the functionality from `opti-extensions`.

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-lecture/diet_case_study.ipynb
— Copyright (c) 2022-2022, AMPL Optimization inc. (licensed under the MIT License)
"""

# %%
# Mathematical formulation
# ------------------------
#
# **Index-sets**:
#
# -  | Nutrients to consider:
#    | :math:`i \in NUTR`
# -  | Food items to consider:
#    | :math:`j \in FOOD`
#
# **Parameters**:
#
# -  | Cost of food item :math:`j`:
#    | :math:`cost_{j} \in \mathbb{R}^{+} \quad \forall \; j \in FOOD`
# -  | Minimum purchase quantity required for food item :math:`j`:
#    | :math:`f\_min_{j} \in \mathbb{R}_{0}^{+} \quad \forall \; j \in FOOD`
# -  | Maximum purchase quantity allowed for food item :math:`j`:
#    | :math:`f\_max_{j} \in \mathbb{R}_{0}^{+} \quad \forall \; j \in FOOD`
# -  | Minimum amount required of nutrient :math:`i`:
#    | :math:`n\_min_{i} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in NUTR`
# -  | Maximum amount required of nutrient :math:`i`:
#    | :math:`n\_max_{i} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in NUTR`
# -  | Amount of nutrient :math:`i` in food item :math:`j`:
#    | :math:`amt_{i, j} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in NUTR \; \& \; \forall \; j \in FOOD`
#
# **Variables**:
#
# -  | Quantity of food item :math:`j` to be purchased:
#    | :math:`buy_{j} \in \mathbb{R}_{0}^{+} (\geq f\_min_{j}, \leq f\_max_{j}) \quad \forall \; j \in FOOD`
#
# **Objective**:
#
# -  | Minimize the total cost of the diet:
#    | :math:`\min \; \sum_{j \in FOOD} cost_{j} \times buy_{j}`
#
# **Constraints**:
#
# -  | Ensure that the nutritional limits are satisfied by the diet:
#    | :math:`n\_min_{i} \leq \sum_{j \in FOOD} amt_{i, j} \times buy_{j} \leq n\_max_{i}, \; \forall \; i \in NUTR`

# %%
# Set up problem data
# -------------------

# %%
# Index-sets
# ^^^^^^^^^^

from opti_extensions import IndexSet1D

NUTR = IndexSet1D(['A', 'B1', 'B2', 'C'], name='NUTRIENT')

FOOD = IndexSet1D(['BEEF', 'CHK', 'FISH', 'HAM', 'MCH', 'MTL', 'SPG', 'TUR'], name='FOOD')

# %%
# Parameters
# ^^^^^^^^^^

from opti_extensions import ParamDict1D, ParamDictND

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

n_min = ParamDict1D(
    {'A': 700, 'C': 700, 'B1': 700, 'B2': 700},
    key_name='NUTRIENT',
    value_name='MIN-AMT',
)

n_max = ParamDict1D(
    {'A': 10000, 'C': 10000, 'B1': 10000, 'B2': 10000},
    key_name='NUTRIENT',
    value_name='MAX-AMT',
)

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
# fmt: off


# %%
# Implement with DOcplex
# ----------------------

# %%
from docplex.mp.model import Model

from opti_extensions.docplex import add_variables, solve

# Instantiate model
model = Model(name='diet')

# Add variables
# Use `add_variables` from opti-extensions instead of `model.continuous_var_dict`
buy = add_variables(model, indexset=FOOD, vartype='continuous', lb=f_min, ub=f_max, name='BUY-QTY')

# Set objective
model.minimize(
    model.sum(cost[j] * buy[j] for j in FOOD)
)

# Add constraints
model.add_constraints_(
    (
        model.sum(amt[i, j] * buy[j] for j in FOOD) >= n_min[i],
        f'min-nutr-reqd_{i}',
    )
    for i in NUTR
)
model.add_constraints_(
    (
        model.sum(amt[i, j] * buy[j] for j in FOOD) <= n_max[i],
        f'max-nutr-allwd_{i}',
    )
    for i in NUTR
)

# Solve with additional logging output for problem and solution statistics
# Use `solve` from opti-extensions instead of `model.solve`
sol = solve(model, log_output=True)

# %%
sol.display(print_zeros=False)

# %%
# Implement with gurobipy
# -----------------------

from gurobipy import GRB, Model, quicksum

from opti_extensions.gurobipy import addVars

# Instantiate model
model = Model(name='diet')

# Add variables
# Use `addVars` from opti-extensions instead of `model.addVars`
buy = addVars(model, indexset=FOOD, lb=f_min, ub=f_max, vtype=GRB.CONTINUOUS, name='BUY-QTY')

# Set objective
model.setObjective(
    quicksum(cost[j] * buy[j] for j in FOOD),
    sense=GRB.MINIMIZE
)

# Add constraints
model.addConstrs(
    (quicksum(amt[i, j] * buy[j] for j in FOOD) >= n_min[i] for i in NUTR),
    name='min-nutr-reqd',
)
model.addConstrs(
    (quicksum(amt[i, j] * buy[j] for j in FOOD) <= n_max[i] for i in NUTR),
    name='max-nutr-allwd',
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
prob = xp.problem(name='diet')

# Add variables
# Use `addVariables` from opti-extensions instead of `prob.addVariables`
buy = addVariables(prob, indexset=FOOD, vartype=xp.continuous, lb=f_min, ub=f_max, name='BUY-QTY')

# Set objective
prob.setObjective(
    xp.Sum(cost[j] * buy[j] for j in FOOD),
    sense=xp.minimize
)

# Add constraints
prob.addConstraint(
    xp.Sum(amt[i, j] * buy[j] for j in FOOD) >= n_min[i]
    for i in NUTR
)
prob.addConstraint(
    xp.Sum(amt[i, j] * buy[j] for j in FOOD) <= n_max[i]
    for i in NUTR
)

# Solve
prob.optimize()

# %%
print(f'var: {"value" :>20}')
print('-' * 25)
for k, v in prob.getSolution(buy).items():
    if abs(v) > 1e-6:
        name = f'{buy.value_name}[{k}]:'
        print(f'{name:<15}  {v :>8.4f}')
