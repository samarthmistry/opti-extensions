# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Custom operations on ParamDictND."""

from statistics import StatisticsError

import pytest

from opti_extensions import ParamDictND


@pytest.mark.parametrize(
    '_input, key, present',
    [('paramdictNd_pop3', ('A', 'B'), True), ('paramdictNd_pop3', ('Y', 'Z'), False)],
)
def test_vardict1d_lookup_pass(request, _input, key, present):
    input = request.getfixturevalue(_input)
    value = input.lookup(*key)
    if present:
        assert value is input[key]
    else:
        assert value == 0


@pytest.mark.parametrize('key', [[13], (0, 0), ()])
def test_vardictNd_lookup_typerr(request, key):
    input = request.getfixturevalue('paramdictNd_pop2')
    with pytest.raises(TypeError):
        input.lookup(key)


@pytest.mark.parametrize('key', [(), (0, 0, 0), (1, 2, 3, 4)])
def test_vardictNd_lookup_valerr(request, key):
    input = request.getfixturevalue('paramdictNd_pop2')
    with pytest.raises(ValueError):
        input.lookup(*key)


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2}), 3),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2}), 3.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0}), 3.0),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2.0}), 3.0),
    ],
)
def test_paramdictNd_sum_all_pass(input, expected):
    assert input.sum() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2}), 1),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2}), 1.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0}), 1),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2.0}), 1.0),
    ],
)
def test_paramdictNd_min_all_pass(input, expected):
    assert input.min() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2}), 2),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2}), 2),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0}), 2.0),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2.0}), 2.0),
    ],
)
def test_paramdictNd_max_all_pass(input, expected):
    assert input.max() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2}), 1.5),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2}), 1.5),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0}), 1.5),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2.0}), 1.5),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3}), 2),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 3.0}), 2.0),
    ],
)
def test_paramdictNd_mean_all_pass(input, expected):
    assert input.mean() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2}), 1.5),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2}), 1.5),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0}), 1.5),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2.0}), 1.5),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3}), 2),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 3.0}), 2.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('E', 'F'): 7}), 2),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2, ('E', 'F'): 7}), 2),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('E', 'F'): 7}), 2.0),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2.0, ('E', 'F'): 7}), 2.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('E', 'F'): 7}), 3),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 3.0, ('E', 'F'): 7}), 3.0),
    ],
)
def test_paramdictNd_median_all_pass(input, expected):
    assert input.median() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('E', 'F'): 7, ('G', 'H'): 8}), 7),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('E', 'F'): 7, ('G', 'H'): 8}), 7),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('E', 'F'): 7.0, ('G', 'H'): 8}), 7.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('E', 'F'): 7.0, ('G', 'H'): 8}), 7.0),
    ],
)
def test_paramdictNd_median_high_all_pass(input, expected):
    assert input.median_high() == expected


@pytest.mark.parametrize(
    'input, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('E', 'F'): 7, ('G', 'H'): 8}), 2),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('E', 'F'): 7, ('G', 'H'): 8}), 2.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('E', 'F'): 7.0, ('G', 'H'): 8}), 2),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('E', 'F'): 7.0, ('G', 'H'): 8}), 2.0),
    ],
)
def test_paramdictNd_median_low_all_pass(input, expected):
    assert input.median_low() == expected


@pytest.mark.parametrize(
    'input, pattern, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7}), ('A', '*'), 8),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2, ('A', 'D'): 7}), ('A', '*'), 8.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('A', '*'), 8.0),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('A', '*'), 8.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'F'): 7}), ('*', 'D'), 2),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'F'): 7}), ('*', 'D'), 2.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'D'): 7.0}), ('Z', '*'), 0),
    ],
)
def test_paramdictNd_sum_partial_pass(input, pattern, expected):
    assert input.sum(*pattern) == expected


@pytest.mark.parametrize(
    'input, pattern, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7}), ('A', '*'), 1),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2, ('A', 'D'): 7}), ('A', '*'), 1.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('A', '*'), 1),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('A', '*'), 1.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'F'): 7}), ('*', 'D'), 2),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'F'): 7}), ('*', 'D'), 2.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'D'): 7.0}), ('Z', '*'), 0),
    ],
)
def test_paramdictNd_min_partial_pass(input, pattern, expected):
    assert input.min(*pattern) == expected


@pytest.mark.parametrize(
    'input, pattern, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7}), ('A', '*'), 7),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2, ('A', 'D'): 7}), ('A', '*'), 7),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('A', '*'), 7.0),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('A', '*'), 7.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'F'): 7}), ('*', 'D'), 2),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'F'): 7}), ('*', 'D'), 2.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2, ('A', 'D'): 7.0}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 2.0, ('A', 'D'): 7.0}), ('Z', '*'), 0),
    ],
)
def test_paramdictNd_max_partial_pass(input, pattern, expected):
    assert input.max(*pattern) == expected


