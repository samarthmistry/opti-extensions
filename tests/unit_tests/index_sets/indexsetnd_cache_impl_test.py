# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Caching implementation in IndexSetND."""

from collections import defaultdict

from opti_extensions import IndexSet1D, IndexSetND


def test_tupleset_subset_index_groups(setNd_int_cmb2):
    _ = setNd_int_cmb2.subset(0, '*')
    assert (0,) in setNd_int_cmb2._index_groups
    assert setNd_int_cmb2._index_groups[(0,)] == defaultdict(
        list, {(0,): [(0, 0), (0, 1)], (1,): [(1, 0), (1, 1)]}
    )
    assert setNd_int_cmb2.subset(0, '*') == setNd_int_cmb2._index_groups[(0,)][(0,)]

    _ = setNd_int_cmb2.subset('*', 1)
    assert (1,) in setNd_int_cmb2._index_groups
    assert setNd_int_cmb2._index_groups[(1,)] == defaultdict(
        list, {(0,): [(0, 0), (1, 0)], (1,): [(0, 1), (1, 1)]}
    )
    assert setNd_int_cmb2.subset('*', 1) == setNd_int_cmb2._index_groups[(1,)][(1,)]


def test_tupleset_squeeze_index_groups(setNd_int_cmb3):
    _ = setNd_int_cmb3.squeeze(0)
    assert (0,) in setNd_int_cmb3._index_groups
    assert setNd_int_cmb3._index_groups[(0,)] == defaultdict(
        list,
        {
            (0,): [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)],
            (1,): [(1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)],
        },
    )
    assert setNd_int_cmb3.squeeze(0) == IndexSet1D(
        key[0] for key in setNd_int_cmb3._index_groups[(0,)]
    )

    _ = setNd_int_cmb3.squeeze(0, 1)
    assert (0, 1) in setNd_int_cmb3._index_groups
    assert setNd_int_cmb3._index_groups[(0, 1)] == defaultdict(
        list,
        {
            (0, 0): [(0, 0, 0), (0, 0, 1)],
            (0, 1): [(0, 1, 0), (0, 1, 1)],
            (1, 0): [(1, 0, 0), (1, 0, 1)],
            (1, 1): [(1, 1, 0), (1, 1, 1)],
        },
    )
    assert setNd_int_cmb3.squeeze(0, 1) == IndexSetND(setNd_int_cmb3._index_groups[(0, 1)])
