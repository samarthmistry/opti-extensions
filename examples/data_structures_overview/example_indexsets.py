# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
IndexSet data structures
========================

We give an overview of the IndexSet data structures provided in `opti-extensions`. They
operate exactly like Python's list (but require all elements to be unique) and have some
additional functionality.

Suppose we want build a model to solve the facility location problem. We'll define the
sets for this problem with these data structures.
"""

# %%

# Let's import the classes defining IndexSets
# To show fail cases
import traceback

# We'll also work with dataframes and series
import pandas as pd

from opti_extensions import IndexSet1D, IndexSetND

# %%
# IndexSet1D
# ----------

# %%
# Constructor
# ^^^^^^^^^^^

# %%
# The facility location problem is usually defined with two unidimensional sets: Facilities
# and Customers. Let's define them with the `IndexSet1D` data structure which, as the name
# suggests, should be used for unidimensional sets. The elements can be 'scalar' data types
# such as `int`, `str`, `pd.Timestamp`, etc.

# %%
# -  | Customers to be served, described by id(s):
#    | :math:`i \in CUST`

# %%

# If we want to define for a range on numbers
CUST = IndexSet1D(range(5))
# Type annotation of CUST is `IndexSet1D[int]`
print(CUST)

# %%

# If we want to define for a sequence of numbers such as a list or tuple or set
CUST = IndexSet1D([1, 2, 3, 4, 5])  # IndexSet1D((1, 2, 3, 4, 5)) # IndexSet1D({1, 2, 3, 4, 5})
print(CUST)

# %%
# -  | Facilities to consider, described by code(s):
#    | :math:`j \in FAC`

# %%

# If we want to define for a sequence of strings
FAC = IndexSet1D(['F1', 'F2', 'F3'])
# Type annotation of FAC is `IndexSet1D[str]`
print(FAC)

# %%
# Fail cases
# ^^^^^^^^^^

# %%

# Will raise an error if input contains non-scalar element(s)
try:
    IndexSet1D(['F1', 'F2', ('F3', 'F4')])
    #        Non-scalar ->  ^^^^^^^^^^^^
except TypeError:
    traceback.print_exc()

# %%

# Will raise an error if input includes duplicates
try:
    IndexSet1D(['F1', 'F2', 'F2'])
    #  Duplicates ->  ^^^^  ^^^^
except ValueError:
    traceback.print_exc()

# %%
# `name` attribute
# ^^^^^^^^^^^^^^^^

# %%
# It also has an optional `name` argument, which gets stored as an attribute that can be referred to
# for various downstream uses.

# %%

# Without specifying the name argument
FAC = IndexSet1D(['F1', 'F2', 'F3'])  # equivalent to `name=None`
print(FAC)

# %%
print(FAC.name)

# %%

# Specifying the name argument, should be a string
FAC = IndexSet1D(['F1', 'F2', 'F3'], name='Facilities')
print(FAC)  # the name will also be added in the header of the string representation

# %%
print(FAC.name)

# %%

# Change the name with attribute assignment
FAC.name = 'FAC'
print(FAC.name)

# %%

# Simple use case 1
print(f'Elements of set {FAC.name} are -> ' + ', '.join(FAC))

# %%

# Simple use case 2
s = pd.Series(FAC, name=FAC.name)
print(s)

# %%
# Basic methods
# ^^^^^^^^^^^^^

# %%
# It supports all methods of python's `list`. Please refer to the
# `Sequence operations <../../api_reference/index_sets.html#sequence-operations>`__ and
# `Dunder methods <../../api_reference/index_sets.html#dunder-methods>`__ sections of
# `API Reference` for more details.
#
# It also supports rich/symbolic comparisons like python's `set`. Please refer to the
# `Set comparison <../../api_reference/index_sets.html#set-comparison>`__ section of
# `API Reference` for more details.

# %%
# IndexSetND
# ----------

# %%
# Constructor
# ^^^^^^^^^^^

# %%
# We can define a two-dimensional set with the `IndexSetND` data structure which, as the name
# suggests, should be used for multidimensional sets. The elements should be tuples of 'scalar'
# data types such as `int`, `str`, `pd.Timestamp`, etc. (with each tuple element having the same
# length).

# %%
# -  | Allowable combinations of facilities and customers:
#    | :math:`(i, j) \in FAC\_CUST`

# %%

# If we want to define for a sequence of tuples such as a list or tuple or set
FAC_CUST = IndexSetND(
    [('F1', 1), ('F1', 2), ('F2', 1), ('F2', 2), ('F3', 1), ('F3', 2)],
)
# Type annotation of FAC_CUST is `IndexSetND[tuple[str, int]]`
print(FAC_CUST)

# %%

FAC = IndexSet1D(['F1', 'F2', 'F3'])
CUST = IndexSet1D([1, 2])

# If we want to define for all possible combinations of two IndexSet1Ds
FAC_CUST = IndexSetND(FAC, CUST)
print(FAC_CUST)

# %%

# .. or all possible combinations of two iterables (such as range or list or tuple or set)
FAC_CUST = IndexSetND(['F1', 'F2', 'F3'], range(2))
print(FAC_CUST)

# %%
# Fail cases
# ^^^^^^^^^^

# %%

# Will raise an error if input contains scalar element(s)
try:
    IndexSetND([('F1', 1), ('F1', 1), ('F2', 1), 'F2', 2])
    #                                Scalars ->  ^^^^ ^^^
except TypeError:
    traceback.print_exc()

# %%

# Will raise an error if input contains tuple elements of different lengths
try:
    IndexSetND([('F1', 1), ('F2', 1), ('F1', 1), ('F2', 2, 'A')])
    #              Tuple of different length ->  ^^^^^^^^^^^^^^
except ValueError:
    traceback.print_exc()

# %%

# Will raise an error if input includes duplicates
try:
    IndexSetND([('F1', 1), ('F2', 1), ('F2', 1), ('F2', 2)])
    #       Duplicates ->  ^^^^^^^^^  ^^^^^^^^^
except ValueError:
    traceback.print_exc()

# %%
# `names` attribute
# ^^^^^^^^^^^^^^^^^

# %%
# It also has an optional `names` argument, which gets stored as an attribute that can be referred
# to for various downstream uses.

# %%

# Without specifying the name argument
FAC_CUST = IndexSetND(['F1', 'F2', 'F3'], range(2))  # equivalent to `name=None`
print(FAC_CUST)

# %%
print(FAC_CUST.names)

# %%

# Specifying the names argument, should be a sequence of strings
FAC_CUST = IndexSetND(['F1', 'F2', 'F3'], range(2), names=['FAC', 'CUST'])
print(FAC_CUST)  # the name will also be added in the header of the string representation

# %%
print(FAC_CUST.names)

# %%
# Change the name with attribute assignment
FAC_CUST.names = ['Facilities', 'Customers']
print(FAC_CUST.names)

# %%
# Simple use case
df = pd.DataFrame(FAC_CUST, columns=FAC_CUST.names)
print(df)

# %%
# Basic methods
# ^^^^^^^^^^^^^

# %%
# It supports all methods of python's `list`. Please refer to the
# `Sequence operations <../../api_reference/index_sets.html#id4>`__ and
# `Dunder methods <../../api_reference/index_sets.html#id5>`__ sections
# of `API Reference` for more details.
#
# It also supports rich/symbolic comparisons like python's `set`. Please refer to the
# `Set comparison <../../api_reference/index_sets.html#id3>`__ section of
# `API Reference` for more details.


# %%
# Efficient subset selection
# ^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# It has two special methods that allow us to efficiently get subsets: `subset` and `squeeze`.

# %%
# `subset` method
# """""""""""""""

