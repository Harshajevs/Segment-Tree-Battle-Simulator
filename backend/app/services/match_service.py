"""Match lifecycle orchestration.

Engine instances live in an in-process registry keyed by match id. If the
process restarts (deploy, crash), ``_rehydrate`` rebuilds the exact engine
state by regenerating soldiers from the seed and replaying the persisted
action log — matches are deterministic by construction.
"""
from __future__ import annotations

import logging
import threading
from typing import Any

from sqlalchemy.orm import Session

from app.db.models import Action, Match
from app.engine.battle import BattleEngine, MatchConfig, RangePair
from app.schemas.match import ActionRequest, MatchCreate

logger = logging.getLogger(__name__)


class MatchNotFoundError(LookupError):
    pass


class MatchService:
    def __init__(self) -> None:
        self._engines: dict[str, BattleEngine] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- create

    def create_match(self, db: Session, payload: MatchCreate) -> tuple[Match, BattleEngine]:
        config = MatchConfig(
            team_size=payload.team_size,
            seed=payload.seed,
            max_rounds=payload.max_rounds,
            challenge_interval=payload.challenge_interval,
        )
        engine = BattleEngine(config)
        row = Match(
            team_size=config.team_size,
            seed=config.seed,
            max_rounds=config.max_rounds,
            challenge_interval=config.challenge_interval,
        )
        db.add(row)
        db.commit()
        with self._lock:
            self._engines[row.id] = engine
        logger.info("match %s created (size=%d seed=%d)", row.id, config.team_size, config.seed)
        return row, engine

    # ------------------------------------------------------------------ read

    def get_match_row(self, db: Session, match_id: str) -> Match:
        row = db.get(Match, match_id)
        if row is None:
            raise MatchNotFoundError(match_id)
        return row

    def get_engine(self, db: Session, match_id: str) -> BattleEngine:
        with self._lock:
            engine = self._engines.get(match_id)
        if engine is not None:
            return engine
        return self._rehydrate(db, match_id)

    def _rehydrate(self, db: Session, match_id: str) -> BattleEngine:
        row = self.get_match_row(db, match_id)
        config = MatchConfig(
            team_size=row.team_size,
            seed=row.seed,
            max_rounds=row.max_rounds,
            challenge_interval=row.challenge_interval,
        )
        engine = BattleEngine(config)
        for action in row.actions:  # ordered by sequence
            engine.apply(
                action.type,
                RangePair(
                    (action.attack_left, action.attack_right),
                    (action.defense_left, action.defense_right),
                ),
            )
        with self._lock:
            self._engines[match_id] = engine
        logger.info("match %s rehydrated from %d actions", match_id, len(row.actions))
        return engine

    # ------------------------------------------------------------------- act

    def act(
        self,
        db: Session,
        match_id: str,
        request: ActionRequest,
        commentary: str | None = None,
    ) -> tuple[Action, BattleEngine, dict[str, Any]]:
        engine = self.get_engine(db, match_id)
        row = self.get_match_row(db, match_id)
        ranges = RangePair(
            (request.attack_range.left, request.attack_range.right),
            (request.defense_range.left, request.defense_range.right),
        )
        result = engine.apply(request.type, ranges)

        # update paths are visualization hints, too bulky for the audit log
        persisted = {k: v for k, v in result.items() if k != "update_paths"}
        action = Action(
            match_id=match_id,
            sequence=len(row.actions) + 1,
            type=request.type,
            attack_left=ranges.attack_range[0],
            attack_right=ranges.attack_range[1],
            defense_left=ranges.defense_range[0],
            defense_right=ranges.defense_range[1],
            result=persisted,
            commentary=commentary,
        )
        row.status = engine.state.status
        row.winner = engine.state.winner
        row.round = engine.state.round
        row.attacker = engine.state.attacker
        row.score_a, row.score_b = engine.state.scores
        db.add(action)
        db.commit()
        return action, engine, result

    # --------------------------------------------------------------- helpers

    def drop_from_cache(self, match_id: str) -> None:
        """Test hook: simulate a process restart for one match."""
        with self._lock:
            self._engines.pop(match_id, None)


match_service = MatchService()
