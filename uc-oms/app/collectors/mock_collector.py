import json, time, hmac, hashlib, base64, logging
from typing import List, Dict, Any
from .base_collector import IProductCollector, IOrderCollector
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MockCollector(IProductCollector):
    BASE_URL = "test.mockCollector.test"
    
    
    async def fetch_products(self, page: int=1, page_size: int=50) -> List[Dict[str, Any]]:
        timestamp = time.strftime("%y%m%d", time.gmtime()) + "T" + time.strftime("%H%M%S", time.gmtime()) + "Z"
        method = "GET"
        path = "/v2/mock/products"
        message = timestamp + method + path

        signature = hmac.new(self.api_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        signatureBase64 = base64.b64encode(signature).decode('utf-8')
        
        mock_auth_header = {
            "client_id": self.api_key,
            "client_key": self.api_secret,
            "signature": signatureBase64,
            "timestamp": timestamp,
            "path": path
        }
        
        mock_products = [
            {
                "channel_id": self.channel_id,
                "external_id": "P_MOCK_1001_",
                "product_name": f"{self.channel_id} - 테스트 상품 A",
                "status": "SALE",
                "channel_type": "mock",
                "auth_result": mock_auth_header # 테스트 결과를 데이터에 첨부
            },
            {
                "channel_id": self.channel_id,
                "external_id": "P_MOCK_1002_",
                "product_name": f"{self.channel_id} - 테스트 상품 B",
                "status": "SOLD_OUT",
                "channel_type": "mock",
                "auth_result": mock_auth_header
            }
        ]
        return mock_products
    
    async def fetch_orders(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        channel_name = f"MockChannel_{self.channel_id}"
        
        mock_orders = [
            # 주문 1: 상품 2개
            {
                "channel_id": self.channel_id,
                "channel_type": "mock",
                "external_order_id": f"O_MOCK_{self.channel_id}_10001",
                "order_date": (datetime.now() - timedelta(hours=1)),
                "total_amount": 35000.0,
                "recipient_name": "홍길동",
                "recipient_phone": "010-1234-5678",
                "shipping_address": "서울시 강남구 테스트로 123",
                "uoms_status": "PAID",
                "items": [
                    {
                        "external_item_id": f"I_MOCK_{self.channel_id}_10001_A",
                        "product_name": f"{channel_name} - 노트북 파우치",
                        "quantity": 1,
                        "item_price": 20000.0,
                        "courier_code": None,
                        "tracking_number": None,
                        "uoms_status": "PAID"
                    },
                    {
                        "external_item_id": f"I_MOCK_{self.channel_id}_10001_B",
                        "product_name": f"{channel_name} - 키보드",
                        "quantity": 1,
                        "item_price": 15000.0,
                        "courier_code": None,
                        "tracking_number": None,
                        "uoms_status": "PAID"
                    }
                ]
            }
        ]
        
        return mock_orders
    
    async def confirm_order_preparation(self, order_item_ids: List[str]) -> bool:
        logger.info(f"Mock: Confirmed preparation for items: {order_item_ids}")
        return True
    
    async def register_tracking_and_ship(self, order_item_id: str, courier_code: str, tracking_number: str) -> bool:
        logger.info(f"Mock: Resigstered tracking for item {order_item_id} with {courier_code}/{tracking_number}")
        return True