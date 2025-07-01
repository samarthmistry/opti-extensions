# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Model functionality."""

import pytest

from opti_extensions.docplex import (
    print_problem_stats,
    print_solution_quality_stats,
    runseeds,
    solve,
)

from .conftest import regex_trim


def validate_logoutput(input, infeasible, expected_log_start, expected_log_end):
    if not infeasible:
        input_pre = input.split('CPLEX optimizer log')[0]
        expected_pre = expected_log_start.split('CPLEX optimizer log')[0]
        assert regex_trim(input_pre) == regex_trim(expected_pre)

    if infeasible:
        input_post = input.split('-' * 85)[1]
        expected_post = expected_log_end.split('-' * 85)[1]
    else:
        input_post = input.split('Solution quality statistics')[1]
        expected_post = expected_log_end.split('Solution quality statistics')[1]
    assert regex_trim(input_post) == regex_trim(expected_post)


def test_print_model_stats_pass(capsys, mdl):
    print_problem_stats(mdl)

    captured = capsys.readouterr().out
    expected = '\n'.join(
        [
            f'Problem name         : {mdl.name}',
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
            '',
        ]
    )

    assert regex_trim(captured) == regex_trim(expected)


def test_print_solution_quality_stats_unsolved_pass(capsys, mdl):
    print_solution_quality_stats(mdl)

    captured = capsys.readouterr().out
    expected = f'Model `{mdl.name}` has no incumbent solution.\n'

    assert regex_trim(captured) == regex_trim(expected)


def test_print_solution_quality_stats_infeas_pass(capsys, infeas_mdl):
    _ = infeas_mdl.solve(log_output=False)
    print_solution_quality_stats(infeas_mdl)

    captured = capsys.readouterr().out
    expected = f'Model `{infeas_mdl.name}` has no incumbent solution.\n'

    assert regex_trim(captured) == regex_trim(expected)


def test_print_solution_quality_stats_solved_pass(capsys, mdl):
    _ = mdl.solve()
    print_solution_quality_stats(mdl)

    captured = capsys.readouterr().out
    expected = '\n'.join(
        [
            'There are no bound infeasibilities.',
            'There are no reduced-cost infeasibilities.',
            'Maximum Ax-b residual              = 0',
            "Maximum c-B'pi residual            = 0",
            'Maximum |x|                        = 0',
            'Maximum |pi|                       = 0',
            'Maximum |red-cost|                 = 0',
            'Condition number of unscaled basis = 0.0e+00',
            '',
            '',
        ]
    )

    assert regex_trim(captured) == regex_trim(expected)


def test_solve_solution_pass(rs_mdl):
    sol1 = rs_mdl.solve(clean_before_solve=True)
    sol2 = solve(rs_mdl, clean_before_solve=True)

    assert sol1.to_string() == sol2.to_string()


def test_solve_infeas_solution_pass(infeas_mdl):
    sol1 = infeas_mdl.solve(clean_before_solve=True)
    sol2 = solve(infeas_mdl, clean_before_solve=True)

    assert sol1 == sol2


@pytest.mark.parametrize(
    'infeasible, _mdl, _expected_log_end',
    [(False, 'mdl', 'expected_log_end'), (True, 'infeas_mdl', 'expected_infeas_log_end')],
)
def test_solve_logoutput_context_pass(
    capsys, request, infeasible, _mdl, _expected_log_end, expected_log_start
):
    mdl = request.getfixturevalue(_mdl)
    expected_log_end = request.getfixturevalue(_expected_log_end)

    mdl.context.solver.log_output = True
    _ = solve(mdl)
    captured = capsys.readouterr().out

    validate_logoutput(captured, infeasible, expected_log_start % mdl.name, expected_log_end)


@pytest.mark.parametrize(
    'infeasible, _mdl, _expected_log_end',
    [(False, 'mdl', 'expected_log_end'), (True, 'infeas_mdl', 'expected_infeas_log_end')],
)
@pytest.mark.parametrize('log_output', [True, 'stdout', 'sys.stdout', '1'])
def test_solve_logoutput_stdout_pass(
    capsys, request, infeasible, _mdl, _expected_log_end, log_output, expected_log_start
):
    mdl = request.getfixturevalue(_mdl)
    expected_log_end = request.getfixturevalue(_expected_log_end)

    _ = solve(mdl, log_output=log_output)
    captured = capsys.readouterr().out

    validate_logoutput(captured, infeasible, expected_log_start % mdl.name, expected_log_end)


@pytest.mark.parametrize(
    'infeasible, _mdl, _expected_log_end',
    [(False, 'mdl', 'expected_log_end'), (True, 'infeas_mdl', 'expected_infeas_log_end')],
)
@pytest.mark.parametrize('log_output', ['stderr', 'sys.stderr'])
def test_solve_logoutput_stderr_pass(
    capsys, request, infeasible, _mdl, _expected_log_end, log_output, expected_log_start
):
    mdl = request.getfixturevalue(_mdl)
    expected_log_end = request.getfixturevalue(_expected_log_end)

    _ = solve(mdl, log_output=log_output)
    captured = capsys.readouterr().err

    validate_logoutput(captured, infeasible, expected_log_start % mdl.name, expected_log_end)