# %%

# If we only want elements of FAC_CUST (a 2-dimensional set) that have the value 'F1' in the first
# dimension and any value in the second dimension, we can supply the wildcard pattern to the
# `subset` method as shown below.
#
# (the single-character string '*' is used as the wildcard to indicate all possible values for the
# given dimension).
#
print(FAC_CUST.subset('F1', '*'))

# %%

# If we only want elements of FAC_CUST (a 2-dimensional set) that have any value in the first
# dimension and the value 1 in the second dimension
print('Subset method:', FAC_CUST.subset('*', 1))

# As compared to an if check inside a loop/comprehension
print('With if check:', [elem for elem in FAC_CUST if elem[1] == 1])

# %%
# Not only does it provide a cleaner syntax, but it is also very performant because of an internal
# caching mechanism. Let's see for an example below:

# %%

from random import choice
from timeit import repeat, timeit

# We'll create a large IndexSetND where the first two dimensions are unique for each element but the
# third dimension is not (many elements share common values in the third dimension)
test_set = IndexSetND((i, str(i), choice(range(99))) for i in range(1_000_000))

# %%

# While the first call of `subset` takes a some millisecs, subsequent calls are extremely fast
code = "subset_res1 = test_set.subset('*', '*', 42)"

time = timeit(code, number=1, globals=globals())
print(f'Execution time: {1000 * time:08.3f} ms')

