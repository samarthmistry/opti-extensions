# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
P-median problem
================

We demonstrate how to implement the model for the p-median problem with DOcplex, gurobipy, and
Xpress along with the functionality from `opti-extensions`.

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/authors/marcos-dv/location/p_median.ipynb
— Copyright (c) 2022-2022, AMPL Optimization inc. (licensed under the MIT License)
"""

# %%
# Mathematical formulation
# ------------------------
#
# **Index-sets**:
#
# -  | Customers to be served:
#    | :math:`i \in CUST`
# -  | Facilities to consider:
#    | :math:`j \in FAC`
#
# **Parameters**:
#
# -  | Cost of supplying customer :math:`i` from facility :math:`j`:
#    | :math:`cost_{i, j} \in \mathbb{R}_{0}^{+} \quad \forall \; i \in CUST \; \& \; \forall \; j \in FAC`
# -  | Number of facilities to be opened:
#    | :math:`p \in \mathbb{R}^{+}`
#
# **Variables**:
#
# -  | Whether to serve customer :math:`i` from facility :math:`j`:
#    | :math:`x_{i, j} \in \mathbb{B} \quad \forall \; i \in CUST \; \& \; j \in FAC`
# -  | Whether to open facility :math:`j` or not:
#    | :math:`y_{j} \in \mathbb{B} \quad \forall \; j \in FAC`
#
# **Objective**:
#
# -  | Minimize the total cost of serving all customers:
#    | :math:`\min \; \sum_{i \in CUST} \sum_{j \in FAC} cost_{i, j} \times x_{i, j}`
#
# **Constraints**:
#
# -  | Each customer must be assigned to exactly one facility:
#    | :math:`\sum_{j \in FAC} x_{i, j} = 1, \; \forall \; i \in CUST`
# -  | Ensure that facility :math:`j` is open if it serves customer :math:`i`:
#    | :math:`x_{i, j} \leq y_{j}, \; \forall \; i \in CUST \; \& \; \forall \; j \in FAC`
# -  | :math:`p` facilities must be opened:
#    | :math:`\sum_{j \in FAC} y_{j} = p, \; \forall \; j \in FAC`

# %%
# Generate input data
# -------------------

# %%
import math
import random
from typing import NamedTuple

random.seed(27)


class Instance(NamedTuple):
    customers: list[int]
    facilities: list[int]
    cost: dict[tuple[int, int], float]
    p: int


def generate_instance(num_customers: int, num_facilities: int, p: int):
    customers = list(range(1, num_customers + 1))
    customer_coord = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in customers}

    facilities = list(range(num_customers, num_facilities + num_customers + 1))
    facility_coord = {j: (random.uniform(0, 100), random.uniform(0, 100)) for j in facilities}

    cost = {
        # Eucledian distance between customer `i` and facility `j`
        (i, j): round(math.sqrt((i_coord[0] - j_coord[0]) ** 2 + (i_coord[1] - j_coord[1]) ** 2), 2)
        for i, i_coord in customer_coord.items()
        for j, j_coord in facility_coord.items()
    }

    return Instance(customers, facilities, cost, p)


instance = generate_instance(5, 5, 2)

# %%
# Set up problem data
# -------------------

# %%
# Index-sets
# ^^^^^^^^^^

from opti_extensions import IndexSet1D, IndexSetND

CUST = IndexSet1D(instance.customers, name='CUST')

FAC = IndexSet1D(instance.facilities, name='FAC')

CUST_x_FAC = IndexSetND(CUST, FAC, names=('CUST', 'FAC'))

# %%
# Parameters
# ^^^^^^^^^^

from opti_extensions import ParamDictND

cost = ParamDictND(instance.cost, key_names=('CUST', 'FAC'), value_name='COST')

p = instance.p
# fmt: off


# %%
# Implement with DOcplex
# ----------------------

# %%
from docplex.mp.model import Model

from opti_extensions.docplex import add_variables, solve

# Instantiate model
model = Model(name='p-median')

# Add variables
# Use `add_variables` from opti-extensions instead of `model.binary_var_dict`
x = add_variables(model, indexset=CUST_x_FAC, vartype='binary', name='x')
y = add_variables(model, indexset=FAC, vartype='binary', name='y')

# Set objective
model.minimize(
    model.sum(cost[i, j] * x[i, j] for i in CUST for j in FAC)
)

# Add constraints
model.add_constraints_(
    x.sum(i, '*') == 1
    for i in CUST
)
model.add_constraints_(
    x[i, j] <= y[j]
    for i in CUST for j in FAC
)
model.add_constraint_(
    y.sum() == p
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
model = Model(name='p-median')

# Add variables
# Use `addVars` from opti-extensions instead of `model.addVars`
x = addVars(model, indexset=CUST_x_FAC, vtype=GRB.BINARY, name='x')
y = addVars(model, indexset=FAC, vtype=GRB.BINARY, name='y')

# Set objective
model.setObjective(
    quicksum(cost[i, j] * x[i, j] for i in CUST for j in FAC),
    sense=GRB.MINIMIZE
)

# Add constraints
model.addConstrs(
    x.sum(i, '*') == 1
    for i in CUST
)
model.addConstrs(
    x[i, j] <= y[j]
    for i, j in CUST_x_FAC
)
model.addConstr(
    y.sum() == p
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
prob = xp.problem(name='p-median')

# Add variables
# Use `addVariables` from opti-extensions instead of `prob.addVariables`
x = addVariables(prob, indexset=CUST_x_FAC, vartype=xp.binary, name='x')
y = addVariables(prob, indexset=FAC, vartype=xp.binary, name='y')

# Set objective
prob.setObjective(
    xp.Sum(cost[i, j] * x[i, j] for i in CUST for j in FAC),
    sense=xp.minimize
)

# Add constraints
prob.addConstraint(
    x.sum(i, '*') == 1
    for i in CUST
)
prob.addConstraint(
    x[i, j] <= y[j]
    for i, j in CUST_x_FAC
)
prob.addConstraint(
    y.sum() == p
)

# Solve
prob.optimize()

# %%
print(f'var: {"value" :>20}')
print('-' * 25)
for vd in (x, y):
    for k, v in prob.getSolution(vd).items():
        if abs(v) > 1e-6:
            name = f'{vd.value_name}[{k}]:'
            print(f'{name:<15}  {v :>8.4f}')