@pytest.mark.parametrize(
    'input, pattern, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7}), ('A', '*'), 4),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 3, ('A', 'D'): 7}), ('A', '*'), 4.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('A', '*'), 4.0),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('A', '*'), 4.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'F'): 7}), ('*', 'D'), 3),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'F'): 7}), ('*', 'D'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7.0}), ('Z', '*'), 0),
    ],
)
def test_paramdictNd_mean_partial_pass(input, pattern, expected):
    assert input.mean(*pattern) == expected


@pytest.mark.parametrize(
    'input, pattern, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('A', 'D'): 7}), ('A', '*'), 3),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3.0, ('A', 'D'): 7}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('A', 'D'): 7.0}), ('A', '*'), 3),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3.0, ('A', 'D'): 7.0}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7}), ('A', '*'), 4),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 3, ('A', 'D'): 7}), ('A', '*'), 4.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('A', '*'), 4.0),
        (ParamDictND({('A', 'B'): 1.0, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('A', '*'), 4.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'F'): 7}), ('*', 'D'), 3),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'F'): 7}), ('*', 'D'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7.0}), ('Z', '*'), 0),
    ],
)
def test_paramdictNd_median_partial_pass(input, pattern, expected):
    assert input.median(*pattern) == expected


@pytest.mark.parametrize(
    'input, pattern, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('A', 'D'): 7}), ('A', '*'), 3),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3.0, ('A', 'D'): 7}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('A', 'D'): 7.0}), ('A', '*'), 3),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3.0, ('A', 'D'): 7.0}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('B', 'D'): 7}), ('A', '*'), 1),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3, ('B', 'D'): 7}), ('A', '*'), 1.0),
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('B', 'D'): 7.0}), ('A', '*'), 1),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3, ('B', 'D'): 7.0}), ('A', '*'), 1.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'F'): 7}), ('*', 'D'), 3),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'F'): 7}), ('*', 'D'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7.0}), ('Z', '*'), 0),
    ],
)
def test_paramdictNd_median_low_partial_pass(input, pattern, expected):
    assert input.median_low(*pattern) == expected


@pytest.mark.parametrize(
    'input, pattern, expected',
    [
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('A', 'D'): 7}), ('A', '*'), 3),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3.0, ('A', 'D'): 7}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('A', 'D'): 7.0}), ('A', '*'), 3),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3.0, ('A', 'D'): 7.0}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('B', 'D'): 7}), ('A', '*'), 3),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3, ('B', 'D'): 7}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('A', 'C'): 3, ('B', 'D'): 7.0}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1.0, ('A', 'C'): 3, ('B', 'D'): 7.0}), ('A', '*'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'F'): 7}), ('*', 'D'), 3),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'F'): 7}), ('*', 'D'), 3.0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3, ('A', 'D'): 7.0}), ('Z', '*'), 0),
        (ParamDictND({('A', 'B'): 1, ('C', 'D'): 3.0, ('A', 'D'): 7.0}), ('Z', '*'), 0),
    ],
)
def test_paramdictNd_median_high_partial_pass(input, pattern, expected):
    assert input.median_high(*pattern) == expected


all_stat_funcs = ['sum', 'min', 'max', 'mean', 'median', 'median_high', 'median_low']


@pytest.mark.parametrize('stat_func', all_stat_funcs)
def test_paramdictNd_empty_stat_err(stat_func):
    prm = ParamDictND()
    with pytest.raises(StatisticsError):
        getattr(prm, stat_func)()


@pytest.mark.parametrize('stat_func', all_stat_funcs)
def test_paramdictNd_stat_partial_valerr1(paramdictNd_pop3, stat_func):
    with pytest.raises(ValueError):
        getattr(paramdictNd_pop3, stat_func)('A', '*', 'B')


@pytest.mark.parametrize('stat_func', all_stat_funcs)
def test_paramdictNd_stat_partial_valerr2(paramdictNd_pop3, stat_func):
    with pytest.raises(ValueError):
        getattr(paramdictNd_pop3, stat_func)('A', 'B')


@pytest.mark.parametrize('stat_func', all_stat_funcs)
def test_paramdictNd_stat_partial_valerr3(paramdictNd_pop3, stat_func):
    with pytest.raises(ValueError):
        getattr(paramdictNd_pop3, stat_func)('*', '*')


@pytest.mark.parametrize('stat_func', all_stat_funcs)
def test_paramdictNd_stat_partial_typerr(paramdictNd_pop3, stat_func):
    with pytest.raises(TypeError):
        getattr(paramdictNd_pop3, stat_func)(('A', '*'))


@pytest.mark.parametrize('stat_func', ['some', 'gibberish', 'str'])
def test_check_for_calc_stat_valerr(paramdictNd_pop3, stat_func):
    with pytest.raises(ValueError):
        paramdictNd_pop3._check_for_calc_stat(stat_func)
