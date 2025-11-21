from fastapi import APIRouter
from app.services.channel_service import fetch_orders_from_external_api
from typing import List, Dict, Any

router = APIRouter(prefix="/test/collector", tags=["Test Collector (MOCK)"])

@router.get("/orders/{channel_id}", response_model=List[Dict[str, Any]])
async def get_mock_orders(channel_id: int):
    orders = await fetch_orders_from_external_api(channel_config_id=channel_id)
    return orders