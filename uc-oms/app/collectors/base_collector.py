from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IProductCollector(ABC):
    """
    모든 외부 채널의 상품 조회 API를 위한 추상 인터페이스
    """
    def __init__(self, channel_id: int, api_key: str, api_secret: str):
        self.channel_id = channel_id
        self.api_key = api_key
        self.api_secret = api_secret

    @abstractmethod
    async def fetch_products(self, page: int=1, page_size: int=50) -> List[Dict[str,Any]]:
        """
        API 키를 사용하여 해당 채널의 상품 목록을 조회하고, 내부 표준화된 상품 형식의 리스트를 반환합니다.
        """
        pass