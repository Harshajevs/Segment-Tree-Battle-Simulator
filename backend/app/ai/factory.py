"""Provider selection + hard fallback.

Adding a paid provider later = one new class implementing CommentaryProvider
and one branch here; nothing else in the codebase changes.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

from app.ai.base import CommentaryProvider
from app.ai.local import LocalCommentaryProvider
from app.core.config import get_settings

logger = logging.getLogger(__name__)


class FallbackCommentaryProvider:
    """Wraps a primary provider; any exception degrades to the local one."""

    def __init__(self, primary: CommentaryProvider, fallback: CommentaryProvider):
        self._primary = primary
        self._fallback = fallback
        self.name = f"{primary.name}+fallback"

    def commentate(self, result: dict[str, Any], team_names: list[str]) -> str | None:
        try:
            return self._primary.commentate(result, team_names)
        except Exception as exc:  # commentary must never break gameplay
            logger.warning("%s commentary failed (%s); using local", self._primary.name, exc)
            return self._fallback.commentate(result, team_names)


def build_provider(settings) -> CommentaryProvider:
    local = LocalCommentaryProvider()
    try:
        if settings.ai_provider == "ollama":
            from app.ai.ollama import OllamaCommentaryProvider

            primary = OllamaCommentaryProvider(
                settings.ollama_base_url, settings.ollama_model, settings.ai_timeout_seconds
            )
            return FallbackCommentaryProvider(primary, local)
        if settings.ai_provider == "openrouter":
            from app.ai.openrouter import OpenRouterCommentaryProvider

            primary = OpenRouterCommentaryProvider(
                settings.openrouter_api_key,
                settings.openrouter_model,
                settings.ai_timeout_seconds,
            )
            return FallbackCommentaryProvider(primary, local)
    except Exception as exc:
        logger.warning("cannot initialise %s provider (%s); using local", settings.ai_provider, exc)
        return local
    if settings.ai_provider != "local":
        logger.warning("unknown AI_PROVIDER=%r; using local", settings.ai_provider)
    return local


@lru_cache
def get_commentary_provider() -> CommentaryProvider:
    return build_provider(get_settings())
