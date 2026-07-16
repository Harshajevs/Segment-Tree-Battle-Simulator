"""A team: soldier stats plus the five segment trees per attribute."""
from __future__ import annotations

from app.engine.operations import GcdOp, LcmOp, MaxIndexOp, MinIndexOp, SumOp
from app.engine.segment_tree import SegmentTree

ATTRIBUTES = ("attack", "health")
OPERATIONS = ("sum", "max", "min", "gcd", "lcm")


class Team:
    def __init__(self, name: str, soldiers: list[tuple[int, int]]):
        if not soldiers:
            raise ValueError("a team needs at least one soldier")
        self.name = name
        self.attack: list[int] = [attack for attack, _ in soldiers]
        self.health: list[int] = [health for _, health in soldiers]
        self.trees: dict[tuple[str, str], SegmentTree] = {}
        for attribute, values in (("attack", self.attack), ("health", self.health)):
            self.trees[(attribute, "sum")] = SegmentTree(values, SumOp())
            self.trees[(attribute, "gcd")] = SegmentTree(values, GcdOp())
            self.trees[(attribute, "lcm")] = SegmentTree(values, LcmOp())
            self.trees[(attribute, "max")] = SegmentTree(values, MaxIndexOp(values))
            self.trees[(attribute, "min")] = SegmentTree(values, MinIndexOp(values))

    @property
    def size(self) -> int:
        return len(self.attack)

    def query(self, attribute: str, operation: str, left: int, right: int) -> int:
        key = (attribute, operation)
        if key not in self.trees:
            raise ValueError(f"unknown query {attribute}/{operation}")
        return self.trees[key].query(left, right)

    def total_health(self) -> int:
        return self.trees[("health", "sum")].query(0, self.size - 1)

    def set_stat(self, pos: int, attribute: str, value: int) -> dict[str, list[int]]:
        """Assign one stat and propagate through all five trees for that
        attribute. Returns the recomputed node path per operation."""
        if attribute not in ATTRIBUTES:
            raise ValueError(f"unknown attribute {attribute!r}")
        if value < 0:
            raise ValueError("stats cannot be negative")
        paths: dict[str, list[int]] = {}
        for operation in OPERATIONS:
            paths[operation] = self.trees[(attribute, operation)].update(pos, value)
        return paths

    def soldiers(self, offset: int, limit: int) -> list[dict[str, int]]:
        end = min(offset + limit, self.size)
        return [
            {"index": i, "attack": self.attack[i], "health": self.health[i]}
            for i in range(offset, end)
        ]
