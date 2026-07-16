"""API contracts (Pydantic v2).

Note on big integers: range-LCM values grow multiplicatively and routinely
exceed JavaScript's Number.MAX_SAFE_INTEGER. ``safe_number`` renders anything
above 2^53 as a decimal string so the frontend never silently loses precision
(the legacy C++ simply overflowed here).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, Field


def _force_utc(value: datetime) -> datetime:
    """SQLite drops tzinfo; re-attach UTC so timestamps serialise uniformly."""
    if isinstance(value, datetime) and value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


UTCDateTime = Annotated[datetime, BeforeValidator(_force_utc)]

MAX_SAFE_INTEGER = 2**53 - 1

Attribute = Literal["attack", "health"]
OperationName = Literal["sum", "max", "min", "gcd", "lcm"]
ActionType = Literal["attack", "challenge"]


def safe_number(value: int) -> int | str:
    return value if abs(value) <= MAX_SAFE_INTEGER else str(value)


def sanitize(payload: Any) -> Any:
    """Recursively apply safe_number to every int in a result structure."""
    if isinstance(payload, bool):
        return payload
    if isinstance(payload, int):
        return safe_number(payload)
    if isinstance(payload, dict):
        return {key: sanitize(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [sanitize(item) for item in payload]
    return payload


class MatchCreate(BaseModel):
    team_size: int = Field(default=32, ge=8, le=100_000)
    seed: int = Field(default=42, ge=0, le=2**31 - 1)
    max_rounds: int = Field(default=20, ge=1, le=1000)
    challenge_interval: int = Field(default=10, ge=2, le=100)


class RangeModel(BaseModel):
    left: int = Field(ge=0)
    right: int = Field(ge=0)


class ActionRequest(BaseModel):
    type: ActionType
    attack_range: RangeModel
    defense_range: RangeModel


class TeamSummary(BaseModel):
    index: int
    name: str
    size: int
    total_health: int
    total_attack: int


class MatchState(BaseModel):
    round: int
    scores: list[int]
    attacker: int
    status: str
    winner: int | None
    expected_action: str


class MatchOut(BaseModel):
    id: str
    created_at: UTCDateTime
    team_size: int
    seed: int
    max_rounds: int
    challenge_interval: int
    state: MatchState
    teams: list[TeamSummary]


class MatchListItem(BaseModel):
    id: str
    created_at: UTCDateTime
    team_size: int
    max_rounds: int
    status: str
    winner: int | None
    round: int
    scores: list[int]


class ActionOut(BaseModel):
    sequence: int
    type: ActionType
    result: dict[str, Any]
    commentary: str | None
    state: MatchState


class ActionLogItem(BaseModel):
    sequence: int
    type: ActionType
    result: dict[str, Any]
    commentary: str | None
    created_at: UTCDateTime


class QueryOut(BaseModel):
    team: int
    attribute: Attribute
    operation: OperationName
    left: int
    right: int
    value: int | str
    # for max/min queries: the winning soldier's stat value
    element_value: int | None = None


class TreeNodeOut(BaseModel):
    node: int
    start: int
    end: int
    depth: int
    payload: int | str


class TreeOut(BaseModel):
    team: int
    attribute: Attribute
    operation: OperationName
    size: int
    max_depth: int
    nodes: list[TreeNodeOut]


class SoldierOut(BaseModel):
    index: int
    attack: int
    health: int


class SoldiersOut(BaseModel):
    team: int
    offset: int
    total: int
    soldiers: list[SoldierOut]
