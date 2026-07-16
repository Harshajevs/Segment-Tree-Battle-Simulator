"""OpenRouter provider — hosted free-tier models (e.g. llama-3.3-70b:free)."""
from __future__ import annotations

import logging
from typing import Any

import httpx

from app.ai.base import describe_action
from app.ai.ollama import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class OpenRouterCommentaryProvider:
    name = "openrouter"

    def __init__(self, api_key: str, model: str, timeout: float = 8.0,
                 client: httpx.Client | None = None):
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is required for the openrouter provider")
        self._model = model
        self._api_key = api_key
        self._client = client or httpx.Client(
            timeout=timeout, base_url="https://openrouter.ai/api/v1"
        )

    def commentate(self, result: dict[str, Any], team_names: list[str]) -> str | None:
        response = self._client.post(
            "/chat/completions",
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={
                "model": self._model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": describe_action(result, team_names)},
                ],
                "max_tokens": 80,
            },
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        return content or None
