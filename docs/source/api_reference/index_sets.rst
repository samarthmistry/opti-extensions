Index-set functionality
#######################

.. note:: Provided through ``opti_extensions.*`` namespace.

.. currentmodule:: opti_extensions

IndexSet1D
==========

Custom `list`-like data structure to define index-sets with 1-dim scalar elements.

Constructor
-----------
.. autosummary::
   :toctree: ../auto_api/

   IndexSet1D

Attributes
----------
.. autosummary::

   IndexSet1D.name

Sequence operations
-------------------
.. autosummary::

   IndexSet1D.append
   IndexSet1D.extend
   IndexSet1D.insert
   IndexSet1D.remove
   IndexSet1D.pop
   IndexSet1D.clear
   IndexSet1D.index
   IndexSet1D.sort
   IndexSet1D.reverse

Set comparison
--------------

* If two sets have the same elements:

   >>> set_a == set_b

* If two sets have different elements:

   >>> set_a != set_b

* If one set is a subset of another:

   >>> set_a <= set_b

* If one set is a proper subset of another:

   >>> set_a < set_b

* If one set is a superset of another:

   >>> set_a >= set_b

* If one set is a proper superset of another:

   >>> set_a > set_b

Set operations
--------------

* If two sets are disjoint or not:

   >>> set_a.isdisjoint(set_b)

* Union of two or more sets:

   >>> set_a.union(set_b, ...)
   >>> set_a | set_b | ...

* Intersection of two or more sets:

   >>> set_a.intersection(set_b, ...)
   >>> set_a & set_b & ...

* Difference of two or more sets:

   >>> set_a.difference(set_b, ...)
   >>> set_a - set_b - ...

* Symmetric difference of two sets:

   >>> set_a.symmetric_difference(set_b)
   >>> set_a ^ set_b

Just like `set`, the non-operator versions of union(), intersection(),
difference(), and symmetric_difference() methods will accept any iterable as
an argument. In contrast, their operator based counterparts require their
arguments to be IndexSet1D.

Dunder methods
--------------
- ``IndexSet1D.__contains__``
- ``IndexSet1D.__iter__``
- ``IndexSet1D.__reversed__``
- ``IndexSet1D.__len__``
- ``IndexSet1D.__getitem__``
- ``IndexSet1D.__setitem__``
- ``IndexSet1D.__delitem__``
- ``IndexSet1D.__add__``
- ``IndexSet1D.__iadd__``

IndexSetND
==========

Custom `list`-like data structure to define index-sets with N-dim tuple elements.

Constructor
-----------
.. autosummary::
   :toctree: ../auto_api/

   IndexSetND

Attributes
----------
.. autosummary::

   IndexSetND.names

Efficient subset selection
--------------------------
.. autosummary::

   IndexSetND.subset
   IndexSetND.squeeze

Sequence operations
-------------------
.. autosummary::

   IndexSetND.append
   IndexSetND.extend
   IndexSetND.insert
   IndexSetND.remove
   IndexSetND.pop
   IndexSetND.clear
   IndexSetND.index
   IndexSetND.sort
   IndexSetND.reverse

Set comparison
--------------

* If two sets have the same elements:

  >>> set_a == set_b

* If two sets have different elements:

   >>> set_a != set_b

* If one set is a subset of another:

   >>> set_a <= set_b

   *A more efficient approach for sparse sets:*

   If ``set_a`` is a 3-dim set (of type IndexSetND) and is composed of sparse
   combinations of elements of three 1-dim sets ``set_x``, ``set_y``, and
   ``set_z`` respectively (each of type IndexSet1D). Then an efficient subset
   check for ``set_a`` can be directly made with a tuple of ``set_x``, ``set_y``,
   and ``set_z`` – without having to enumerate all possible combinations from
   the three.

   >>> set_a <= (set_x, set_y, set_z)

   Can raise the following errors:

   * ``LookupError``: If the IndexSetND is empty and checked with a tuple of
     IndexSet1D.

   * ``ValueError``: If the IndexSetND is checked with a tuple of IndexSet1D that
     is not the same length as the elements of the IndexSetND.

* If one set is a proper subset of another:

   >>> set_a < set_b

* If one set is a superset of another:

   >>> set_a >= set_b

* If one set is a proper superset of another:

   >>> set_a > set_b

Set operations
--------------

* If two sets are disjoint or not:

   >>> set_a.isdisjoint(set_b)

* Union of two or more sets:

   >>> set_a.union(set_b, ...)
   >>> set_a | set_b | ...

* Intersection of two or more sets:

   >>> set_a.intersection(set_b, ...)
   >>> set_a & set_b & ...

* Difference of two or more sets:

   >>> set_a.difference(set_b, ...)
   >>> set_a - set_b - ...

* Symmetric difference of two sets:

   >>> set_a.symmetric_difference(set_b)
   >>> set_a ^ set_b

Just like `set`, the non-operator versions of union(), intersection(),
difference(), and symmetric_difference() methods will accept any iterable as
an argument. In contrast, their operator based counterparts require their
arguments to be IndexSetND.

Dunder methods
--------------
- ``IndexSetND.__contains__``
- ``IndexSetND.__iter__``
- ``IndexSetND.__reversed__``
- ``IndexSetND.__len__``
- ``IndexSetND.__getitem__``
- ``IndexSetND.__setitem__``
- ``IndexSetND.__delitem__``
- ``IndexSetND.__add__``
- ``IndexSetND.__iadd__``

Casting from pandas Series/DataFrame/Index
==========================================

Methods to cast pandas Series/DataFrame/Index into IndexSet1D/IndexSetND are
provided through the custom ``.opti`` accessor.

.. currentmodule:: pandas

.. autosummary::
   :toctree: ../auto_api/
   :template: autosummary/accessor_method.rst

   Series.opti.to_indexset
   DataFrame.opti.to_indexset
   Index.opti.to_indexset
