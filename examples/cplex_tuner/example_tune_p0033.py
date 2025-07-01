# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Tune for a DOcplex model
========================

We will tune parameters for the instance `p0033` from MIPLIB 3.0 using the
`opti-extensions` library.

Reference:
Bixby, Robert E., Sebastian Ceria, Cassandra M. McZeal, and Martin WP
Savelsbergh. "An updated mixed integer programming library: MIPLIB 3.0."
Optima 58, no. June (1998): 12-15.
"""

# %%
# Fetch the instance
# ------------------
from pathlib import Path
from urllib.request import urlopen

Path('instances').mkdir(exist_ok=True)
name = 'p0033.mps.gz'

response = urlopen(f'https://miplib2010.zib.de/miplib3/miplib3/{name}')

response_OK = True
if response.getcode() == 200:
    with open(f'instances/{name}', 'wb') as fp:
        fp.write(response.read())
else:
    response_OK = False
    print(f'Could not fetch the instance {name} from MIPLIB 3.0')

# %%
# Run the tuning tool
# -------------------
from docplex.mp.model_reader import ModelReader

from opti_extensions.docplex import tune

if response_OK:
    model = ModelReader.read('instances/p0033.mps.gz')
    tuned_params = tune(model, log_output=True, overall_timelimit_sec=10, repeat=3)

# %%
# Tuned parameters
# ----------------
if response_OK:
    print(tuned_params)
