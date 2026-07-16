"""Battle rules engine — pure domain logic, no I/O.

Preserves the legacy game with its audited bugs fixed (see docs/AUDIT.md and
docs/PRD.md section 5):

- teams alternate as attacker each round (legacy: Team A always attacked and
  both scores received the same value);
- damage = max(0, attackSum(range) - healthSum(defence range));
- damage lands on the defender's weakest soldier (min-health index query) and
  the attacker's strongest soldier (max-attack index query) gains a rally
  bonus — the point-update-after-query flow of the original, with coherent
  semantics;
- every ``challenge_interval``-th round is a GCD/LCM challenge worth +50 per
  comparison (legacy awarded GCD only; LCM now also scores);
- the match ends at ``max_rounds`` or when a team's total health reaches 0.

Everything is deterministic given (seed, action sequence), which is what makes
replay-based rehydration possible.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from app.engine.team import Team

CHALLENGE_BONUS = 50
ATTACK_MIN, ATTACK_MAX = 50, 200
HEALTH_MIN, HEALTH_MAX = 500, 1500


@dataclass(frozen=True)
class MatchConfig:
    team_size: int = 32
    seed: int = 42
    max_rounds: int = 20
    challenge_interval: int = 10

    def __post_init__(self) -> None:
        if not (8 <= self.team_size <= 100_000):
            raise ValueError("team_size must be within [8, 100000]")
        if not (1 <= self.max_rounds <= 1000):
            raise ValueError("max_rounds must be within [1, 1000]")
        if self.challenge_interval < 2:
            raise ValueError("challenge_interval must be >= 2")


def generate_soldiers(seed: int, team_size: int) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Deterministic replacement for the legacy data/team*.txt files."""
    rng = random.Random(seed)
    make = lambda: [
        (rng.randint(ATTACK_MIN, ATTACK_MAX), rng.randint(HEALTH_MIN, HEALTH_MAX))
        for _ in range(team_size)
    ]
    return make(), make()


@dataclass
class RangePair:
    attack_range: tuple[int, int]
    defense_range: tuple[int, int]


@dataclass
class BattleState:
    round: int = 1
    scores: list[int] = field(default_factory=lambda: [0, 0])
    attacker: int = 0
    status: str = "in_progress"  # in_progress | finished
    winner: int | None = None  # 0 / 1 / None (tie or unfinished)


