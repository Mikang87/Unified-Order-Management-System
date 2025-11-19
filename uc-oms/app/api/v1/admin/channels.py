from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from services import channel_service
from schemas.channel import ChannelCreate, ChannelUpdate, ChannelRead

# 1. FastAPI 라우터 객체 생성
# prefix와 tags를 설정하여 Swagger/Redoc 문서에서 경로와 그룹을 명시합니다.
router = APIRouter(
    prefix="/channels",
    tags=["Admin Channel Configuration"]
)

# 2. CRUD 엔드포인트 정의

# ----------------------------------------------------
# 2.1. 채널 생성 (Create)
# ----------------------------------------------------
@router.post(
    "/", 
    response_model=ChannelRead, 
    status_code=status.HTTP_201_CREATED,
    summary="새로운 쇼핑몰 채널을 등록하고 API Secret을 암호화하여 저장"
)
def create_channel_endpoint(
    channel: ChannelCreate, 
    db: Session = Depends(get_db) # DB 세션 의존성 주입
):
    """
    관리자로부터 채널 설정 정보를 받아 암호화 후 저장합니다.
    """
    # Service 계층의 create_channel 함수 호출
    db_channel = channel_service.create_channel(db, channel)
    
    # ChannelRead 스키마로 변환되어 응답 (보안을 위해 API Secret은 제외됨)
    return db_channel

# ----------------------------------------------------
# 2.2. 채널 목록 조회 (Read All)
# ----------------------------------------------------
@router.get(
    "/", 
    response_model=List[ChannelRead],
    summary="등록된 모든 채널 설정 정보를 페이지네이션하여 조회"
)
def read_channels_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db) # DB 세션 의존성 주입
):
    """
    등록된 채널 목록을 조회합니다.
    """
    # Service 계층의 get_channels 함수 호출
    channels = channel_service.get_channels(db, skip=skip, limit=limit)
    return channels

# ----------------------------------------------------
# 2.3. 단일 채널 조회 (Read One)
# ----------------------------------------------------
@router.get(
    "/{channel_id}", 
    response_model=ChannelRead,
    summary="특정 ID의 채널 정보를 조회"
)
def read_channel_endpoint(
    channel_id: int, 
    db: Session = Depends(get_db)
):
    # Service 계층의 get_channel 함수 호출
    db_channel = channel_service.get_channel(db, channel_id=channel_id)
    
    if db_channel is None:
        # 해당 ID의 채널이 없을 경우 404 에러 반환
        raise HTTPException(status_code=404, detail="Channel not found")
        
    return db_channel

# ----------------------------------------------------
# 2.4. 채널 수정 (Update)
# ----------------------------------------------------
@router.put(
    "/{channel_id}", 
    response_model=ChannelRead,
    summary="특정 ID의 채널 정보를 수정 (API Secret이 포함되면 자동 암호화)"
)
def update_channel_endpoint(
    channel_id: int, 
    channel: ChannelUpdate,
    db: Session = Depends(get_db)
):
    # Service 계층의 update_channel 함수 호출
    updated_channel = channel_service.update_channel(db, channel_id, channel)
    
    if updated_channel is None:
        # 수정 대상 채널이 없을 경우 404 에러 반환
        raise HTTPException(status_code=404, detail="Channel not found")
        
    return updated_channel

# ----------------------------------------------------
# 2.5. 채널 삭제 (Delete)
# ----------------------------------------------------
@router.delete(
    "/{channel_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="특정 ID의 채널을 삭제"
)
def delete_channel_endpoint(
    channel_id: int, 
    db: Session = Depends(get_db)
):
    # Service 계층의 delete_channel 함수 호출
    if not channel_service.delete_channel(db, channel_id):
        # 삭제 실패 (채널이 존재하지 않는 경우) 404 에러 반환
        raise HTTPException(status_code=404, detail="Channel not found")
        
    # 성공적인 삭제는 204 No Content로 응답 본문을 보내지 않습니다.
    return