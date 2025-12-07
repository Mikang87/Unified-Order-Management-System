from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from typing import List, Dict, Any

router = APIRouter(prefix="/orders", tags=['Admin Orders'])

@router.get("/", response_model=List[Dict[str,Any]], summary="주문 목록 조회")
async def get_orders_list_endpoint(
    db: AsyncSession = Depends(get_db)
):
    return[
        {"order_id": 1001, "channel_name": "coupang", "status": "PAYMENT_COMPLETE"},
        {"order_id": 1002, "channel_name": "smartstore", "status": "SHIPPING_PREPARE"},
    ]
    
@router.get("/channels/{channel_id}/fetch", response_model=List[Dict[str,Any]], summary="특정 채널로부터 주문 목록 수집 (API 통신)")
async def fetch_orders_from_channel_endpoint(
    channel_id: int,
    db: AsyncSession = Depends(get_db)
):
    return [{"message": f"Fetching orders from channel {channel_id} is not fully implemented yet."}]