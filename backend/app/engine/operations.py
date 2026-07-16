"""Associative operations that parameterise the generic segment tree.

The legacy C++ maintained ten hand-written trees (five operations x two
attributes). Here each operation is a small strategy object; one generic
``SegmentTree`` handles build/query/update for all of them.

Semantics are preserved from the original implementation, including identity
elements (sum 0, gcd 0, lcm 1), lcm(0, x) == 0, and tie-breaking on the
*right* index for max/min index queries.
"""
from __future__ import annotations

import math
from typing import Protocol, Sequence


class Operation(Protocol):
    """An associative merge over segment-tree node payloads.

    For value operations (sum/gcd/lcm) the payload is the aggregated value.
    For index operations (max/min) the payload is the index of the winning
    element, so callers can locate the strongest/weakest soldier.
    """

    identity: int

    def leaf(self, index: int, value: int) -> int: ...

    def merge(self, a: int, b: int) -> int: ...


class SumOp:
    identity = 0

    def leaf(self, index: int, value: int) -> int:
        return value

    def merge(self, a: int, b: int) -> int:
        return a + b


class GcdOp:
    identity = 0

    def leaf(self, index: int, value: int) -> int:
        return value

    def merge(self, a: int, b: int) -> int:
        return math.gcd(a, b)


class LcmOp:
    identity = 1

    def leaf(self, index: int, value: int) -> int:
        return value

    def merge(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return a * b // math.gcd(a, b)


class MaxIndexOp:
    """Index of the range maximum over a shared, mutable value list."""

    identity = -1

    def __init__(self, values: Sequence[int]):
        self._values = values

    def leaf(self, index: int, value: int) -> int:
        return index

    def merge(self, a: int, b: int) -> int:
        if a == -1:
            return b
        if b == -1:
            return a
        return a if self._values[a] > self._values[b] else b


class MinIndexOp:
    """Index of the range minimum over a shared, mutable value list."""

    identity = -1

    def __init__(self, values: Sequence[int]):
        self._values = values

    def leaf(self, index: int, value: int) -> int:
        return index

    def merge(self, a: int, b: int) -> int:
        if a == -1:
            return b
        if b == -1:
            return a
        return a if self._values[a] < self._values[b] else b
