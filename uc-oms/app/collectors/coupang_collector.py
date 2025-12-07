import httpx
from typing import List, Dict, Any
from .base_collector import IProductCollector, IOrderCollector
import hmac, hashlib, base64, time
from urllib.parse import urlencode, urlparse

class CoupangCollector(IProductCollector):
    BASE_URL="https://api-gateway.coupang.com"
    
    def _generate_signature(self, method:str, path:str, query: str="") -> Dict[str, str]:
        datetime_gmt = time.strftime("%y%m%d", time.gmtime()) + "T" + time.strftime("%H%M%S", time.gmtime()) + "Z"
        
        if query:
            canonical_path = f"{path}?{query}"
        else:
            canonical_path = path

        message = datetime_gmt + method + canonical_path
        secret_key_bytes = self.api_secret.encode("utf-8")
        
        signature = hmac.new(secret_key_bytes, message.encode('utf-8'), hashlib.sha256).digest()
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        
        authorization_header = (
            f"HMAC-SHA256 accessKey={self.api_key}, "
            f"timestamp={datetime_gmt}, "
            f"signature={signature_base64}"
        )
        
        return{
            "Authorization": authorization_header,
            "Accept": "application/json",
            "Content-type": "application/json;charset=UTF-8" 
        }
        
    async def fetch_products(self, page: int=1, page_size: int=50) -> List[Dict[str,Any]]:
        path = "/v2/providers/seller_api/apis/api/v1/marketplace/seller-products"
        query_params = {'pageSize': page_size, 'page': page}
        
        headers = self._generate_signature("GET", path, query_params)
        
        url = f"{self.BASE_URL}{path}?{query_params}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                products = []
                for item in data.get('data',{}).get('content',[]):
                    products.append({
                        "channel_id": self.channel_id,
                        "external_id": item.get('sellerPoductId'),
                        "product_name": item.get('productName'),
                        "status": item.get('salesStatus'),
                        "channel_type": "coupang"
                    })
                return products
            except httpx.HTTPStatusError as e:
                raise ConnectionError(f"Coupang API Error: {e.response.status_code} - {e.response.text}") from e
            except Exception as e:
                raise ConnectionError(f"Coupang API Connection Failed: {e}") from e

class CoupangOrderCollector(IOrderCollector):
    pass