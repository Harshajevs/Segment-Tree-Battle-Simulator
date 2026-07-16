"""Ollama provider — free, fully local LLM inference."""
from __future__ import annotations

import logging
from typing import Any

import httpx

from app.ai.base import describe_action

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an excitable esports commentator for a turn-based strategy game. "
    "Given a factual battle event, respond with ONE vivid sentence of commentary. "
    "No preamble, no quotes."
)


class OllamaCommentaryProvider:
    name = "ollama"

    def __init__(self, base_url: str, model: str, timeout: float = 8.0,
                 client: httpx.Client | None = None):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._client = client or httpx.Client(timeout=timeout)

    def commentate(self, result: dict[str, Any], team_names: list[str]) -> str | None:
        response = self._client.post(
            f"{self._base_url}/api/chat",
            json={
                "model": self._model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": describe_action(result, team_names)},
                ],
            },
        )
        response.raise_for_status()
        content = response.json()["message"]["content"].strip()
        return content or None
