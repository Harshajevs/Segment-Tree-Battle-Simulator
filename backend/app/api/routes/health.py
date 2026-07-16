from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/api/health")
def health() -> dict:
    settings = get_settings()
    return {"status": "ok", "app": settings.app_name, "ai_provider": settings.ai_provider}
