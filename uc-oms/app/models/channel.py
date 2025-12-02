from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base # (선언적 기본 클래스)
from app.core.database import Base # core/database.py에서 정의된 Base 클래스를 가져옵니다.


# 1. ORM 모델 클래스 정의
class ChannelConfig(Base):
    """
    외부 쇼핑몰 채널의 연결 설정 정보를 저장하는 ORM 모델입니다.
    """
    __tablename__ = "channel_configs" # DB에 생성될 테이블 이름

    # 기본 키 및 고유 식별자
    id = Column(Integer, primary_key=True, index=True) 

    # 채널 식별 정보
    channel_name = Column(String(50), unique=True, index=True, nullable=False) # 관리자에게 표시될 이름 (예: 쿠팡-Mikang87점)
    channel_type = Column(String(50), nullable=False)                         # 채널 종류 (예: coupang, naver_smartstore)

    # API 연동 정보 (민감 데이터)
    # String 필드에 암호화된 문자열이 저장됩니다.
    api_key = Column(String(255), nullable=False) 
    api_secret = Column(String(255), nullable=False)

    # 관리 및 상태 정보
    is_active = Column(Boolean, default=True) # 주문 수집 활성화 여부
    
    # 타임스탬프
    created_at = Column(DateTime, default=func.now()) # 레코드 생성 시간
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) # 레코드 마지막 업데이트 시간

    # 디버깅을 위한 표현 메서드
    def __repr__(self):
        return f"<ChannelConfig(id={self.id}, name='{self.channel_name}', type='{self.channel_type}', active={self.is_active})>"