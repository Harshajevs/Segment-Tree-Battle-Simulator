"""Correctness tests for the generic segment tree.

The core guarantee: every operation, on every range, always matches a naive
O(n) recomputation — including after randomized interleaved updates. This is
the test suite the legacy C++ never had (its index-update trees were broken
for two years without anyone noticing).
"""
import math
import random

import pytest

from app.engine.operations import GcdOp, LcmOp, MaxIndexOp, MinIndexOp, SumOp
from app.engine.segment_tree import SegmentTree
from app.engine.team import Team


def naive(values, operation, left, right):
    window = values[left : right + 1]
    if operation == "sum":
        return sum(window)
    if operation == "gcd":
        return math.gcd(*window) if len(window) > 1 else window[0]
    if operation == "lcm":
        acc = 1
        for v in window:
            acc = 0 if (acc == 0 or v == 0) else acc * v // math.gcd(acc, v)
        return acc
    if operation == "max":  # legacy tie-break: rightmost wins
        best = left
        for i in range(left, right + 1):
            if values[i] > values[best] or (values[i] == values[best] and i > best):
                best = i
        return best
    if operation == "min":
        best = left
        for i in range(left, right + 1):
            if values[i] < values[best] or (values[i] == values[best] and i > best):
                best = i
        return best
    raise AssertionError(operation)


def build_tree(values, operation):
    shared = list(values)
    ops = {
        "sum": lambda: SumOp(),
        "gcd": lambda: GcdOp(),
        "lcm": lambda: LcmOp(),
        "max": lambda: MaxIndexOp(shared),
        "min": lambda: MinIndexOp(shared),
    }
    return SegmentTree(shared, ops[operation]())


OPERATIONS = ["sum", "gcd", "lcm", "max", "min"]


@pytest.mark.parametrize("operation", OPERATIONS)
def test_all_ranges_match_naive_on_build(operation):
    rng = random.Random(7)
    values = [rng.randint(0, 60) for _ in range(23)]
    tree = build_tree(values, operation)
    for left in range(len(values)):
        for right in range(left, len(values)):
            assert tree.query(left, right) == naive(values, operation, left, right), (
                operation,
                left,
                right,
            )


@pytest.mark.parametrize("operation", OPERATIONS)
def test_randomized_update_query_sequences(operation):
    rng = random.Random(1216)
    values = [rng.randint(1, 100) for _ in range(64)]
    tree = build_tree(values, operation)
    reference = list(tree.values)  # same initial content, independent copy
    for _ in range(500):
        if rng.random() < 0.5:
            pos, value = rng.randrange(64), rng.randint(0, 100)
            tree.update(pos, value)
            reference[pos] = value
        else:
            left = rng.randrange(64)
            right = rng.randrange(left, 64)
            assert tree.query(left, right) == naive(reference, operation, left, right)
    assert tree.values == reference


def test_update_returns_leaf_to_root_path():
    tree = build_tree([1, 2, 3, 4, 5, 6, 7, 8], "sum")
    path = tree.update(5, 99)
    assert path[-1] == 1  # root recomputed last
    assert len(path) == 4  # depth of an 8-leaf tree
    for child, parent in zip(path, path[1:]):
        assert parent == child // 2


def test_invalid_ranges_rejected():
    tree = build_tree([1, 2, 3], "sum")
    for left, right in [(-1, 2), (0, 3), (2, 1)]:
        with pytest.raises(ValueError):
            tree.query(left, right)
    with pytest.raises(ValueError):
        tree.update(3, 1)


def test_single_element_tree():
    tree = build_tree([42], "gcd")
    assert tree.query(0, 0) == 42
    tree.update(0, 18)
    assert tree.query(0, 0) == 18


def test_snapshot_depth_cap_and_coverage():
    tree = build_tree(list(range(1, 17)), "sum")
    nodes = tree.snapshot(max_depth=2)
    assert max(n.depth for n in nodes) == 2
    root = next(n for n in nodes if n.node == 1)
    assert (root.start, root.end, root.payload) == (0, 15, sum(range(1, 17)))
    # children of any exported internal node partition its range
    by_id = {n.node: n for n in nodes}
    for n in nodes:
        if 2 * n.node in by_id:
            left, right = by_id[2 * n.node], by_id[2 * n.node + 1]
            assert (left.start, right.end) == (n.start, n.end)
            assert left.end + 1 == right.start


def test_team_updates_propagate_to_all_five_trees():
    rng = random.Random(3)
    soldiers = [(rng.randint(1, 50), rng.randint(1, 50)) for _ in range(20)]
    team = Team("T", soldiers)
    paths = team.set_stat(11, "attack", 999)
    assert set(paths) == {"sum", "max", "min", "gcd", "lcm"}
    assert team.query("attack", "max", 0, 19) == 11
    assert team.query("attack", "sum", 11, 11) == 999
    # health trees untouched
    assert team.query("health", "sum", 0, 19) == sum(h for _, h in soldiers)
