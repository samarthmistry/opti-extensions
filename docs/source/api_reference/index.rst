API Reference
#############

All public functions and classes are provided through the ``opti_extensions.*``,
``opti_extensions.docplex.*``, ``opti_extensions.gurobipy.*``,
``opti_extensions.xpress.*`` namespaces as follows:

.. code-block:: RST

  opti_extensions
  ├── IndexSet1D
  ├── IndexSetND
  ├── ParamDict1D
  └── ParamDictND

  opti_extensions.docplex
  ├── print_problem_stats
  ├── print_solution_quality_stats
  ├── runseeds
  ├── solve
  ├── batch_tune
  ├── tune
  ├── add_variable
  ├── add_variables
  ├── VarDict1D
  └── VarDictND

  opti_extensions.gurobipy
  ├── addVars
  ├── VarDict1D
  └── VarDictND

  opti_extensions.xpress
  ├── addVariables
  ├── VarDict1D
  └── VarDictND

.. warning::
   Modules, functions, and methods named with a leading underscore are PRIVATE. Stable
   functionality is not guaranteed.

Details
=======

.. toctree::
   :maxdepth: 2

   index_sets
   parameters
   docplex_model_specific
   docplex_variables
   gurobipy_variables
   xpress_variables

|
