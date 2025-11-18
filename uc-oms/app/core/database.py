"""비동기 데이터베이스 연결과 세션 유틸리티를 제공한다."""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 의존성에서 사용 가능한 비동기 DB 세션을 생성하고 반환한다."""

    async with AsyncSessionLocal() as session:
        yield session
