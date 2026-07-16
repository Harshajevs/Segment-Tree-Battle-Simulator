"""AI commentary provider tests — network providers use injected fake
transports; no real calls ever happen in the test suite."""
import httpx
import pytest

from app.ai.factory import FallbackCommentaryProvider, build_provider
from app.ai.local import LocalCommentaryProvider
from app.ai.ollama import OllamaCommentaryProvider
from app.ai.openrouter import OpenRouterCommentaryProvider
from app.core.config import Settings

ATTACK_RESULT = {
    "type": "attack",
    "round": 3,
    "attacker": 0,
    "attack_range": [0, 7],
    "defense_range": [0, 3],
    "attack_sum": 900,
    "defense_sum": 700,
    "damage": 200,
    "target_index": 2,
    "target_health_before": 800,
    "target_health_after": 600,
    "champion_index": 5,
    "champion_attack_before": 150,
    "champion_attack_after": 157,
}

CHALLENGE_RESULT = {
    "type": "challenge",
    "round": 10,
    "attacker": 1,
    "gcd_winner": 0,
    "lcm_winner": None,
    "bonus": 50,
}

TEAMS = ["Team A", "Team B"]


def test_local_provider_is_deterministic_and_complete():
    provider = LocalCommentaryProvider()
    first = provider.commentate(ATTACK_RESULT, TEAMS)
    assert first == provider.commentate(ATTACK_RESULT, TEAMS)
    assert "200" in first and "Team A" in first

    challenge = provider.commentate(CHALLENGE_RESULT, TEAMS)
    assert "Team A takes +50" in challenge
    assert "dead heat" in challenge

    blocked = provider.commentate({**ATTACK_RESULT, "damage": 0, "defense_sum": 999}, TEAMS)
    assert "999" in blocked or "absorbed" in blocked


def _fake_client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://openrouter.ai/api/v1")


def test_ollama_provider_parses_chat_response():
    def handler(request):
        assert request.url.path == "/api/chat"
        return httpx.Response(200, json={"message": {"content": " What a strike! "}})

    provider = OllamaCommentaryProvider(
        "http://localhost:11434", "llama3.2",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    assert provider.commentate(ATTACK_RESULT, TEAMS) == "What a strike!"


def test_openrouter_provider_parses_completion():
    def handler(request):
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(
            200, json={"choices": [{"message": {"content": "Devastating blow!"}}]}
        )

    provider = OpenRouterCommentaryProvider("test-key", "some/model:free", client=_fake_client(handler))
    assert provider.commentate(ATTACK_RESULT, TEAMS) == "Devastating blow!"


def test_openrouter_requires_key():
    with pytest.raises(ValueError):
        OpenRouterCommentaryProvider("", "some/model:free")


def test_fallback_degrades_to_local_on_error():
    def handler(request):
        return httpx.Response(500)

    broken = OllamaCommentaryProvider(
        "http://localhost:11434", "llama3.2",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    provider = FallbackCommentaryProvider(broken, LocalCommentaryProvider())
    commentary = provider.commentate(ATTACK_RESULT, TEAMS)
    assert commentary is not None and "200" in commentary


def test_factory_selection():
    assert build_provider(Settings(ai_provider="local")).name == "local"
    assert build_provider(Settings(ai_provider="ollama")).name == "ollama+fallback"
    assert (
        build_provider(Settings(ai_provider="openrouter", openrouter_api_key="k")).name
        == "openrouter+fallback"
    )
    # unknown provider and missing key both degrade safely to local
    assert build_provider(Settings(ai_provider="nonsense")).name == "local"
    assert build_provider(Settings(ai_provider="openrouter", openrouter_api_key="")).name == "local"


def test_api_actions_include_commentary(client_and_match):
    client, match_id = client_and_match
    response = client.post(
        f"/api/matches/{match_id}/actions",
        json={
            "type": "attack",
            "attack_range": {"left": 0, "right": 7},
            "defense_range": {"left": 0, "right": 3},
        },
    )
    assert response.status_code == 200
    assert response.json()["commentary"]

    log = client.get(f"/api/matches/{match_id}/actions").json()
    assert log[-1]["commentary"] == response.json()["commentary"]
