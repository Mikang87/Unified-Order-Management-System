import httpx, json, time
from typing import List, Dict, Any
from .base_collector import IProductCollector, IOrderCollector

class SmartstoreCollector(IProductCollector):
    BASE_URL = "api.commerce.naver.com"
    AUTH_TOKEN_URL = "/external/v1/oauth2/token"
    
    async def _get_access_token(self) -> str:
        client_id = self.api_key
        client_secret_sign = self.api_secret
        
        timestamp = int(time.time()*1000)
        
        auth_data = {
            "client_id": client_id,
            "client_secret_sign": client_secret_sign,
            "grant_type": "client_credentials",
            "timestamp": timestamp,
            "type": "SELF"
        }
        
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        async with httpx.AsyncClient() as client:
           try:
               response = await client.post(self.AUTH_TOKEN_URL, data=auth_data, headers=headers)
               response.raise_for_status()
               
               token_data = response.json()
               access_token = token_data.get("access_token")
               
               if not access_token:
                   raise ConnectionError(f"Smartstore Token Error: Access token not found in response: {token_data}")
               return access_token
           except httpx.HTTPStatusError as e:
               error_detail = e.response.text
               raise ConnectionError(f"Smartstore API Auth Error: {e.response.status_code} - {error_detail}")
           except Exception as e:
               raise ConnectionError(f"Smartstore API Auth Failed: {e}")
        
    def _get_auth_headers(self, access_token: str) -> Dict[str, str]:
        
        client_id = self.api_key
        
        return{
            "Authorization": f"Bearer {access_token}",
            "client_id": client_id,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
    async def fetch_products(self, page: int=1, size: int=50) -> List[Dict[str,Any]]:
        
        access_token = await self._get_access_token()
        headers = self._get_auth_headers(access_token)
        
        path = "/external/v1/products/search"
        url = self.BASE_URL + path

        payload = {"page": page -1, "size": size}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, content=json.dumps(payload))
                response.raise_for_status()
                raw_data = response.json()
                
                products = []
                for item in raw_data.get("data",{}).get('content',[]):
                    products.append({
                        "channel_id": self.channel_id,
                        "external_id": item.get("id"),
                        "product_name": item.get("name"),
                        "status": item.get("statusType"),
                        "channel_type": "smartstore"
                    })
                return products
            except httpx.HTTPStatusError as e:
                raise ConnectionError(f"Smartstore API Error: {e.response.status_code} - {e.response.text}") from e
            except Exception as e:
                raise ConnectionError(f"Smartstore API Connection Failed: {e}") from e
                    
class SmartstoreOrderCollector(IOrderCollector):
    pass