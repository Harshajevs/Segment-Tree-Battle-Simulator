"""Commentary provider contract.

Commentary is decorative: providers may fail, time out, or be unconfigured,
and gameplay must never block on them. The factory wraps every non-local
provider with a fallback to the local template engine.
"""
from __future__ import annotations

from typing import Any, Protocol


class CommentaryProvider(Protocol):
    name: str

    def commentate(self, result: dict[str, Any], team_names: list[str]) -> str | None:
        """Return one or two sentences about an action result, or None."""
        ...


def describe_action(result: dict[str, Any], team_names: list[str]) -> str:
    """Compact, factual prompt/context shared by all LLM providers."""
    attacker = team_names[result["attacker"]]
    defender = team_names[1 - result["attacker"]]
    if result["type"] == "attack":
        return (
            f"Round {result['round']}: {attacker} attacked soldiers "
            f"{result['attack_range'][0]}-{result['attack_range'][1]} "
            f"(attack sum {result['attack_sum']}) against {defender}'s defence "
            f"{result['defense_range'][0]}-{result['defense_range'][1]} "
            f"(health sum {result['defense_sum']}), dealing {result['damage']} damage "
            f"to soldier #{result['target_index']} "
            f"({result['target_health_before']} -> {result['target_health_after']} hp). "
            f"{attacker}'s champion #{result['champion_index']} rallied to "
            f"{result['champion_attack_after']} attack."
        )
    winners = {0: team_names[0], 1: team_names[1], None: "nobody"}
    return (
        f"Round {result['round']} challenge: GCD duel won by "
        f"{winners[result['gcd_winner']]}, LCM duel won by "
        f"{winners[result['lcm_winner']]} (+{result['bonus']} points each)."
    )
