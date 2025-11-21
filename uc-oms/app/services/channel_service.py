from sqlalchemy.orm import Session
from typing import List, Optional

from models.channel import ChannelConfig
from schemas.channel import ChannelConfigCreate, ChannelConfigUpdate
from core import security

# ====================================================================
# 1. CREATE: 채널 생성
# ====================================================================

def create_channel(db: Session, channel: ChannelConfigCreate) -> ChannelConfig:
    """
    새 채널 정보를 DB에 저장합니다. 
    저장 전 api_key와 api_secret을 암호화합니다.
    """
    
    # 🚨 핵심 보안 로직: 민감 정보를 암호화
    encrypted_key = security.encrypt_data(channel.api_key)
    encrypted_secret = security.encrypt_data(channel.api_secret)
    
    # 암호화된 데이터와 나머지 데이터를 ORM 모델에 맞게 준비
    db_channel = ChannelConfig(
        channel_name=channel.channel_name,
        channel_type=channel.channel_type,
        api_key=encrypted_key,       # 암호화된 키 저장
        api_secret=encrypted_secret, # 암호화된 시크릿 저장
        is_active=channel.is_active
    )
    
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

# ====================================================================
# 2. READ: 채널 조회 (단일)
# ====================================================================

def get_channel(db: Session, channel_id: int) -> Optional[ChannelConfig]:
    """
    ID를 기준으로 단일 채널 정보를 조회합니다.
    """
    # DB 조회는 models.channel.py의 ChannelConfig를 사용
    return db.query(ChannelConfig).filter(ChannelConfig.id == channel_id).first()

# ====================================================================
# 3. READ: 채널 목록 조회
# ====================================================================

def get_channels(db: Session, skip: int = 0, limit: int = 100) -> List[ChannelConfig]:
    """
    채널 목록을 조회합니다. (Pagination 적용)
    """
    return db.query(ChannelConfig).offset(skip).limit(limit).all()

# ====================================================================
# 4. UPDATE: 채널 수정
# ====================================================================

def update_channel(db: Session, channel_id: int, channel_update: ChannelConfigUpdate) -> Optional[ChannelConfig]:
    """
    ID에 해당하는 채널 정보를 업데이트합니다.
    api_key나 api_secret이 제공되면 암호화 후 업데이트합니다.
    """
    db_channel = get_channel(db, channel_id)

    if db_channel:
        update_data = channel_update.model_dump(exclude_unset=True) # 변경된 필드만 가져옴
        
        # 🚨 핵심 보안 로직: API 키/시크릿이 변경된 경우 암호화
        if "api_key" in update_data:
            update_data["api_key"] = security.encrypt_data(update_data["api_key"])
        
        if "api_secret" in update_data:
            update_data["api_secret"] = security.encrypt_data(update_data["api_secret"])
            
        # Pydantic dict를 ORM 객체에 적용
        for key, value in update_data.items():
            setattr(db_channel, key, value)
            
        db.commit()
        db.refresh(db_channel)
        return db_channel
    
    return None

# ====================================================================
# 5. DELETE: 채널 삭제
# ====================================================================

def delete_channel(db: Session, channel_id: int) -> bool:
    """
    ID를 기준으로 채널을 삭제합니다.
    """
    db_channel = get_channel(db, channel_id)
    
    if db_channel:
        db.delete(db_channel)
        db.commit()
        return True
        
    return False

# ====================================================================
# 6. 유틸리티: 복호화된 Secret 가져오기
# ====================================================================

def get_decrypted_secret(db: Session, channel_id: int) -> Optional[str]:
    """
    주문 수집을 위해 사용할, 복호화된 API Secret을 반환합니다.
    """
    db_channel = get_channel(db, channel_id)
    
    if db_channel and db_channel.api_secret:
        # 🚨 핵심 보안 로직: 암호화된 Secret을 복호화
        return security.decrypt_data(db_channel.api_secret)
        
    return None