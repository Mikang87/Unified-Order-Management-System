"""관리자용 채널 설정 CRUD 라우터."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.channel import (
    ChannelConfigCreate,
    ChannelConfigRead,
    ChannelConfigUpdate,
)
from app.services.channel_service import ChannelService

router = APIRouter(prefix="/api/v1/admin/channels", tags=["admin:channels"])
channel_service = ChannelService()


async def admin_auth() -> bool:
    """더미 관리자 인증 의존성."""

    return True


@router.post(
    "/",
    response_model=ChannelConfigRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_channel(
    payload: ChannelConfigCreate,
    _: bool = Depends(admin_auth),
    db: AsyncSession = Depends(get_db),
) -> ChannelConfigRead:
    """새로운 채널 구성을 생성한다."""

    channel = await channel_service.create_channel(db, payload)
    return ChannelConfigRead.model_validate(channel)


@router.get(
    "/",
    response_model=list[ChannelConfigRead],
)
async def list_channels(
    skip: int = 0,
    limit: int = 100,
    _: bool = Depends(admin_auth),
    db: AsyncSession = Depends(get_db),
) -> list[ChannelConfigRead]:
    """채널 구성 목록을 조회한다."""

    channels = await channel_service.get_channels(db, skip=skip, limit=limit)
    return [ChannelConfigRead.model_validate(ch) for ch in channels]


@router.get(
    "/{channel_id}",
    response_model=ChannelConfigRead,
)
async def retrieve_channel(
    channel_id: int,
    _: bool = Depends(admin_auth),
    db: AsyncSession = Depends(get_db),
) -> ChannelConfigRead:
    """식별자로 단일 채널 구성을 조회한다."""

    channel = await channel_service.get_channel(db, channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    return ChannelConfigRead.model_validate(channel)


@router.put(
    "/{channel_id}",
    response_model=ChannelConfigRead,
)
async def update_channel(
    channel_id: int,
    payload: ChannelConfigUpdate,
    _: bool = Depends(admin_auth),
    db: AsyncSession = Depends(get_db),
) -> ChannelConfigRead:
    """채널 구성을 부분 업데이트한다."""

    channel = await channel_service.get_channel(db, channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

    updated = await channel_service.update_channel(db, channel, payload)
    return ChannelConfigRead.model_validate(updated)


@router.delete(
    "/{channel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_channel(
    channel_id: int,
    _: bool = Depends(admin_auth),
    db: AsyncSession = Depends(get_db),
) -> Response:
    """채널 구성을 삭제한다."""

    channel = await channel_service.get_channel(db, channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

    await channel_service.delete_channel(db, channel)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

