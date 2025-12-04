from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.channel import ChannelConfig
from app.core.security import decrypt_data
from app.collectors.base_collector import IProductCollector
from app.collectors.coupang_collector import CoupangCollector
from app.collectors.smartstore_collector import SmartstoreCollector
from app.collectors.mock_collector import MockCollector
from sqlalchemy import select

COLLECTOR_MAPPING = {
        "coupang": CoupangCollector,
        "smartstore": SmartstoreCollector,
        "mock": MockCollector
}

class ProductCollectorService:
        def __init__(self, db:AsyncSession):
                self.db = db
                
        async def fetch_products_from_channel(self, channel_id: int, page: int=1, page_size: int=50) -> List[Dict[str,Any]]:
                stmt = select(ChannelConfig).where(ChannelConfig.id == channel_id, ChannelConfig.is_active == True)
                result= await self.db.execute(stmt)
                channel_config = result.scalar_one_or_none()
                
                if not channel_config:
                        raise ValueError(f"Channel with ID {channel_id} not found or is inactive.")
                
                channel_type = channel_config.channel_type
                
                if channel_type not in COLLECTOR_MAPPING:
                        raise NotImplementedError(f"Collector for channel type '{channel_type}' is not implemented.")
                
                try:
                        decrypted_api_key = decrypt_data(channel_config.api_key)
                        decrypted_api_secret = decrypt_data(channel_config.api_secret)
                except ValueError as e:
                        raise RuntimeError(f"Configuration error: Failed to decrypt API keys for channel {channel_id}.")
                
                CollectorClass: type[IProductCollector] = COLLECTOR_MAPPING[channel_type]
                
                collector = CollectorClass(
                        channel_id=channel_id,
                        api_key=decrypted_api_key,
                        api_secret=decrypted_api_secret
                )
                
                products = await collector.fetch_products(page=page, page_size=page_size)
                return products
        
        async def fetch_all_products(self, page: int=1, page_size: int=50) -> List[Dict[str, Any]]:
                stmt = select(ChannelConfig.id).where(ChannelConfig.is_active==True)
                result = await self.db.execute(stmt)
                active_channel_ids: List[int] = result.scalars().all()
                
                all_products = []
                
                for channel_id in active_channel_ids:
                        try:
                                products = await self.fetch_products_from_channel(
                                        channel_id=channel_id,
                                        page=page,
                                        page_size=page_size
                                )                       
                                all_products.extend(products)
                        except Exception as e:
                                print(f"Warning: Failed to fetch products for channel ID {channel_id}. Error: {e}")
                                continue
                return all_products
                        