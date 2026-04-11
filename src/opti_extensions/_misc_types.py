# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Miscellaneous types."""

from typing import Any, Protocol, TypeVar

_AttrT = TypeVar('_AttrT')


class MinimalRepresentationPrinter(Protocol):
    """Minimal protocol for `IPython.lib.pretty.RepresentationPrinter`."""

    def text(self, obj: str) -> None: ...
    def pretty(self, obj: Any) -> None: ...
