# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution
from typing_extensions import assert_type

from opti_extensions._misc_types import SupportsWrite
from opti_extensions.docplex import (
    print_problem_stats,
    print_solution_quality_stats,
    runseeds,
    solve,
    tune,
)


class CustomWriter:
    def write(self, s: str, /) -> int:
        return len(s)

    def flush(self) -> None:
        pass


mdl = Model()
writer = CustomWriter()

# Positive checks: SupportsWrite structural protocol satisfaction
sw: SupportsWrite = writer

# Positive checks: solve with typed kwargs and SupportsWrite
assert_type(solve(mdl), SolveSolution | None)
assert_type(solve(mdl, log_output=writer), SolveSolution | None)
assert_type(
    solve(mdl, log_output=True, clean_before_solve=True, checker='std'),
    SolveSolution | None,
)

# Positive checks: runseeds and tune
runseeds(mdl, count=5, log_output=writer)
assert_type(
    tune(mdl, fixed_params_and_values={'timelimit': 100}, log_output=writer),
    dict[str, int | float],
)
print_problem_stats(mdl)
print_solution_quality_stats(mdl)

# Negative checks: invalid solve checker option
solve(mdl, checker='invalid_checker')  # type: ignore[arg-type]

# Negative checks: unknown solve kwargs
solve(mdl, unknown_kwarg=123)  # type: ignore[call-arg]

# Negative checks: runseeds disallows False/None log_output
runseeds(mdl, log_output=False)  # type: ignore[arg-type]

# Negative checks: fixed_params_and_values should be a Mapping
tune(mdl, fixed_params_and_values=[1, 2])  # type: ignore[arg-type]
