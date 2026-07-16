"""Deterministic template commentator — the zero-credential default."""
from __future__ import annotations

from typing import Any

from app.ai.base import describe_action

ATTACK_TEMPLATES = [
    "{attacker} storms the field! {damage} damage crashes into {defender}'s soldier #{target}.",
    "A calculated strike by {attacker} — soldier #{target} of {defender} takes {damage} damage.",
    "{attacker} probes the line. {defender}'s weakest link, #{target}, absorbs {damage} damage.",
    "Brutal efficiency from {attacker}: {damage} damage, and champion #{champion} grows stronger.",
]

NO_DAMAGE_TEMPLATES = [
    "{defender}'s defence holds! {attacker}'s assault breaks against a wall of {defense_sum} health.",
    "{attacker} finds no gap — the strike is fully absorbed by {defender}'s line.",
]

CHALLENGE_TEMPLATE = (
    "Challenge round! GCD duel: {gcd_outcome}. LCM duel: {lcm_outcome}."
)


class LocalCommentaryProvider:
    name = "local"

    def commentate(self, result: dict[str, Any], team_names: list[str]) -> str | None:
        attacker = team_names[result["attacker"]]
        defender = team_names[1 - result["attacker"]]
        if result["type"] == "attack":
            if result["damage"] == 0:
                templates = NO_DAMAGE_TEMPLATES
            else:
                templates = ATTACK_TEMPLATES
            # deterministic variety: rotate by round number
            template = templates[result["round"] % len(templates)]
            return template.format(
                attacker=attacker,
                defender=defender,
                damage=result["damage"],
                target=result.get("target_index"),
                champion=result.get("champion_index"),
                defense_sum=result.get("defense_sum"),
            )
        outcome = lambda winner: (
            f"{team_names[winner]} takes +{result['bonus']}" if winner is not None else "a dead heat, no points"
        )
        return CHALLENGE_TEMPLATE.format(
            gcd_outcome=outcome(result["gcd_winner"]),
            lcm_outcome=outcome(result["lcm_winner"]),
        )


# re-export for provider prompt reuse
__all__ = ["LocalCommentaryProvider", "describe_action"]
