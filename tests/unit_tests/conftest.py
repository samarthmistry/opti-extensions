# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Shared fixtures for unit tests."""

import pytest

from opti_extensions import IndexSetND


@pytest.fixture
def setNd_cmb2():
    return IndexSetND(range(2), range(2))


@pytest.fixture
def setNd_cmb3():
    return IndexSetND(range(2), range(2), range(2))