# %%

code = "subset_res2 = test_set.subset('*', '*', 42)"

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = "subset_res3 = test_set.subset('*', '*', 27)"

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = 'ifcheck_res = [elem for elem in test_set if elem[2] == 42]'

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%

code = 'ifcheck_res = [elem for elem in test_set if elem[2] == 27]'

times = repeat(code, number=10, repeat=5, globals=globals())
print(f'Execution time: {1000 * sum(times) / len(times):08.3f} ms')

# %%
# Individually, these micro-speedups may seem trivial, but in aggregate, they end up making a
# notable difference when building large-scale models.

# %%
# `squeeze` method
# """"""""""""""""

# %%

# From FAC_CUST (a 2-dimensional set), if we want to get an IndexSet of all
# unique values at the first dimension (i.e., at dimension 0 because Python
# uses zero-based indexing)
print(FAC_CUST.squeeze(0))

# %%

# From FAC_CUST (a 2-dimensional set), if we want to get an IndexSet of all
# unique values at the second dimension (i.e., at dimension 1 because Python
# uses zero-based indexing)
print(FAC_CUST.squeeze(1, names=['CUST']))

# %%
# Integration with `pandas`
# -------------------------

# %%
# opti-extensions provides optional functionality to directly cast pandas Series/DataFrame/Index
# objects into IndexSet data structures.  If pandas is present in the python environment, this
# functionality will be registered with a custom ``.opti`` accessor when opti-extensions is
# imported.
#
# Note: The opti-extensions package has to be imported first to use this method with pandas.

# %%

# Say, we have data for the problem in form of a pandas dataframe
data = pd.DataFrame(
    {
        'FAC': ['F0', 'F0', 'F0', 'F1', 'F2', 'F2', 'F2', 'F3', 'F3', 'F3', 'F4', 'F4'],
        'CUST': [2, 3, 4, 1, 0, 3, 4, 2, 3, 4, 0, 1],
        'COST': [119, 144, 185, 261, 230, 102, 192, 169, 116, 138, 126, 100],
    },
)
print(data)

# %%

# To directly get the set of facilities in form of IndexSet1D
# (pd.Series to IndexSet1D)
s_FAC = data.FAC.drop_duplicates()  # need to drop duplicates
print(s_FAC.opti.to_indexset())

# %%

# To directly get the set of customers in form of IndexSet1D
# (single column pd.DataFrame to IndexSet1D)
df_CUST = data[['CUST']].drop_duplicates()  # need to drop duplicates
print(df_CUST.opti.to_indexset())

# %%

# To directly get the set of allowed combinations of facilities & customers in form of IndexSetND
# (pd.DataFrame to IndexSetND)
df_FAC_CUST = data[['FAC', 'CUST']]
print(df_FAC_CUST.opti.to_indexset())

# %%

# ... or
# (pd.Index to IndexSetND)
ix_FAC_CUST = data.set_index(['FAC', 'CUST']).index
print(ix_FAC_CUST.opti.to_indexset())
