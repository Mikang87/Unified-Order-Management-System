import json, time, hmac, hashlib, base64
from typing import List, Dict, Any
from .base_collector import IProductCollector

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