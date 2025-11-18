"""FastAPI 애플리케이션 엔트리 포인트."""

from __future__ import annotations

from fastapi import FastAPI

# from app.api.v1.admin import channels


def create_app() -> FastAPI:
    """FastAPI 애플리케이션을 초기화하고 라우터를 연결한다."""

    application = FastAPI(title="UC-OMS", version="0.1.0")
    # application.include_router(channels.router, prefix="/api/v1/admin", tags=["channels"])
    return application


app = create_app()
