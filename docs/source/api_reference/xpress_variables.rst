Xpress variable functionality
#############################

.. note:: Provided through ``opti_extensions.xpress.*`` namespace.

.. currentmodule:: opti_extensions.xpress._var_funcs

Add variables
=============
.. autosummary::
   :toctree: ../auto_api/

   addVariables

.. currentmodule:: opti_extensions.xpress._var_dicts

VarDict1D
=========

Custom subclass of `dict` to store Xpress problem variables with 1-dim scalar keys.

.. autosummary::
   :toctree: ../auto_api/
   :nosignatures:

   VarDict1D

Attributes
----------
.. autosummary::

   VarDict1D.problem
   VarDict1D.vartype
   VarDict1D.key_name
   VarDict1D.value_name

Numerical operations
--------------------
.. autosummary::

   VarDict1D.sum
   VarDict1D.sum_squares
   VarDict1D.dot

The ``@`` operator
------------------

The matrix multiplication operator ``@`` can be used instead of the `dot`
method. Both ``ParamDict1D @ VarDict1D`` and ``VarDict1D @ ParamDict1D``
will produce the same result as ``VarDict1D.dot(ParamDict1D)``.

Mapping operations
------------------
.. autosummary::

   VarDict1D.get
   VarDict1D.lookup

Views
-----
- ``VarDict1D.items()``
- ``VarDict1D.keys()``
- ``VarDict1D.values()``

VarDictND
=========

Custom subclass of `dict` to store Xpress problem variables with N-dim tuple keys.

.. autosummary::
   :toctree: ../auto_api/
   :nosignatures:

   VarDictND

Attributes
----------
.. autosummary::

   VarDictND.problem
   VarDictND.vartype
   VarDictND.key_names
   VarDictND.value_name

Numerical operations
--------------------
.. autosummary::

   VarDictND.sum
   VarDictND.sum_squares
   VarDictND.dot

The ``@`` operator
------------------

The matrix multiplication operator ``@`` can be used instead of the `dot`
method. Both ``ParamDictND @ VarDictND`` and ``VarDictND @ ParamDictND``
will produce the same result as ``VarDictND.dot(ParamDictND)``.

Mapping operations
------------------
.. autosummary::

   VarDictND.get
   VarDictND.lookup

Efficient subset selection
--------------------------
.. autosummary::

   VarDictND.subset_keys
   VarDictND.subset_values

Views
-----
- ``VarDictND.items()``
- ``VarDictND.keys()``
- ``VarDictND.values()``
