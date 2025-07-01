# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Custom operations on ParamDict1D."""

from statistics import StatisticsError

import pytest

from opti_extensions import ParamDict1D


@pytest.mark.parametrize(
    '_input, key, present',
    [('paramdict1d_pop3', 'A', True), ('paramdict1d_pop3', 'Z', False)],
)
def test_vardict1d_lookup_pass(request, _input, key, present):
    input = request.getfixturevalue(_input)
    value = input.lookup(key)
    if present:
        assert value is input[key]
    else:
        assert value == 0


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDict1D({'A': 1, 'B': 2}), 3),
        (ParamDict1D({'A': 1.0, 'B': 2}), 3.0),
        (ParamDict1D({'A': 1, 'B': 2.0}), 3.0),
        (ParamDict1D({'A': 1.0, 'B': 2.0}), 3.0),
    ],
)
def test_paramdict1d_sum_pass(input, expected):
    assert input.sum() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDict1D({'A': 1, 'B': 2}), 1),
        (ParamDict1D({'A': 1.0, 'B': 2}), 1.0),
        (ParamDict1D({'A': 1, 'B': 2.0}), 1),
        (ParamDict1D({'A': 1.0, 'B': 2.0}), 1.0),
    ],
)
def test_paramdict1d_min_pass(input, expected):
    assert input.min() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDict1D({'A': 1, 'B': 2}), 2),
        (ParamDict1D({'A': 1.0, 'B': 2}), 2),
        (ParamDict1D({'A': 1, 'B': 2.0}), 2.0),
        (ParamDict1D({'A': 1.0, 'B': 2.0}), 2.0),
    ],
)
def test_paramdict1d_max_pass(input, expected):
    assert input.max() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDict1D({'A': 1, 'B': 2}), 1.5),
        (ParamDict1D({'A': 1.0, 'B': 2}), 1.5),
        (ParamDict1D({'A': 1, 'B': 2.0}), 1.5),
        (ParamDict1D({'A': 1.0, 'B': 2.0}), 1.5),
        (ParamDict1D({'A': 1, 'B': 3}), 2),
        (ParamDict1D({'A': 1.0, 'B': 3.0}), 2.0),
    ],
)
def test_paramdict1d_mean_pass(input, expected):
    assert input.mean() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDict1D({'A': 1, 'B': 2}), 1.5),
        (ParamDict1D({'A': 1.0, 'B': 2}), 1.5),
        (ParamDict1D({'A': 1, 'B': 2.0}), 1.5),
        (ParamDict1D({'A': 1.0, 'B': 2.0}), 1.5),
        (ParamDict1D({'A': 1, 'B': 3}), 2),
        (ParamDict1D({'A': 1.0, 'B': 3.0}), 2.0),
        (ParamDict1D({'A': 1, 'B': 2, 'C': 7}), 2),
        (ParamDict1D({'A': 1.0, 'B': 2, 'C': 7}), 2),
        (ParamDict1D({'A': 1, 'B': 2.0, 'C': 7}), 2.0),
        (ParamDict1D({'A': 1.0, 'B': 2.0, 'C': 7}), 2.0),
        (ParamDict1D({'A': 1, 'B': 3, 'C': 7}), 3),
        (ParamDict1D({'A': 1.0, 'B': 3.0, 'C': 7}), 3.0),
    ],
)
def test_paramdict1d_median_pass(input, expected):
    assert input.median() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDict1D({'A': 1, 'B': 2, 'C': 7, 'D': 8}), 7),
        (ParamDict1D({'A': 1, 'B': 2.0, 'C': 7, 'D': 8}), 7),
        (ParamDict1D({'A': 1, 'B': 2, 'C': 7.0, 'D': 8}), 7.0),
        (ParamDict1D({'A': 1, 'B': 2.0, 'C': 7.0, 'D': 8}), 7.0),
    ],
)
def test_paramdict1d_median_high_pass(input, expected):
    assert input.median_high() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDict1D({'A': 1, 'B': 2, 'C': 7, 'D': 8}), 2),
        (ParamDict1D({'A': 1, 'B': 2.0, 'C': 7, 'D': 8}), 2.0),
        (ParamDict1D({'A': 1, 'B': 2, 'C': 7.0, 'D': 8}), 2),
        (ParamDict1D({'A': 1, 'B': 2.0, 'C': 7.0, 'D': 8}), 2.0),
    ],
)
def test_paramdict1d_median_low_pass(input, expected):
    assert input.median_low() == expected


@pytest.mark.parametrize(
    'stat_func', ['sum', 'min', 'max', 'mean', 'median', 'median_high', 'median_low']
)
def test_paramdict1d_empty_stat_err(stat_func):
    prm = ParamDict1D()
    with pytest.raises(StatisticsError):
        getattr(prm, stat_func)()
