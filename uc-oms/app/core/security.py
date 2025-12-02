from passlib.context import CryptContext
from cryptography.fernet import Fernet
from typing import Optional

from app.core.config import settings

# 1. 비밀번호 해싱을 위한 설정
# bcrypt는 널리 사용되고 안전한 해싱 알고리즘입니다.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 2. Fernet 암호화/복호화 키 설정
# SECRET_KEY를 Fernet 키로 변환하여 사용합니다.
# Fernet 키는 32 URL-safe base64-encoded bytes여야 합니다. 
# settings.SECRET_KEY가 이 요건을 충족하지 않을 경우 예외 처리가 필요할 수 있습니다.
try:
    # SECRET_KEY가 Fernet 요구사항을 충족한다고 가정하고 초기화
    # 실제 프로덕션 환경에서는 settings.SECRET_KEY를 기반으로 Fernet 키를 안전하게 생성하고 관리해야 합니다.
    # 여기서는 간단하게 SECRET_KEY를 Fernet 인스턴스 초기화에 사용합니다.
    cipher = Fernet(settings.SECRET_KEY.encode('utf-8').ljust(44, b'='))
except Exception as e:
    # 실제로는 키 길이가 32바이트가 아닌 경우 등을 처리해야 합니다.
    print(f"Error initializing Fernet: {e}")
    # 임시적으로 더미 키를 사용하거나, 애플리케이션 시작을 중단할 수 있습니다.
    cipher = None


# ==================================
# I. 비밀번호 해싱 함수
# ==================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 해시된 비밀번호를 비교하여 일치 여부를 검증합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    평문 비밀번호를 bcrypt를 사용하여 해시합니다.
    """
    return pwd_context.hash(password)


# ==================================
# II. 데이터 암호화/복호화 함수 (API Keys, Secrets 용도)
# ==================================

def encrypt_data(data: str) -> Optional[str]:
    """
    문자열 데이터를 Fernet을 사용하여 암호화합니다.
    """
    if cipher:
        encoded_data = data.encode()
        encrypted_bytes = cipher.encrypt(encoded_data)
        return encrypted_bytes.decode()
    return None

def decrypt_data(encrypted_data: str) -> Optional[str]:
    """
    암호화된 데이터를 Fernet을 사용하여 복호화합니다.
    """
    if cipher:
        try:
            encrypted_bytes = encrypted_data.encode()
            decrypted_bytes = cipher.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception:
            # 복호화 실패(잘못된 키, 손상된 데이터 등) 시 None 반환
            return None
    return None