"""민감 정보 암복호화를 담당하는 보안 유틸리티."""

from __future__ import annotations

import logging
from typing import Final

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings

logger = logging.getLogger(__name__)


def _create_fernet(secret_key: str) -> Fernet:
    """주어진 시크릿 키로 Fernet 인스턴스를 안전하게 생성한다."""

    try:
        return Fernet(secret_key)
    except (TypeError, ValueError) as exc:
        raise RuntimeError("유효하지 않은 SECRET_KEY 값입니다.") from exc


_fernet: Final[Fernet] = _create_fernet(settings.secret_key)


async def encrypt_data(data: str) -> str:
    """평문 문자열을 암호화하여 Base64 인코딩 문자열로 반환한다."""

    if not data:
        raise ValueError("암호화할 데이터가 비어 있습니다.")
    return _fernet.encrypt(data.encode("utf-8")).decode("utf-8")


async def decrypt_data(data: str) -> str:
    """암호화 문자열을 복호화하여 평문 문자열로 반환한다."""

    if not data:
        raise ValueError("복호화할 데이터가 비어 있습니다.")
    try:
        return _fernet.decrypt(data.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        logger.error("Fernet 복호화 실패: %s", exc)
        raise RuntimeError("복호화에 실패했습니다.") from exc