"""Generic segment tree with pluggable associative operations.

Preserves the legacy layout: 1-indexed nodes, children at 2i / 2i+1, 4n
storage, O(n) build, O(log n) query and point update. ``update`` returns the
recomputed node path so the frontend can highlight propagation, and
``snapshot`` exports the internal nodes for visualization.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.engine.operations import Operation


@dataclass(frozen=True)
class TreeNode:
    node: int
    start: int
    end: int
    depth: int
    payload: int


class SegmentTree:
    def __init__(self, values: list[int], op: Operation):
        if not values:
            raise ValueError("SegmentTree requires at least one element")
        self.n = len(values)
        self.op = op
        # Shared reference: index operations resolve payloads through this
        # list, and sibling trees over the same attribute mutate it in step.
        self.values = values
        self.tree: list[int] = [op.identity] * (4 * self.n)
        self._build(1, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = self.op.leaf(start, self.values[start])
            return
        mid = (start + end) // 2
        self._build(2 * node, start, mid)
        self._build(2 * node + 1, mid + 1, end)
        self.tree[node] = self.op.merge(self.tree[2 * node], self.tree[2 * node + 1])

    def _check_range(self, left: int, right: int) -> None:
        if not (0 <= left <= right < self.n):
            raise ValueError(
                f"invalid range [{left}, {right}] for size {self.n}: "
                "require 0 <= left <= right < size"
            )

    def query(self, left: int, right: int) -> int:
        self._check_range(left, right)
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, left: int, right: int) -> int:
        if start > right or end < left:
            return self.op.identity
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return self.op.merge(
            self._query(2 * node, start, mid, left, right),
            self._query(2 * node + 1, mid + 1, end, left, right),
        )

    def update(self, pos: int, value: int) -> list[int]:
        """Point-assign ``values[pos] = value``; returns recomputed node ids
        from leaf to root (visualization of update propagation)."""
        if not (0 <= pos < self.n):
            raise ValueError(f"position {pos} out of range for size {self.n}")
        self.values[pos] = value
        path: list[int] = []
        self._update(1, 0, self.n - 1, pos, value, path)
        return path

    def _update(
        self, node: int, start: int, end: int, pos: int, value: int, path: list[int]
    ) -> None:
        if start == end:
            self.tree[node] = self.op.leaf(pos, value)
            path.append(node)
            return
        mid = (start + end) // 2
        if pos <= mid:
            self._update(2 * node, start, mid, pos, value, path)
        else:
            self._update(2 * node + 1, mid + 1, end, pos, value, path)
        self.tree[node] = self.op.merge(self.tree[2 * node], self.tree[2 * node + 1])
        path.append(node)

    def snapshot(self, max_depth: int | None = None) -> list[TreeNode]:
        """Breadth-first export of materialised nodes down to ``max_depth``
        (root is depth 0). Depth-capped so 100k-element trees stay renderable."""
        nodes: list[TreeNode] = []
        queue: list[tuple[int, int, int, int]] = [(1, 0, self.n - 1, 0)]
        while queue:
            node, start, end, depth = queue.pop(0)
            nodes.append(TreeNode(node, start, end, depth, self.tree[node]))
            if start == end or (max_depth is not None and depth >= max_depth):
                continue
            mid = (start + end) // 2
            queue.append((2 * node, start, mid, depth + 1))
            queue.append((2 * node + 1, mid + 1, end, depth + 1))
        return nodes
