# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Evaluate variability of a DOcplex model
=======================================

We will evaluate variability of the instance `glass4` from MIPLIB 2010 using the
`opti-extensions` library.

Reference:
Koch, Thorsten, Tobias Achterberg, Erling Andersen, Oliver Bastert, Timo
Berthold, Robert E. Bixby, Emilie Danna et al. "MIPLIB 2010: Mixed integer
programming library version 5." Mathematical Programming Computation 3
(2011): 103-163.
"""

# %%
# Fetch the instance
# ------------------
from pathlib import Path
from urllib.request import urlopen

Path('instances').mkdir(exist_ok=True)
name = 'glass4.mps.gz'

response = urlopen(f'https://miplib.zib.de/WebData/instances/{name}')

response_OK = True
if response.getcode() == 200:
    with open(f'instances/{name}', 'wb') as fp:
        fp.write(response.read())
else:
    response_OK = False
    print(f'Could not fetch the instance {name} from MIPLIB 2010')

# %%
# Run the `runseeds` procedure
# ----------------------------
from docplex.mp.model_reader import ModelReader

from opti_extensions.docplex import runseeds

if response_OK:
    model = ModelReader.read('instances/glass4.mps.gz')
    model.parameters.timelimit = 4
    runseeds(model, count=3, log_output=True)
