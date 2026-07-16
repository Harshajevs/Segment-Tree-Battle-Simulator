"""Persistence model: a match's config + ordered action log.

Engine state is deliberately NOT serialised — matches are deterministic given
(seed, actions), so state is rehydrated by replay (see MatchService). The
denormalised score/round/status columns exist for cheap listing queries.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    team_size: Mapped[int] = mapped_column(Integer, nullable=False)
    seed: Mapped[int] = mapped_column(Integer, nullable=False)
    max_rounds: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_interval: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(String(16), default="in_progress")
    winner: Mapped[int | None] = mapped_column(Integer, nullable=True)
    round: Mapped[int] = mapped_column(Integer, default=1)
    attacker: Mapped[int] = mapped_column(Integer, default=0)
    score_a: Mapped[int] = mapped_column(Integer, default=0)
    score_b: Mapped[int] = mapped_column(Integer, default=0)

    actions: Mapped[list["Action"]] = relationship(
        back_populates="match", cascade="all, delete-orphan", order_by="Action.sequence"
    )


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("matches.id"), index=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(16), nullable=False)

    # canonical replay inputs
    attack_left: Mapped[int] = mapped_column(Integer, nullable=False)
    attack_right: Mapped[int] = mapped_column(Integer, nullable=False)
    defense_left: Mapped[int] = mapped_column(Integer, nullable=False)
    defense_right: Mapped[int] = mapped_column(Integer, nullable=False)

    # denormalised outcome for history display (never used for replay)
    result: Mapped[dict] = mapped_column(JSON, nullable=False)
    commentary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    match: Mapped[Match] = relationship(back_populates="actions")
