"""Application configuration — 12-factor, environment-driven, safe defaults."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Segment Tree Battle Simulator"
    log_level: str = "INFO"

    # sqlite locally; set to a Postgres URL (e.g. Neon) in production
    database_url: str = "sqlite:///./battle.db"

    # comma-separated list of allowed frontend origins
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # AI commentary: local (default, no credentials) | ollama | openrouter
    ai_provider: str = "local"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    openrouter_api_key: str = ""
    openrouter_model: str = "meta-llama/llama-3.3-70b-instruct:free"
    ai_timeout_seconds: float = 8.0

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
