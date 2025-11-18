"""ChannelConfig 관련 Pydantic 스키마 정의."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Extra


class ChannelConfigBase(BaseModel):
    """채널 구성 생성/수정 시 공통으로 사용하는 필드."""

    name: str
    provider_type: str
    api_key: str
    secret_key: str


class ChannelConfigCreate(ChannelConfigBase):
    """채널 구성을 생성할 때 사용하는 요청 스키마."""

    pass


class ChannelConfigRead(BaseModel):
    """민감 정보를 제외하고 채널 구성을 노출하는 응답 스키마."""

    id: int
    name: str
    provider_type: str
    is_active: bool
    last_sync_at: datetime | None = None

    class Config:
        """ORM 객체와의 호환 설정."""

        from_attributes = True


class ChannelConfigUpdate(BaseModel):
    """채널 구성 수정 시 사용되는 부분 업데이트 스키마."""

    name: str | None = None
    provider_type: str | None = None
    api_key: str | None = None
    secret_key: str | None = None
    is_active: bool | None = None

    class Config:
        """허용되지 않은 필드를 차단한다."""

        extra = Extra.forbid
