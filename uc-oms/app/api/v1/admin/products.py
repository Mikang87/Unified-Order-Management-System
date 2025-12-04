from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.product_service import ProductCollectorService
from typing import List, Dict, Any

router = APIRouter(prefix="/products", tags=["Admin Products"])

@router.get(
    "/{channel_id}/fetch", 
    response_model=List[Dict[str,Any]], 
    summary="특정 채널로부터 상품 목록 조회 (API 통신)"
)
async def fetch_products_endpoint(
    channel_id: int, 
    page: int=1, 
    page_size: int=50, 
    db:AsyncSession = Depends(get_db)):
    try:
        service = ProductCollectorService(db=db)
        products = await service.fetch_products_from_channel(
            channel_id=channel_id,
            page=page,
            page_size=page_size
        )
        return products
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotImplementedError as e:
        # 해당 채널 타입에 대한 Collector가 구현되지 않은 경우
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail=str(e))
    except ConnectionError as e:
        # 외부 API 통신 실패 (Collector에서 발생)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail=f"External API communication failed: {e}")
    except RuntimeError as e:
        # 복호화 오류 등 심각한 구성 오류
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal system error: {e}")
    
@router.get(
    "/fetch_all", 
    response_model=List[Dict[str,Any]], 
    summary="모든 활성 채널로부터 상품 목록 일괄 조회 (API 통신)")
async def fetch_all_products_endpoint(
    page: int=1,
    page_size: int=50,
    db:AsyncSession = Depends(get_db)
):
    try:
        service = ProductCollectorService(db=db)
        products = await service.fetch_all_products(
            page=page,
            page_size=page_size
            
        )
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An unexpected error occurred during bulk fetch: {e}"
        )
        