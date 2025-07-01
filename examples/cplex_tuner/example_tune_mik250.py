# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Tune for a batch of models
==========================

We will tune parameters for the instances `mik-250-20-75-1` & `mik-250-20-75-2`
from MIPLIB 2010 using the `opti-extensions` library.

Reference:
Koch, Thorsten, Tobias Achterberg, Erling Andersen, Oliver Bastert, Timo
Berthold, Robert E. Bixby, Emilie Danna et al. "MIPLIB 2010: Mixed integer
programming library version 5." Mathematical Programming Computation 3
(2011): 103-163.
"""

# %%
# Fetch the instances
# -------------------
from pathlib import Path
from urllib.request import urlopen

Path('instances').mkdir(exist_ok=True)
names = ('mik-250-20-75-1.mps.gz', 'mik-250-20-75-2.mps.gz')

response_OK = True
for name in names:
    response = urlopen(f'https://miplib.zib.de/WebData/instances/{name}')

    if response.getcode() == 200:
        with open(f'instances/{name}', 'wb') as fp:
            fp.write(response.read())
    else:
        response_OK = False
        print(f'Could not fetch the instance {name} from MIPLIB 2010')

# %%
# Run the tuning tool
# -------------------
from opti_extensions.docplex import batch_tune

if response_OK:
    tuned_params = batch_tune(
        'instances/mik-250-20-75-1.mps.gz',
        'instances/mik-250-20-75-2.mps.gz',
        log_output=True,
        overall_timelimit_sec=60,
        fixed_params_and_values={'threads': 2},
    )

# %%
# Tuned parameters
# ----------------
if response_OK:
    print(tuned_params)
