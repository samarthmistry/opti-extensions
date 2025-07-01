# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures for testing model functionality."""

import os
import re

import pytest
from docplex.mp.model import Model


def regex_trim(input: str) -> str:
    return re.sub(r'\s+', '', input)


@pytest.fixture()
def mdl():
    mdl = Model()
    yield mdl
    mdl.end()


@pytest.fixture()
def expected_log_start():
    text = '\n'.join(
        [
            '------------------------------  LP problem statistics  ------------------------------',
            '',
            'Problem name         : %s',
            'Objective sense      : Minimize',
            'Variables            :       0',
            'Objective nonzeros   :       0',
            'Linear constraints   :       0',
            '  Nonzeros           :       0',
            '  RHS nonzeros       :       0',
            '',
            'Variables            : Min LB: all infinite     Max UB: all infinite   ',
            'Objective nonzeros   : Min   : all zero         Max   : all zero       ',
            'Linear constraints   :',
            '  Nonzeros           : Min   : all zero         Max   : all zero       ',
            '  RHS nonzeros       : Min   : all zero         Max   : all zero       ',
            '',
            '-------------------------------  CPLEX optimizer log  -------------------------------',
            '',
        ]
    )
    return text


@pytest.fixture()
def expected_log_end():
    text = '\n'.join(
        [
            '---------------------------  Solution quality statistics  ---------------------------',
            '',
            'There are no bound infeasibilities.',
            'There are no reduced-cost infeasibilities.',
            'Maximum Ax-b residual              = 0',
            "Maximum c-B'pi residual            = 0",
            'Maximum |x|                        = 0',
            'Maximum |pi|                       = 0',
            'Maximum |red-cost|                 = 0',
            'Condition number of unscaled basis = 0.0e+00',
            '',
            '-------------------------------------------------------------------------------------',
            '',
        ]
    )
    return text


@pytest.fixture(scope='module')
def mdl_to_tune():
    mdl = Model(name='dummy', checker='off', ignore_names=True)
    desk = mdl.continuous_var(name='desk')
    cell = mdl.continuous_var(name='cell')
    mdl.add_constraints_(
        [
            desk >= 100,
            cell >= 100,
            0.2 * desk + 0.4 * cell <= 400,
            0.5 * desk + 0.4 * cell <= 490,
        ]
    )
    mdl.maximize(12 * desk + 20 * cell)

    yield mdl

    mdl.end()


@pytest.fixture(scope='module')
def files_to_tune():
    mdl1 = Model(name='dummy1', checker='off', ignore_names=True)
    desk1 = mdl1.continuous_var(name='desk')
    cell1 = mdl1.continuous_var(name='cell')
    mdl1.add_constraints_(
        [
            desk1 >= 100,
            cell1 >= 100,
            0.2 * desk1 + 0.4 * cell1 <= 400,
            0.5 * desk1 + 0.4 * cell1 <= 490,
        ]
    )
    mdl1.maximize(12 * desk1 + 20 * cell1)
    mdl1_path = mdl1.export_as_mps(basename='mdl1')  # will write to tempdir by default
    mdl1.end()

    mdl2 = Model(name='Dummy', checker='off', ignore_names=True)
    desk2 = mdl2.continuous_var(name='desk')
    cell2 = mdl2.continuous_var(name='cell')
    mdl2.add_constraints_(
        [
            desk2 >= 120,
            cell2 >= 80,
            0.3 * desk2 + 0.6 * cell2 <= 450,
            0.5 * desk2 + 0.5 * cell2 <= 450,
        ]
    )
    mdl2.maximize(14 * desk2 + 22 * cell2)
    mdl2_path = mdl2.export_as_mps(basename='mdl2')  # will write to tempdir by default
    mdl2.end()

    yield mdl1_path, mdl2_path

    os.remove(mdl1_path)
    os.remove(mdl2_path)


@pytest.fixture(scope='module')
def rs_mdl():
    mdl = Model(name='dummy', checker='off', ignore_names=True)
    desk = mdl.integer_var(name='desk')
    cell = mdl.integer_var(name='cell')
    mdl.add_constraints_(
        [
            desk >= 100,
            cell >= 100,
            0.2 * desk + 0.4 * cell <= 400,
            0.5 * desk + 0.4 * cell <= 490,
        ]
    )
    mdl.maximize(12 * desk + 20 * cell)

    yield mdl

    mdl.end()


@pytest.fixture()
def expected_infeas_log_end():
    text = '\n'.join(
        [
            '-------------------------------------------------------------------------------------',
            '',
        ]
    )
    return text


@pytest.fixture(scope='module')
def infeas_mdl():
    mdl = Model(name='dummy', checker='off', ignore_names=True)
    desk = mdl.integer_var(name='desk')
    cell = mdl.integer_var(name='cell')
    mdl.add_constraints_(
        [
            0.2 * desk + 0.4 * cell <= 400,
            0.2 * desk + 0.4 * cell >= 500,
        ]
    )
    mdl.maximize(12 * desk + 20 * cell)

    yield mdl

    mdl.end()
