# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
VarDict data structures
=======================

We give an overview of the VarDict data structures provided in `opti-extensions`. They
are immutable subclasses of Python's dict with some additional functionality.

Suppose we want build a model to solve the facility location problem. We'll define the
variables for this problem with these data structures.

.. note::

    We'll be using DOcplex here, but the same approach will work for gurobipy and Xpress.
"""

# %%

# Let's import the classes defining IndexSets, and the function that adds variables based on
# IndexSets and returns VarDicts
from opti_extensions import IndexSet1D, IndexSetND
from opti_extensions.docplex import add_variables

# We'll also work with dataframes and series
import pandas as pd

# %%
# Let's instantiate a DOcplex model
from docplex.mp.model import Model

mdl = Model()

# %%
# VarDict1D
# ---------

# %%
# Constructor
# ^^^^^^^^^^^

# %%
# The facility location problem defines binary selection variables indexed on the set of facilities.
# Let's define these with `add_variables` function that takes in an `IndexSet1D` and returns a
# `VarDict1D` for variables indexed on unidimensional sets. The VarDict keys will be as per the
# given IndexSet1D and the values will be the corresponding DOcplex variables.

# %%
# -  | Whether to open facility :math:`j` or not:
#    | :math:`y_{j} \in \mathbb{B} \quad \forall \; j \in FAC`

# %%

# Define the set of facilities
FAC = IndexSet1D(['F1', 'F2', 'F3'])

# Define the set of binary variables indexed over this set
select_fac = add_variables(mdl, indexset=FAC, vartype='binary')
# Type annotation of select_fac is `VarDict1D[str, docplex.mp.dvar.Var]`
print(select_fac)

# %%
# `key_name` & `value_name` attributes
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# It also has an optional `name` argument, which get stored as `value_name` attribute that can be
# referred to for various downstream uses. The input IndexSet1D's `name` attribute will get stored
# as the resulting VarDict's `key_name` attribute.

# %%

# When name argument is not specified
print(select_fac.key_name, select_fac.value_name)

# %%

# Specifying the name arguments, should be strings
# Define the set of facilities
FAC = IndexSet1D(['F1', 'F2', 'F3'], name='Facility')

# Define the set of binary variables indexed over this set
select_fac = add_variables(mdl, indexset=FAC, vartype='binary', name='Select')
print(select_fac)  # the names will also be added in the header of the string representation

# %%
print(select_fac.key_name, select_fac.value_name)

# %%

# Change the names with attribute assignment
select_fac.key_name = 'FAC'
select_fac.value_name = 'SELC'  # this will NOT change the var names in the model, just the VarDict
print(select_fac.key_name, select_fac.value_name)

# %%

# Simple use case
sol = mdl.new_solution()  # dummy solution; all zeros
sol_select_fac = sol.get_value_dict(select_fac)
s = pd.Series(sol_select_fac, name=select_fac.value_name).rename_axis(select_fac.key_name)
print(s)

# %%

# %%
# Basic methods
# ^^^^^^^^^^^^^

# %%
# VarDict1D is an immutable subclass of python's `dict` i.e., it does not allow any methods that
# update it once it's created: clear, pop, popitem, setdefault, update, fromkeys. Please refer to
# the `Mapping operations` and `Views` sections of `API Reference` for more details.
#
# It provides a special method `lookup` that returns variables for keys present in the
# VarDict1D and zero for keys not found i.e., equivalent to ``VarDict1D.get(key, 0)``. This is
# helpful when working with variables indexed on sparse sets.

# %%
print({j: select_fac.lookup(j) for j in ('F1', 'F2', 'F99')})

# %%
# Numerical operations
# ^^^^^^^^^^^^^^^^^^^^

# %%
# It has special methods to directly sum all variables and sum squares of all variables.

# %%
print(select_fac.sum())
print(select_fac.sum_squares())

# %%
# VarDictND
# ---------

# %%
# Constructor
# ^^^^^^^^^^^

# %%
# The facility location problem defines continuous demand allocation variables indexed on the set of
# customers and facilities. Let's define these with `add_variables` function that takes in an
# `IndexSetND` and returns a `VarDictND` for variables indexed on multidimensional sets. The VarDict
# keys will be as per the given IndexSetND and the values will be the corresponding DOcplex
# variables.

# %%
# -  | Amount of demand of customer :math:`i` served by facility :math:`j`:
#    | :math:`x_{i, j} \in \mathbb{R}_{0}^{+} \quad \forall \; (i, j) \in FAC\_CUST`

# %%

# Define the set of customers and facilities
FAC_CUST = IndexSetND(
    [('F1', 1), ('F1', 2), ('F2', 1), ('F2', 2), ('F3', 1), ('F3', 2)],
)

# Define the set of continuous variables indexed over this set
dem_alloc = add_variables(mdl, indexset=FAC_CUST, vartype='continuous')
# Type annotation of dem_alloc is `VarDict1D[tuple[str, int], docplex.mp.dvar.Var]`
print(dem_alloc)

# %%
# `key_names` & `value_name` attributes
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# It also has an optional `name` argument, which get stored as `value_name` attribute that can be
# referred to for various downstream uses. The input IndexSetND's `names` attribute will get stored
# as the resulting VarDict's `key_names` attribute.

# %%

# When name argument is not specified
print(dem_alloc.key_names, dem_alloc.value_name)

# %%

# Specifying the name arguments, should be strings
# Define the set of customers and facilities
FAC_CUST = IndexSetND(
    [('F1', 1), ('F1', 2), ('F2', 1), ('F2', 2), ('F3', 1), ('F3', 2)],
    names=('Facility', 'Customer'),
)

# Define the set of binary variables indexed over this set
dem_alloc = add_variables(mdl, indexset=FAC_CUST, vartype='continuous', name='Allocation')
print(dem_alloc)  # the names will also be added in the header of the string representation

# %%
print(dem_alloc.key_names, dem_alloc.value_name)

# %%

# Change the names with attribute assignment
dem_alloc.key_names = ('FAC', 'CUST')
dem_alloc.value_name = 'ALLOC'  # this will NOT change the var names in the model, just the VarDict
print(dem_alloc.key_names, dem_alloc.value_name)

# %%
# Simple use case
sol = mdl.new_solution()  # dummy solution; all zeros
sol_dem_alloc = sol.get_value_dict(dem_alloc)
s = pd.Series(dem_alloc, name=dem_alloc.value_name).rename_axis(dem_alloc.key_names)
print(s)

# %%
# Basic methods
# ^^^^^^^^^^^^^

# %%
# VarDictND is an immutable subclass of python's `dict` i.e., it does not allow any methods that
# update it once it's created: clear, pop, popitem, setdefault, update, fromkeys. Please refer to
# the `Mapping operations` and `Views` sections of `API Reference` for more details.
#
# It provides a special method `lookup` that returns variables for keys present in the
# VarDictND and zero for keys not found i.e., equivalent to ``VarDictND.get(key, 0)``. This is
# helpful when working with variables indexed on sparse sets.

# %%
print({(i, j): dem_alloc.lookup(i, j) for i in ('F1', 'F2') for j in (1, 99)})

# %%
# Efficient subset selection
# ^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# It has two special methods that allow us to efficiently get subsets: `subset_keys` and
# `subset_values`.

# %%

# If we only want keys/values of dem_alloc (indexed on a 2-dimensional set) that have the value
# 'F1' in the first dimension and any value in the second dimension, we can supply the wildcard
# pattern to the `subset_keys`/`subset_values` method as shown below.
#
# (the single-character string '*' is used as the wildcard to indicate all possible values for the
# given dimension).
#
print(dem_alloc.subset_keys('F1', '*'))
print(dem_alloc.subset_values('F1', '*'))

# %%

# If we only want keys/values of dem_alloc (indexed on a 2-dimensional set) that have any value in
# the first dimension and the value 1 in the second dimension
print('Subset method:', dem_alloc.subset_keys('*', 1))
print('Subset method:', dem_alloc.subset_values('*', 1))

# As compared to an if check inside a loop/comprehension
print('With if check:', [elem for elem in dem_alloc if elem[1] == 1])
print('With if check:', [val for elem, val in dem_alloc.items() if elem[1] == 1])

# %%
# Numerical operations
# ^^^^^^^^^^^^^^^^^^^^

# %%
# It has special methods to directly sum all (or a subset of) variables and sum squares of all (or a
# subset of) variables

# %%

# Sum all dem_alloc variables
print(dem_alloc.sum())

# %%

# Sum a subset of dem_alloc variables, that have the value 'F1' in the first dimension and any value in
# the second dimension, based on wildcard pattern
print(dem_alloc.sum('F1', '*'))

# %%

# Sum squares of all dem_alloc variables
print(dem_alloc.sum_squares())

# %%

# Sum squares of a subset of dem_alloc variables, that have the value 'F1' in the first dimension and any
# value in the second dimension, based on wildcard pattern
print(dem_alloc.sum_squares('F1', '*'))

# %%
# Not only does it provide a cleaner syntax, but it is also very performant because of an internal
# caching mechanism. Let's see for an example below:

# %%

from random import choice
from timeit import repeat, timeit

# We'll create a large VarDictND where the first dimension for each element is unique but the
# second dimension is not (many elements share common values in the second dimension)
test_set = IndexSetND((i, choice(range(99))) for i in range(500_000))
test_var = add_variables(mdl, indexset=test_set, vartype='continuous', name='TEST')

# %%

# While the first call of `sum` (or any other numerical op, or `subset_keys`, or `subset_values`)
# takes a some millisecs, subsequent calls are extremely fast
code = "subset_res1 = test_var.sum('*', 42)"

time = timeit(code, number=1, globals=globals())
print(f'Execution time: {1000 * time:08.3f} ms')

# %%

code = "subset_res2 = test_var.sum('*', 42)"

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = "subset_res3 = test_var.sum('*', 27)"

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = 'ifcheck_res = mdl.sum(v for k, v in test_var.items() if k[1] == 42)'

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = 'ifcheck_res = mdl.sum(v for k, v in test_var.items() if k[1] == 27)'

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%
# Individually, these micro-speedups may seem trivial, but in aggregate, they end up making a
# notable difference when building large-scale models.
