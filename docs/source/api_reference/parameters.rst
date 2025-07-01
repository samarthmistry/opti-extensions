Parameter functionality
#######################

.. note:: Provided through ``opti_extensions.*`` namespace.

.. currentmodule:: opti_extensions

ParamDict1D
===========

Custom subclass of `dict` to define parameters with 1-dim scalar keys.

Constructor
-----------
.. autosummary::
   :toctree: ../auto_api/

   ParamDict1D

Attributes
----------
.. autosummary::

   ParamDict1D.key_name
   ParamDict1D.value_name

Numerical operations
--------------------
.. autosummary::

   ParamDict1D.sum
   ParamDict1D.min
   ParamDict1D.max
   ParamDict1D.mean
   ParamDict1D.median
   ParamDict1D.median_high
   ParamDict1D.median_low

Mapping operations
------------------
.. autosummary::

   ParamDict1D.clear
   ParamDict1D.get
   ParamDict1D.lookup
   ParamDict1D.pop
   ParamDict1D.popitem
   ParamDict1D.setdefault

Views
-----
- ``ParamDict1D.items()``
- ``ParamDict1D.keys()``
- ``ParamDict1D.values()``

ParamDictND
===========

Custom subclass of `dict` to define parameters with N-dim tuple keys.

Constructor
-----------
.. autosummary::
   :toctree: ../auto_api/

   ParamDictND

Attributes
----------
.. autosummary::

   ParamDictND.key_names
   ParamDictND.value_name

Numerical operations
--------------------
.. autosummary::

   ParamDictND.sum
   ParamDictND.min
   ParamDictND.max
   ParamDictND.mean
   ParamDictND.median
   ParamDictND.median_high
   ParamDictND.median_low

Mapping operations
------------------
.. autosummary::

   ParamDictND.clear
   ParamDictND.get
   ParamDictND.lookup
   ParamDictND.pop
   ParamDictND.popitem
   ParamDictND.setdefault

Efficient subset selection
--------------------------
.. autosummary::

   ParamDictND.subset_keys
   ParamDictND.subset_values

Views
-----
- ``ParamDictND.items()``
- ``ParamDictND.keys()``
- ``ParamDictND.values()``

Casting from pandas Series/DataFrame
====================================

Methods to cast pandas Series/DataFrame into ParamDict1D/ParamDictND are provided
through the custom ``.opti`` accessor.

.. currentmodule:: pandas

.. autosummary::
   :toctree: ../auto_api/
   :template: autosummary/accessor_method.rst

   Series.opti.to_paramdict
   DataFrame.opti.to_paramdict
