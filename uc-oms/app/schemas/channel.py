"""ChannelConfig 관련 Pydantic 스키마 정의."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ChannelConfigBase(BaseModel):
    """채널 구성 생성/수정 시 공통으로 사용하는 필드."""
    model_config = ConfigDict(populate_by_name=True)
    
    channel_name: str = Field(..., alias="name")
    provider_type: str = Field(..., alias="type")
    api_key: str
    api_secret: str = Field(..., alias="secret_key")


class ChannelConfigCreate(ChannelConfigBase):
    """채널 구성을 생성할 때 사용하는 요청 스키마."""

    pass


class ChannelConfigRead(BaseModel):
    """민감 정보를 제외하고 채널 구성을 노출하는 응답 스키마."""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: int
    channel_name: str = Field(..., alias="name")
    channel_type: str = Field(..., alias="type")
    is_active: bool = Field(..., alias="active")
    last_sync_at: datetime | None = None


class ChannelConfigUpdate(BaseModel):
    """채널 구성 수정 시 사용되는 부분 업데이트 스키마."""
    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )

    channel_name: str | None = Field(None, alias="name")
    channel_type: str | None = Field(None, alias="type")
    api_key: str | None = None
    api_secret: str | None = Field(None, alias="secret_key")
    is_active: bool | None = Field(None, alias="active")