class BattleEngine:
    def __init__(self, config: MatchConfig, teams: tuple[Team, Team] | None = None):
        self.config = config
        if teams is None:
            soldiers_a, soldiers_b = generate_soldiers(config.seed, config.team_size)
            teams = (Team("Team A", soldiers_a), Team("Team B", soldiers_b))
        self.teams = teams
        self.state = BattleState()

    # ------------------------------------------------------------------ api

    @property
    def expected_action(self) -> str:
        if self.state.status == "finished":
            return "none"
        if self.state.round % self.config.challenge_interval == 0:
            return "challenge"
        return "attack"

    def attack(self, ranges: RangePair) -> dict[str, Any]:
        self._require("attack")
        attacker, defender = self._sides()
        al, ar = self._validate(attacker, ranges.attack_range)
        dl, dr = self._validate(defender, ranges.defense_range)

        attack_sum = attacker.query("attack", "sum", al, ar)
        defense_sum = defender.query("health", "sum", dl, dr)
        damage = max(0, attack_sum - defense_sum)

        target_index = defender.query("health", "min", dl, dr)
        target_health_before = defender.health[target_index]
        update_paths: dict[str, dict[str, list[int]]] = {}
        if damage > 0:
            new_health = max(0, target_health_before - damage)
            update_paths["defender_health"] = defender.set_stat(
                target_index, "health", new_health
            )

        champion_index = attacker.query("attack", "max", al, ar)
        champion_attack_before = attacker.attack[champion_index]
        rally = max(1, champion_attack_before // 20)
        update_paths["attacker_attack"] = attacker.set_stat(
            champion_index, "attack", champion_attack_before + rally
        )

        self.state.scores[self.state.attacker] += damage
        result = {
            "type": "attack",
            "round": self.state.round,
            "attacker": self.state.attacker,
            "attack_range": [al, ar],
            "defense_range": [dl, dr],
            "attack_sum": attack_sum,
            "defense_sum": defense_sum,
            "damage": damage,
            "target_index": target_index,
            "target_health_before": target_health_before,
            "target_health_after": defender.health[target_index],
            "champion_index": champion_index,
            "champion_attack_before": champion_attack_before,
            "champion_attack_after": attacker.attack[champion_index],
            "update_paths": update_paths,
        }
        self._advance()
        return result

    def challenge(self, ranges: RangePair) -> dict[str, Any]:
        """GCD/LCM surprise round: attacker's attack vs defender's health."""
        self._require("challenge")
        attacker, defender = self._sides()
        al, ar = self._validate(attacker, ranges.attack_range)
        dl, dr = self._validate(defender, ranges.defense_range)

        gcd_a = attacker.query("attack", "gcd", al, ar)
        gcd_d = defender.query("health", "gcd", dl, dr)
        lcm_a = attacker.query("attack", "lcm", al, ar)
        lcm_d = defender.query("health", "lcm", dl, dr)

        gcd_winner = self._award(gcd_a, gcd_d)
        lcm_winner = self._award(lcm_a, lcm_d)

        result = {
            "type": "challenge",
            "round": self.state.round,
            "attacker": self.state.attacker,
            "attack_range": [al, ar],
            "defense_range": [dl, dr],
            "gcd_attacker": gcd_a,
            "gcd_defender": gcd_d,
            "gcd_winner": gcd_winner,
            "lcm_attacker": lcm_a,
            "lcm_defender": lcm_d,
            "lcm_winner": lcm_winner,
            "bonus": CHALLENGE_BONUS,
        }
        self._advance()
        return result

    def apply(self, action_type: str, ranges: RangePair) -> dict[str, Any]:
        """Uniform dispatch used both by the API and by replay rehydration."""
        if action_type == "attack":
            return self.attack(ranges)
        if action_type == "challenge":
            return self.challenge(ranges)
        raise ValueError(f"unknown action type {action_type!r}")

    # ------------------------------------------------------------- internals

    def _sides(self) -> tuple[Team, Team]:
        return self.teams[self.state.attacker], self.teams[1 - self.state.attacker]

    def _require(self, action_type: str) -> None:
        if self.state.status == "finished":
            raise ValueError("match is already finished")
        if self.expected_action != action_type:
            raise ValueError(
                f"round {self.state.round} expects a {self.expected_action!r} action"
            )

    @staticmethod
    def _validate(team: Team, rng: tuple[int, int]) -> tuple[int, int]:
        left, right = rng
        if not (0 <= left <= right < team.size):
            raise ValueError(
                f"invalid range [{left}, {right}] for {team.name} of size {team.size}"
            )
        return left, right

    def _award(self, attacker_value: int, defender_value: int) -> int | None:
        if attacker_value > defender_value:
            self.state.scores[self.state.attacker] += CHALLENGE_BONUS
            return self.state.attacker
        if defender_value > attacker_value:
            self.state.scores[1 - self.state.attacker] += CHALLENGE_BONUS
            return 1 - self.state.attacker
        return None

    def _advance(self) -> None:
        for team_index, team in enumerate(self.teams):
            if team.total_health() == 0:
                self.state.status = "finished"
                self.state.winner = 1 - team_index
                return
        if self.state.round >= self.config.max_rounds:
            self.state.status = "finished"
            a, b = self.state.scores
            self.state.winner = 0 if a > b else 1 if b > a else None
            return
        self.state.round += 1
        self.state.attacker = 1 - self.state.attacker
