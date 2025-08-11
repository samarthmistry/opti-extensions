opti-extensions |version|
#########################

A collection of custom data structures and user-friendly functions for
mathematical optimization modeling with `DOcplex <https://
ibmdecisionoptimization.github.io/docplex-doc>`_, `gurobipy <https://
docs.gurobi.com/projects/optimizer/en/current/reference/python.html>`_,
and `Xpress <https://www.fico.com/fico-xpress-optimization/docs/latest/
solver/optimizer/python/HTML>`_.

Features
========

* **Specialized data structures**: For defining index-sets, parameters, and
  decision variables enabling concise and high-performance algebraic modeling
  — compatible across different solver APIs.
* **Easy access to additional CPLEX functionality**: Like `tuning tool <https://
  www.ibm.com/docs/en/icos/latest?topic=programmingconsiderations-tuning-
  tool>`_, `runseeds <https://www.ibm.com/docs/en/icos/latest?topic=cplex-
  evaluating-variability>`_, `displaying problem statistics <https://www.ibm.com/
  docs/en/icos/latest?topic=problem-displaying-statistics>`_, and `displaying
  solution quality statistics <https://www.ibm.com/docs/en/icos/latest?topic=
  cplex-evaluating-solution-quality>`_ — not directly available in DOcplex.
* **Type-complete interface**: Enables static type checking and intelligent
  auto-completion suggestions with modern IDEs — reducing type errors and
  improving development speed.
* **Robust codebase**: 100% coverage spanning 2750+ test cases and fully
  type-checked with mypy under `strict mode <https://mypy.readthedocs.io/en/
  stable/getting_started.html#strict-mode-and-configuration>`_. Tested with:

  * CPLEX versions: 20.1.0, 22.1.0, 22.1.1, 22.1.2
  * Gurobi versions: 11.0, 12.0
    (most likely works with 10.0 but `cannot test <https://support.gurobi.
    com/hc/en-us/articles/19487474933521-How-do-I-resolve-the-error-License
    -expired-2024-10-28>`_ with the size-limited license provided with
    gurobipy distributed via PyPI)
  * Xpress versions: 9.4, 9.5, 9.6, 9.7

Documentation
=============

.. grid:: 4

   .. grid-item-card:: Installation
       :link: installation/index
       :link-type: doc
       :text-align: center
       :margin: 2 auto auto auto

       :material-regular:`terminal;2em`

   .. grid-item-card:: API Reference
       :link: api_reference/index
       :link-type: doc
       :text-align: center
       :margin: 2 auto auto auto

       :material-regular:`text_snippet;2em`

   .. grid-item-card:: Tutorials & Examples
       :link: auto_examples/index
       :link-type: doc
       :text-align: center
       :margin: 2 auto auto auto

       :material-regular:`computer;2em`

   .. grid-item-card:: Changelog
       :link: https://github.com/samarthmistry/opti-extensions/releases
       :text-align: center
       :margin: 2 auto auto auto

       :material-regular:`track_changes;2em`

.. toctree::
   :hidden:
   :maxdepth: 1

   installation/index
   api_reference/index
   auto_examples/index
   Changelog <https://github.com/samarthmistry/opti-extensions/releases>

License
=======

opti-extensions is an open-source project developed by `Samarth Mistry
<https://www.linkedin.com/in/samarthmistry/>`_ :fab:`linkedin` and released
under the Apache 2.0 License. See the `LICENSE <https://github.com/
samarthmistry/opti-extensions/blob/main/LICENSE>`_ and `NOTICE <https://
github.com/samarthmistry/opti-extensions/blob/main/NOTICE>`_ for more
details.

|
