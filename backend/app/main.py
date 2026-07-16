"""FastAPI application factory."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health, matches
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.database import init_db
from app.services.match_service import MatchNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name, version="2.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(MatchNotFoundError)
    async def match_not_found(request: Request, exc: MatchNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"error": {"message": f"match {exc} not found"}})

    @app.exception_handler(ValueError)
    async def domain_error(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"error": {"message": str(exc)}})

    app.include_router(health.router)
    app.include_router(matches.router)
    return app


app = create_app()
