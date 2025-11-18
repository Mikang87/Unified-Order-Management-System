"""ChannelConfig ORM 모델 정의."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy Declarative Base 클래스."""

    pass


class ChannelConfig(Base):
    """외부 판매 채널 자격 증명을 저장하는 설정 모델."""

    __tablename__ = "channel_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    provider_type: Mapped[str] = mapped_column(String(50), nullable=False)
    api_key: Mapped[str] = mapped_column(String(512), nullable=False)
    secret_key: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
