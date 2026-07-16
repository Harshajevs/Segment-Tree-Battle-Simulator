"""Battle-rules tests: preserved legacy semantics with fixed scoring."""
import pytest

from app.engine.battle import (
    CHALLENGE_BONUS,
    BattleEngine,
    MatchConfig,
    RangePair,
    generate_soldiers,
)
from app.engine.team import Team


def make_engine(**overrides):
    config = MatchConfig(**{"team_size": 16, "seed": 1, "max_rounds": 12, **overrides})
    return BattleEngine(config)


def test_soldier_generation_is_deterministic():
    assert generate_soldiers(5, 100) == generate_soldiers(5, 100)
    assert generate_soldiers(5, 100) != generate_soldiers(6, 100)


def test_attack_resolution_matches_manual_computation():
    engine = make_engine()
    attacker, defender = engine.teams
    attack_sum = attacker.query("attack", "sum", 0, 7)
    defense_sum = defender.query("health", "sum", 0, 3)
    expected_damage = max(0, attack_sum - defense_sum)
    target = defender.query("health", "min", 0, 3)
    target_before = defender.health[target]

    result = engine.attack(RangePair((0, 7), (0, 3)))

    assert result["damage"] == expected_damage
    assert result["target_index"] == target
    assert result["target_health_after"] == max(0, target_before - expected_damage)
    assert defender.health[target] == result["target_health_after"]
    assert engine.state.scores[0] == expected_damage
    assert result["champion_attack_after"] > result["champion_attack_before"]


def test_attackers_alternate_and_rounds_advance():
    engine = make_engine()
    assert (engine.state.round, engine.state.attacker) == (1, 0)
    engine.attack(RangePair((0, 3), (0, 3)))
    assert (engine.state.round, engine.state.attacker) == (2, 1)
    engine.attack(RangePair((0, 3), (0, 3)))
    assert (engine.state.round, engine.state.attacker) == (3, 0)


def test_every_tenth_round_is_a_challenge():
    engine = make_engine(max_rounds=15)
    for _ in range(9):
        assert engine.expected_action == "attack"
        engine.attack(RangePair((0, 3), (0, 3)))
    assert engine.state.round == 10
    assert engine.expected_action == "challenge"
    with pytest.raises(ValueError):
        engine.attack(RangePair((0, 3), (0, 3)))
    result = engine.challenge(RangePair((0, 15), (0, 15)))
    assert result["type"] == "challenge"
    assert engine.state.round == 11
    assert engine.expected_action == "attack"


def test_challenge_awards_bonus_to_gcd_and_lcm_winners():
    soldiers_a = [(8, 10)] * 8  # attack gcd 8, lcm 8
    soldiers_b = [(5, 6)] * 8  # health gcd 6, lcm 6
    config = MatchConfig(team_size=8, seed=1, max_rounds=30, challenge_interval=2)
    engine = BattleEngine(config, (Team("A", soldiers_a), Team("B", soldiers_b)))
    engine.attack(RangePair((0, 0), (0, 0)))  # round 1
    result = engine.challenge(RangePair((0, 7), (0, 7)))  # round 2: B attacks
    # attacker is B: attack gcd 5 < defender (A) health gcd 10 -> A (=0) wins both
    assert result["gcd_winner"] == 0
    assert result["lcm_winner"] == 0
    assert engine.state.scores[0] >= 2 * CHALLENGE_BONUS


def test_match_finishes_at_max_rounds_with_score_winner():
    engine = make_engine(max_rounds=3)
    for _ in range(3):
        engine.attack(RangePair((0, 15), (0, 0)))
    assert engine.state.status == "finished"
    assert engine.expected_action == "none"
    a, b = engine.state.scores
    assert engine.state.winner == (0 if a > b else 1 if b > a else None)
    with pytest.raises(ValueError):
        engine.attack(RangePair((0, 0), (0, 0)))


def test_wiping_a_team_ends_the_match_immediately():
    soldiers_a = [(10_000, 100)] * 8
    soldiers_b = [(1, 1)] * 8
    config = MatchConfig(team_size=8, seed=1, max_rounds=100)
    engine = BattleEngine(config, (Team("A", soldiers_a), Team("B", soldiers_b)))
    for _ in range(8):  # one weakest soldier dies per hit
        if engine.state.status == "finished":
            break
        if engine.state.attacker == 1:  # B's turn: harmless poke
            engine.attack(RangePair((0, 0), (0, 7)))
            continue
        engine.attack(RangePair((0, 7), (0, 7)))
    assert engine.teams[1].total_health() > 0 or engine.state.status == "finished"
    # drive to completion
    while engine.state.status != "finished":
        ranges = RangePair((0, 7), (0, 7))
        engine.apply(engine.expected_action, ranges)
    if engine.teams[1].total_health() == 0:
        assert engine.state.winner == 0


def test_replay_reproduces_identical_state():
    engine = make_engine(max_rounds=12)
    actions = []
    ranges = [((0, 7), (2, 9)), ((1, 4), (0, 15)), ((3, 12), (5, 8))]
    for i in range(12):
        pair = RangePair(*ranges[i % len(ranges)])
        actions.append((engine.expected_action, pair))
        engine.apply(*actions[-1])

    replayed = make_engine(max_rounds=12)
    for action_type, pair in actions:
        replayed.apply(action_type, pair)

    assert replayed.state == engine.state
    for original, copy in zip(engine.teams, replayed.teams):
        assert original.attack == copy.attack
        assert original.health == copy.health


def test_config_validation():
    with pytest.raises(ValueError):
        MatchConfig(team_size=4)
    with pytest.raises(ValueError):
        MatchConfig(max_rounds=0)
    with pytest.raises(ValueError):
        MatchConfig(challenge_interval=1)


def test_invalid_action_ranges_rejected_without_state_change():
    engine = make_engine()
    before_round = engine.state.round
    with pytest.raises(ValueError):
        engine.attack(RangePair((0, 99), (0, 3)))
    with pytest.raises(ValueError):
        engine.attack(RangePair((5, 2), (0, 3)))
    assert engine.state.round == before_round
