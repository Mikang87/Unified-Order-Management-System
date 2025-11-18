"""채널 설정 비즈니스 로직을 담당하는 Service 계층."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import encrypt_data
from app.models.channel import ChannelConfig
from app.schemas.channel import ChannelConfigCreate, ChannelConfigUpdate


class ChannelService:
    """채널 설정 등록 및 조회 기능을 제공한다."""

    async def create_channel(
        self,
        db: AsyncSession,
        data: ChannelConfigCreate,
    ) -> ChannelConfig:
        """민감 정보를 암호화한 뒤 ChannelConfig 레코드를 생성한다."""

        encrypted_api_key = await encrypt_data(data.api_key)
        encrypted_secret_key = await encrypt_data(data.secret_key)

        channel = ChannelConfig(
            name=data.name,
            provider_type=data.provider_type,
            api_key=encrypted_api_key,
            secret_key=encrypted_secret_key,
        )
        db.add(channel)
        await db.commit()
        await db.refresh(channel)
        return channel

    async def get_channel(self, db: AsyncSession, channel_id: int) -> ChannelConfig | None:
        """식별자로 단일 채널 구성을 조회한다."""

        return await db.get(ChannelConfig, channel_id)

    async def get_channels(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ChannelConfig]:
        """채널 구성 목록을 페이지네이션 파라미터와 함께 조회한다."""

        stmt = select(ChannelConfig).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update_channel(
        self,
        db: AsyncSession,
        db_channel: ChannelConfig,
        data: ChannelConfigUpdate,
    ) -> ChannelConfig:
        """입력된 필드만 갱신하여 채널 구성을 수정한다."""

        update_data = data.model_dump(exclude_unset=True)
        if "api_key" in update_data and update_data["api_key"] is not None:
            update_data["api_key"] = await encrypt_data(update_data["api_key"])
        if "secret_key" in update_data and update_data["secret_key"] is not None:
            update_data["secret_key"] = await encrypt_data(update_data["secret_key"])

        for field, value in update_data.items():
            setattr(db_channel, field, value)

        await db.commit()
        await db.refresh(db_channel)
        return db_channel

    async def delete_channel(self, db: AsyncSession, db_channel: ChannelConfig) -> None:
        """주어진 채널 구성을 삭제한다."""

        await db.delete(db_channel)
        await db.commit()

