"""어플리케이션 환경 설정 로직."""

from __future__ import annotations

from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env 파일을 가능한 한 빨리 로드한다.
load_dotenv()


class Settings(BaseSettings):
    """프로젝트 전역 환경 설정을 보관하는 Pydantic 설정 클래스."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: str = Field(..., alias="SECRET_KEY")


@lru_cache
def get_settings() -> Settings:
    """애플리케이션 전역에서 재사용할 Settings 인스턴스를 반환한다."""

    return Settings()


settings = get_settings()
