Installation
############

Install
=======

Python >=3.10 is required.

opti-extensions can be installed via pip from `PyPI <https://pypi.python
.org/pypi/opti-extensions>`_.

.. code-block:: bash

    pip install opti-extensions

Required dependencies
=====================

opti-extensions is developed and tested with package versions newer than
those listed below, making them the recommended choice.

==========  ==================================
Solver API  Recommended package versions
==========  ==================================
DOcplex     docplex >=2.25.236, cplex >=20.1.0
----------  ----------------------------------
gurobipy    gurobipy >=11
----------  ----------------------------------
Xpress      xpress >=9.4
==========  ==================================

Optional dependencies
=====================

opti-extensions provides optional functionality to directly cast pandas
Series/DataFrame/Index objects into its specialized data structures. If pandas
is present, this functionality will be registered with a custom ``.opti``
accessor. Please refer to the :doc:`../api_reference/index` section for more
details.

pandas >=1.5.0 is recommended.

|
