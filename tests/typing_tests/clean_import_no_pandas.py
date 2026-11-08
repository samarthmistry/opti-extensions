# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Verify core opti_extensions structures type-check cleanly without pandas imported."""

from typing_extensions import assert_type

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND

s1: IndexSet1D[str] = IndexSet1D(['A', 'B'])
snd: IndexSetND[tuple[str, int]] = IndexSetND(['A', 'B'], [1, 2])
p1: ParamDict1D[str, int] = ParamDict1D({'A': 1, 'B': 2})
pnd: ParamDictND[tuple[str, int], float] = ParamDictND({('A', 1): 1.5, ('B', 2): 2.5})

assert_type(s1, IndexSet1D[str])
assert_type(snd, IndexSetND[tuple[str, int]])
assert_type(p1, ParamDict1D[str, int])
assert_type(pnd, ParamDictND[tuple[str, int], float])
