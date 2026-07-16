"""Match endpoints — thin routing/validation layer over MatchService."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Match
from app.engine.battle import BattleEngine
from app.schemas.match import (
    ActionLogItem,
    ActionOut,
    ActionRequest,
    Attribute,
    MatchCreate,
    MatchListItem,
    MatchOut,
    MatchState,
    OperationName,
    QueryOut,
    SoldiersOut,
    TeamSummary,
    TreeOut,
    safe_number,
    sanitize,
)
from app.services.match_service import match_service

router = APIRouter(prefix="/api/matches", tags=["matches"])

VISUALIZER_MAX_DEPTH = 8


def _state(engine: BattleEngine) -> MatchState:
    return MatchState(
        round=engine.state.round,
        scores=list(engine.state.scores),
        attacker=engine.state.attacker,
        status=engine.state.status,
        winner=engine.state.winner,
        expected_action=engine.expected_action,
    )


def _match_out(row: Match, engine: BattleEngine) -> MatchOut:
    teams = [
        TeamSummary(
            index=i,
            name=team.name,
            size=team.size,
            total_health=team.total_health(),
            total_attack=team.query("attack", "sum", 0, team.size - 1),
        )
        for i, team in enumerate(engine.teams)
    ]
    return MatchOut(
        id=row.id,
        created_at=row.created_at,
        team_size=row.team_size,
        seed=row.seed,
        max_rounds=row.max_rounds,
        challenge_interval=row.challenge_interval,
        state=_state(engine),
        teams=teams,
    )


@router.post("", response_model=MatchOut, status_code=201)
def create_match(payload: MatchCreate, db: Session = Depends(get_db)) -> MatchOut:
    row, engine = match_service.create_match(db, payload)
    return _match_out(row, engine)


@router.get("", response_model=list[MatchListItem])
def list_matches(db: Session = Depends(get_db), limit: int = Query(20, ge=1, le=100)):
    rows = db.query(Match).order_by(desc(Match.created_at)).limit(limit).all()
    return [
        MatchListItem(
            id=row.id,
            created_at=row.created_at,
            team_size=row.team_size,
            max_rounds=row.max_rounds,
            status=row.status,
            winner=row.winner,
            round=row.round,
            scores=[row.score_a, row.score_b],
        )
        for row in rows
    ]


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: str, db: Session = Depends(get_db)) -> MatchOut:
    row = match_service.get_match_row(db, match_id)
    engine = match_service.get_engine(db, match_id)
    return _match_out(row, engine)


@router.post("/{match_id}/actions", response_model=ActionOut)
def act(match_id: str, request: ActionRequest, db: Session = Depends(get_db)) -> ActionOut:
    action, engine, result = match_service.act(db, match_id, request)
    commentary = action.commentary
    return ActionOut(
        sequence=action.sequence,
        type=action.type,
        result=sanitize(result),
        commentary=commentary,
        state=_state(engine),
    )


@router.get("/{match_id}/actions", response_model=list[ActionLogItem])
def action_log(match_id: str, db: Session = Depends(get_db)):
    row = match_service.get_match_row(db, match_id)
    return [
        ActionLogItem(
            sequence=a.sequence,
            type=a.type,
            result=sanitize(a.result),
            commentary=a.commentary,
            created_at=a.created_at,
        )
        for a in row.actions
    ]


@router.get("/{match_id}/query", response_model=QueryOut)
def range_query(
    match_id: str,
    team: int = Query(ge=0, le=1),
    attribute: Attribute = Query(),
    operation: OperationName = Query(),
    left: int = Query(ge=0),
    right: int = Query(ge=0),
    db: Session = Depends(get_db),
) -> QueryOut:
    engine = match_service.get_engine(db, match_id)
    side = engine.teams[team]
    value = side.query(attribute, operation, left, right)
    element_value = None
    if operation in ("max", "min"):
        element_value = getattr(side, attribute)[value]
    return QueryOut(
        team=team,
        attribute=attribute,
        operation=operation,
        left=left,
        right=right,
        value=safe_number(value),
        element_value=element_value,
    )


@router.get("/{match_id}/tree", response_model=TreeOut)
def tree_snapshot(
    match_id: str,
    team: int = Query(ge=0, le=1),
    attribute: Attribute = Query(),
    operation: OperationName = Query(),
    max_depth: int = Query(default=5, ge=1, le=VISUALIZER_MAX_DEPTH),
    db: Session = Depends(get_db),
) -> TreeOut:
    engine = match_service.get_engine(db, match_id)
    tree = engine.teams[team].trees[(attribute, operation)]
    nodes = tree.snapshot(max_depth=max_depth)
    return TreeOut(
        team=team,
        attribute=attribute,
        operation=operation,
        size=tree.n,
        max_depth=max_depth,
        nodes=[
            {
                "node": n.node,
                "start": n.start,
                "end": n.end,
                "depth": n.depth,
                "payload": safe_number(n.payload),
            }
            for n in nodes
        ],
    )


@router.get("/{match_id}/soldiers", response_model=SoldiersOut)
def soldiers(
    match_id: str,
    team: int = Query(ge=0, le=1),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=256, ge=1, le=1024),
    db: Session = Depends(get_db),
) -> SoldiersOut:
    engine = match_service.get_engine(db, match_id)
    side = engine.teams[team]
    return SoldiersOut(
        team=team,
        offset=offset,
        total=side.size,
        soldiers=side.soldiers(offset, limit),
    )
