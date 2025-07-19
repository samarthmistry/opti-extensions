# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
ParamDict data structures
=========================

We give an overview of the ParamDict data structures provided in opti-extensions. They
are subclasses of Python's dict with some additional functionality.

Suppose we want build a model to solve the facility location problem. We'll define the
parameters for this problem with these data structures.
"""

# %%

# Let's import the classes defining IndexSets & ParamDicts
from opti_extensions import ParamDict1D, ParamDictND

# To show fail cases
import traceback

# We'll also work with dataframes and series
import pandas as pd

# %%
# ParamDict1D
# -----------

# %%
# Constructor
# ^^^^^^^^^^^

# %%
# The facility location problem is usually solved with customer-level demand data i.e., values
# indexed on the set of customers. Let's define it with `ParamDict1D` data structure which, as the
# name suggests, should be used for parameters indexed unidimensional sets. The ParamDict keys
# should be 'scalar' data types such as `int`, `str`, `pd.Timestamp`, etc. and the values should be
# `int` or `float`.

# %%
# .. tip::
#
#     **Type annotations**: Being a subclass of Python's `dict`, `ParamDict1D` is also a generic
#     container type and can be annotated accordingly. Additionally, opti-extensions provides a
#     type-complete interface, enabling most type checkers and LSPs to infer the type automatically.

# %%
# **Demand of customer :math:`i`:** :math:`dem_{i} \in \mathbb{R}^{+} \quad \forall \; i \in CUST`

# %%

# Each key is customer id, each value is units of demand
DEM = ParamDict1D(
    {0: 215, 1: 138, 2: 240, 3: 134, 4: 149},
)
print(DEM)

# %%
# Type annotation of `DEM` is `ParamDict1D[int, int]`, similar to `dict[int, int]`.

# %%
# Fail cases
# ^^^^^^^^^^

# %%

# Will raise an error if any key(s) are non-scalar element(s)
try:
    ParamDict1D({0: 215, 1: 138, 2: 240, 3: 134, (4, 5): 149})
    #                             Non-scalar ->  ^^^^^^
except TypeError:
    traceback.print_exc()

# %%

# Will raise an error if any value(s) are not int or float
try:
    ParamDict1D({0: 215, 1: 138, 2: 240, 3: 134, 4: '149'})
    #                          Not int or float ->  ^^^^^
except TypeError:
    traceback.print_exc()

# %%
# `key_name` & `value_name` attributes
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# It also has optional `key_name` & `value_name` arguments, which get stored as attributes that can
# be referred to for various downstream uses.

# %%

# Without specifying the name arguments
DEM = ParamDict1D(
    {0: 215, 1: 138, 2: 240, 3: 134, 4: 149}
)  # equivalent to `key_name=None, value_name=None`
print(DEM)

# %%
print(DEM.key_name, DEM.value_name)

# %%

# Specifying the name arguments, should be strings
DEM = ParamDict1D(
    {0: 215, 1: 138, 2: 240, 3: 134, 4: 149},
    key_name='Customer',
    value_name='Demand',
)
print(DEM)  # the names will also be added in the header of the string representation

# %%
print(DEM.key_name, DEM.value_name)

# %%

# Change the names with attribute assignment
DEM.key_name = 'CUST'
DEM.value_name = 'DEM'
print(DEM.key_name, DEM.value_name)

# %%

# Simple use case 1
print(f'({DEM.key_name}: {DEM.value_name}) -> ' + ', '.join(f'({k}: {v})' for k, v in DEM.items()))

# %%

# Simple use case 2
s_cost = pd.Series(DEM, name=DEM.value_name).rename_axis(DEM.key_name)
print(s_cost)

# %%
# Basic methods
# ^^^^^^^^^^^^^

# %%
# Being a subclass, it provides all methods of python's `dict`. Please refer to the
# `Mapping operations <../../api_reference/parameters.html#mapping-operations>`__ and
# `Views <../../api_reference/parameters.html#views>`__ sections of `API Reference` for more
# details.
#
# It provides a special method `lookup` that returns parameter values for keys present in the
# ParamDict1D and zero for keys not found i.e., equivalent to ``ParamDict1D.get(key, 0)``. This
# is helpful when working with parameters indexed on sparse sets.

# %%
print({i: DEM.lookup(i) for i in (0, 1, 99)})

# %%
# Numerical operations
# ^^^^^^^^^^^^^^^^^^^^

# %%
# It has special methods for numerical operations over parameter values.

# %%
print(f'{DEM.sum() = }')
print(f'{DEM.min() = }')
print(f'{DEM.max() = }')
print(f'{DEM.mean() = }')
print(f'{DEM.median() = }')
print(f'{DEM.median_low() = }')
print(f'{DEM.median_high() = }')

# %%
# ParamDictND
# -----------

# %%
# .. tip::
#
#     **Type annotations**: Being a subclass of Python's `dict`, `ParamDictND` is also a generic
#     container type and can be annotated accordingly. Additionally, opti-extensions provides a
#     type-complete interface, enabling most type checkers and LSPs to infer the type automatically.

# %%
# Constructor
# ^^^^^^^^^^^

# %%
# The facility location problem is usually solved with customer-facility cost data i.e., values
# indexed on the set of customers & facilities. Let's define it with `ParamDictND` data structure
# which, as the name suggests, should be used for parameters indexed unidimensional sets. The
# ParamDict keys should be tuples of 'scalar' data types such as `int`, `str`, `pd.Timestamp`, etc.
# (with each tuple element having the same length) and the values should be `int` or `float`.

# %%
# **Cost of supplying customer :math:`i` from facility :math:`j`:**
# :math:`cost_{i, j} \in \mathbb{R}^{+} \quad \forall \; (i, j) \in FAC\_CUST`

# %%

# Each key is a tuple of facility code & customer id, each value is cost
COST = ParamDictND(
    {('F1', 1): 197, ('F1', 2): 345, ('F2', 1): 99, ('F2', 2): 270, ('F3', 1): 205, ('F3', 2): 360},
)
print(COST)

# %%
# Type annotation of `COST` is `ParamDictND[tuple[str, int], int]`, similar to
# `dict[tuple[str, int], int]`.

# %%
# Fail cases
# ^^^^^^^^^^

# %%

# Will raise an error if any key(s) are scalar element(s)
try:
    ParamDictND({('F1', 1): 197, ('F1', 2): 345, ('F2', 1): 99, ('F3', 1): 205, 'F3': 360})
    #                                                                Scalar ->  ^^^^
except TypeError:
    traceback.print_exc()

# %%

# Will raise an error if any value(s) are not int or float
try:
    ParamDictND({('F1', 1): 197, ('F1', 2): 345, ('F2', 1): 99, ('F3', 1): 205, ('F3', 2): '300'})
    #                                                                 Not int or float ->  ^^^^^
except TypeError:
    traceback.print_exc()


# %%
# `key_names` & `value_name` attributes
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# It also has optional `key_name` & `value_name` arguments, which get stored as attributes that can
# be referred to for various downstream uses.

# %%

# Without specifying the name arguments
COST = ParamDictND(
    {('F1', 1): 197, ('F1', 2): 345, ('F2', 1): 99, ('F2', 2): 270, ('F3', 1): 205, ('F3', 2): 360}
)  # equivalent to `key_names=None, value_name=None`
print(COST)

# %%
print(COST.key_names, COST.value_name)

# %%

# Specifying the name arguments, should be strings
COST = ParamDictND(
    {('F1', 1): 197, ('F1', 2): 345, ('F2', 1): 99, ('F2', 2): 270, ('F3', 1): 205, ('F3', 2): 360},
    key_names=('Facility', 'Customer'),
    value_name='Cost',
)
print(COST)  # the names will also be added in the header of the string representation

# %%
print(COST.key_names, COST.value_name)

# %%

# Change the names with attribute assignment
COST.key_names = ('FAC', 'CUST')
COST.value_name = 'COST'
print(COST.key_names, COST.value_name)

# %%
# Simple use case
s_cost = pd.Series(COST, name=COST.value_name).rename_axis(COST.key_names)
print(s_cost)

# %%
# Basic methods
# ^^^^^^^^^^^^^

# %%
# Being a subclass, it provides all methods of python's `dict`. Please refer to the
# `Mapping operations <../../api_reference/parameters.html#id4>`__ and
# `Views <../../api_reference/parameters.html#id5>`__ sections of `API Reference` for more
# details.
#
# It provides a special method `lookup` that returns parameter values for keys present in the
# ParamDictND and zero for keys not found i.e., equivalent to ``ParamDictND.get(key, 0)``. This
# is helpful when working with parameters indexed on sparse sets.

# %%
print({(i, j): COST.lookup(i, j) for i in ('F1', 'F2') for j in (1, 99)})

# %%
# Efficient subset selection
# ^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# It has two special methods that allow us to efficiently get subsets: `subset_keys` and
# `subset_values`.

# %%

# If we only want keys/values of COST (indexed on a 2-dimensional set) that have the value
# 'F1' in the first dimension and any value in the second dimension, we can supply the wildcard
# pattern to the `subset_keys`/`subset_values` method as shown below.
#
# (the single-character string '*' is used as the wildcard to indicate all possible values for the
# given dimension).
#
print(COST.subset_keys('F1', '*'))
print(COST.subset_values('F1', '*'))

# %%

# If we only want keys/values of COST (indexed on a 2-dimensional set) that have any value in the
# first dimension and the value 1 in the second dimension
print('Subset method:', COST.subset_keys('*', 1))
print('Subset method:', COST.subset_values('*', 1))

# As compared to an if check inside a loop/comprehension
print('With if check:', [elem for elem in COST if elem[1] == 1])
print('With if check:', [val for elem, val in COST.items() if elem[1] == 1])

# %%
# Numerical operations
# ^^^^^^^^^^^^^^^^^^^^

# %%
# It has special methods for numerical operations over all or a subset of parameter values.

# %%

# Numerical operations over all parameter values of COST
print(f'{COST.sum() = }')
print(f'{COST.min() = }')
print(f'{COST.max() = }')
print(f'{COST.mean() = }')
print(f'{COST.median() = }')
print(f'{COST.median_low() = }')
print(f'{COST.median_high() = }')

# %%

# Numerical operations over a subset of parameter values, that have the value 'F1' in the first
# dimension and any value in the second dimension of COST, based on wildcard pattern
print(f'{COST.sum("F1", "*") = }')
print(f'{COST.min("F1", "*") = }')
print(f'{COST.max("F1", "*") = }')
print(f'{COST.mean("F1", "*") = }')
print(f'{COST.median("F1", "*") = }')
print(f'{COST.median_low("F1", "*") = }')
print(f'{COST.median_high("F1", "*") = }')

# %%
# Not only does it provide a cleaner syntax, but it is also very performant because of an internal
# caching mechanism. Let's see for an example below:

# %%

from random import choice
from timeit import repeat, timeit

# We'll create a large ParamDictND where the first dimension for each element is unique but the
# second dimension is not (many elements share common values in the second dimension)
test_param = ParamDictND(
    {(i, choice(range(99))): choice(range(10)) for i in range(1_000_000)},
)

# %%

# While the first call of `sum` (or any other numerical op, or `subset_keys`, or `subset_values`)
# takes a some millisecs, subsequent calls are extremely fast
code = "subset_res1 = test_param.sum('*', 42)"

time = timeit(code, number=1, globals=globals())
print(f'Execution time: {1000 * time:08.3f} ms')

# %%

code = "subset_res2 = test_param.sum('*', 42)"

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = "subset_res3 = test_param.sum('*', 27)"

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = 'ifcheck_res = sum(v for k, v in test_param.items() if k[1] == 42)'

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = 'ifcheck_res = sum(v for k, v in test_param.items() if k[1] == 27)'

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%
# Individually, these micro-speedups may seem trivial, but in aggregate, they end up making a
# notable difference when building large-scale models.

# %%
# Integration with `pandas`
# -------------------------

# %%
# opti-extensions provides optional functionality to directly cast pandas Series/DataFrame/Index
# objects into ParamDict data structures. If pandas is present in the python environment, this
# functionality will be registered with a custom ``.opti`` accessor when opti-extensions is
# imported.

# %%
# .. tip::
#
#     **Type annotations**: Since this functionality is registered at runtime, Python type checkers
#     and LSPs that use static type checking cannot automatically infer the types. The user will
#     need to annotate the ParamDict data structures created through these methods for type
#     checking.

# %%

# Say, we have demand data for the problem in form of a pandas dataframe
data1 = pd.DataFrame({'CUST': [0, 1, 2, 3, 4], 'DEM': [215, 138, 240, 134, 149]})
print(data1)

# %%

# To directly get the demand parameter in form of ParamDict1D
# (pd.Series to ParamDict1D)
#   index labels: ParamDict keys,
#   series values: ParamDict values
s_dem = data1.set_index('CUST').DEM
print(s_dem.opti.to_paramdict())

# %%

# To directly get the demand parameter in form of ParamDict1D
# (single column pd.DataFrame to ParamDict1D)
#   index labels: ParamDict keys,
#   series values: ParamDict values
df_dem = data1.set_index('CUST')[['DEM']]
print(df_dem.opti.to_paramdict())


# %%

# Say, we have cost data for the problem in form of a pandas dataframe
data2 = pd.DataFrame(
    {
        'FAC': ['F0', 'F0', 'F0', 'F1', 'F2', 'F2', 'F2', 'F3', 'F3', 'F3', 'F4', 'F4'],
        'CUST': [2, 3, 4, 1, 0, 3, 4, 2, 3, 4, 0, 1],
        'COST': [119, 144, 185, 261, 230, 102, 192, 169, 116, 138, 126, 100],
    },
)
print(data2)

# %%

# To directly get the cost parameter in form of ParamDictND
# (pd.Series to ParamDictND)
#   index labels: ParamDict keys,
#   series values: ParamDict values
s_cost = data2.set_index(['FAC', 'CUST']).COST
print(s_cost.opti.to_paramdict())

# %%

# To directly get the set of cost parameter in form of ParamDictND
# (single column pd.DataFrame to ParamDictND)
#   index labels: ParamDict keys,
#   dataframe column values: ParamDict values
df_cost = data2.set_index(['FAC', 'CUST'])[['COST']]
print(df_cost.opti.to_paramdict())