@pytest.mark.parametrize(
    'infeasible, _mdl, _expected_log_end',
    [(False, 'mdl', 'expected_log_end'), (True, 'infeas_mdl', 'expected_infeas_log_end')],
)
def test_solve_logoutput_filepath_pass(
    tmp_path, request, infeasible, _mdl, _expected_log_end, expected_log_start
):
    mdl = request.getfixturevalue(_mdl)
    expected_log_end = request.getfixturevalue(_expected_log_end)

    file = tmp_path / 'file.log'
    _ = solve(mdl, log_output=str(file))
    captured = file.read_text(encoding='utf-8')

    validate_logoutput(captured, infeasible, expected_log_start % mdl.name, expected_log_end)


@pytest.mark.parametrize(
    'infeasible, _mdl, _expected_log_end',
    [(False, 'mdl', 'expected_log_end'), (True, 'infeas_mdl', 'expected_infeas_log_end')],
)
def test_solve_logoutput_fileobj_pass(
    tmp_path, request, infeasible, _mdl, _expected_log_end, expected_log_start
):
    mdl = request.getfixturevalue(_mdl)
    expected_log_end = request.getfixturevalue(_expected_log_end)

    file = tmp_path / 'file.log'
    with file.open('w') as f:
        _ = solve(mdl, log_output=f)
    captured = file.read_text(encoding='utf-8')

    validate_logoutput(captured, infeasible, expected_log_start % mdl.name, expected_log_end)


@pytest.mark.parametrize('log_output', [False, '0', None])
def test_solve_logoutput_false_pass(capsys, mdl, log_output):
    _ = solve(mdl, log_output=log_output)

    captured = capsys.readouterr()
    expected = ''

    assert captured.out == expected


def test_solve_logoutput_not_provided(capsys, mdl):
    _ = solve(mdl)

    captured = capsys.readouterr()
    expected = ''

    assert captured.out == expected


@pytest.mark.parametrize('mdl', ['abc', 123, ('A', 'B')])
def test_solve_mdl_typerr(mdl):
    with pytest.raises(TypeError):
        solve(mdl)


def validate_runseeds_logoutput(input: str) -> None:
    assert 'Exit codes:' in input
    assert 'Optimization status codes:' in input


@pytest.mark.parametrize('mdl', ['abc', 123, ('A', 'B')])
def test_runseeds_mdl_typerr(mdl):
    with pytest.raises(TypeError):
        runseeds(mdl)


def test_runseeds_mdl_cpxerr(mdl_to_tune):
    with pytest.raises(ValueError):
        runseeds(mdl_to_tune)


@pytest.mark.parametrize('log_output', [True, 'stdout', 'sys.stdout', '1'])
def test_runseeds_logoutput_stdout_pass(capsys, rs_mdl, log_output):
    _ = runseeds(rs_mdl, log_output=log_output)
    captured = capsys.readouterr().out

    validate_runseeds_logoutput(captured)


@pytest.mark.parametrize('log_output', ['stderr', 'sys.stderr'])
def test_runseeds_logoutput_stderr_pass(capsys, rs_mdl, log_output):
    _ = runseeds(rs_mdl, log_output=log_output)
    captured = capsys.readouterr().err

    validate_runseeds_logoutput(captured)


@pytest.mark.parametrize('log_output', [False, None, '0'])
def test_runseeds_logoutput_no_valerr(rs_mdl, log_output):
    with pytest.raises(ValueError):
        _ = runseeds(rs_mdl, log_output=log_output)


def test_runseeds_logoutput_filepath_pass(tmp_path, rs_mdl):
    file = tmp_path / 'file.log'
    _ = runseeds(rs_mdl, log_output=str(file))
    captured = file.read_text(encoding='utf-8')

    validate_runseeds_logoutput(captured)


def test_runseeds_logoutput_fileobj_pass(tmp_path, rs_mdl):
    file = tmp_path / 'file.log'
    with file.open('w') as f:
        _ = runseeds(rs_mdl, log_output=f)
    captured = file.read_text(encoding='utf-8')

    validate_runseeds_logoutput(captured)


@pytest.mark.parametrize('log_output', [2, ['A', 'B'], 3.0])
def test_runseeds_logoutput_typerr(rs_mdl, log_output):
    with pytest.raises(TypeError):
        _ = runseeds(rs_mdl, log_output=log_output)


@pytest.mark.parametrize('count', [False, None, '0', -2, 0, (1, 2)])
def test_runseeds_count_valerr(rs_mdl, count):
    with pytest.raises(ValueError):
        _ = runseeds(rs_mdl, count=count)


@pytest.mark.parametrize(
    'input, func',
    [
        (True, 'stderr'),
        ('1', 'stderr'),
        ('stdout', 'stderr'),
        ('sys.stdout', 'stderr'),
        ('stderr', 'stdout'),
        ('sys.stderr', 'stdout'),
        ('file', 'stdout'),
    ],
)
def test_runseeds_persist_lo(tmp_path, rs_mdl, input, func):
    if input == 'file':
        prior = (tmp_path / 'file.log').open('w+')
    else:
        prior = input

    rs_mdl.log_output = prior
    prior_log_output = rs_mdl.log_output

    runseeds(rs_mdl, count=1, log_output=func)

    assert rs_mdl.log_output is prior_log_output
