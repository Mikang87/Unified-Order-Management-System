from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.core import security

from app.models.channel import ChannelConfig
from app.schemas.channel import ChannelConfigCreate, ChannelConfigUpdate

# 가상의 주문 데이터 정의 (MOCK DATA)
MOCK_ORDER_DATA= [
    {
        "external_order_id": "MOCK-1",
        "provider_type": "coupang",
        "order_date": "2025-11-20T10:00:00Z",
        "total-amount": 45000,
        "product_name": "Mocking test A"
    },
    {
        "external_order_id": "MOCK-2",
        "provider_type": "coupang",
        "order_date": "2025-11-20T10:01:11Z",
        "total-amount": 21000,
        "product_name": "Mocking test B"   
    },
    {
        "external_order_id": "MOCK-3",
        "provider_type": "smartstore",
        "order_date": "2025-11-20T10:21:22Z",
        "total-amount": 11000,
        "product_name": "Mocking test C"   
    }
]

# 특정 채널 ID의 설정 정보를 사용하여 외부 API에서 주문 데이터를 수집하는 함수
async def fetch_orders_from_external_api(channel_config_id: int) -> list[Dict[str,Any]]:
    if settings.MOCK_COLLECTOR:
        print(f"--- MOKE MODE: 채널 ID {channel_config_id}의 가상 주문 데이터를 반환합니다.")
        return MOCK_ORDER_DATA
    
    return []

# 1. CREATE: 채널 생성
async def create_channel(db: AsyncSession, channel: ChannelConfigCreate) -> ChannelConfig:
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
        channel_type=channel.provider_type,
        api_key=encrypted_key,       # 암호화된 키 저장
        api_secret=encrypted_secret, # 암호화된 시크릿 저장
        is_active=True
    )
    
    db.add(db_channel)
    await db.commit()
    await db.refresh(db_channel)
    return db_channel

# 2. READ: 채널 조회 (단일)
async def get_channel(db: AsyncSession, channel_id: int) -> Optional[ChannelConfig]:
    """
    ID를 기준으로 단일 채널 정보를 조회합니다.
    """
    stmt = select(ChannelConfig).where(ChannelConfig.id == channel_id)
    result = await db.execute(stmt)
    # DB 조회는 models.channel.py의 ChannelConfig를 사용
    return result.scalar_one_or_none()

# 3. READ: 채널 목록 조회
async def get_channels(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ChannelConfig]:
    """
    채널 목록을 조회합니다. (Pagination 적용)
    """
    stmt = select(ChannelConfig).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())
# 4. UPDATE: 채널 수정
async def update_channel(db: AsyncSession, channel_id: int, channel_update: ChannelConfigUpdate) -> Optional[ChannelConfig]:
    """
    ID에 해당하는 채널 정보를 업데이트합니다.
    api_key나 api_secret이 제공되면 암호화 후 업데이트합니다.
    """
    db_channel = await get_channel(db, channel_id)

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
            
        await db.commit()
        await db.refresh(db_channel)
        return db_channel
    
    return None

# 5. DELETE: 채널 삭제
async def delete_channel(db: AsyncSession, channel_id: int) -> bool:
    """
    ID를 기준으로 채널을 삭제합니다.
    """
    stmt = delete(ChannelConfig).where(ChannelConfig.id==channel_id)
    result = await db.execute(stmt)
    
    if result.rowcount > 0:
        await db.commit()
        return True
        
    return False

# 6. 유틸리티: 복호화된 Secret 가져오기
async def get_decrypted_secret(db: AsyncSession, channel_id: int) -> Optional[str]:
    """
    주문 수집을 위해 사용할, 복호화된 API Secret을 반환합니다.
    """
    db_channel = await get_channel(db, channel_id)
    
    if db_channel and db_channel.api_secret:
        # 🚨 핵심 보안 로직: 암호화된 Secret을 복호화
        return security.decrypt_data(db_channel.api_secret)
        
    return None