import logging
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.channel import ChannelConfig
from app.models.order import Order, OrderItem
from app.schemas.order import OrderBase, OrderItemBase
from app.core.security import decrypt_data
from app.collectors.base_collector import IOrderCollector
from app.collectors.coupang_collector import CoupangOrderCollector
from app.collectors.smartstore_collector import SmartstoreOrderCollector
from app.collectors.mock_collector import MockCollector

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ORDER_COLLECTOR_MAPPING={
    "coupang": CoupangOrderCollector,
    "smartstore": SmartstoreOrderCollector,
    "mock": MockCollector
}

class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def _get_channel_collector(self, channel_id: int) -> IOrderCollector:
        stmt = select(ChannelConfig).where(ChannelConfig.id == channel_id, ChannelConfig.is_active == True)
        result = await self.db.execute(stmt)
        channel_config = result.scalar_one_or_none()
        
        if not channel_config:
            raise ValueError(f"Channel with ID {channel_id} not found or is inactive")
        
        channel_type = channel_config.channel_type
        
        if channel_type not in ORDER_COLLECTOR_MAPPING:
            raise NotImplementedError(f"Order Collector for channel type '{channel_type}' is not implemented.")
        
        try:
            decrypted_api_key = decrypt_data(channel_config.api_key)
            decrypted_api_secret = decrypt_data(channel_config.api_secret)
        except ValueError as e:
            raise RuntimeError(f"Configuration error: {channel_id}")
        
        CollectorClass: type[IOrderCollector] = ORDER_COLLECTOR_MAPPING[channel_type]
        
        return CollectorClass(
            channel_id = channel_config.id,
            api_key = decrypted_api_key,
            api_secret = decrypted_api_secret
        )
        
    async def fetch_and_save_orders(self, channel_id:int, start_date: str, end_date: str) -> int:
        collector = await self._get_channel_collector(channel_id)
        
        raw_orders_data: List[Dict[str, Any]] = await collector.fetch_orders(start_date,end_date)
        
        if not raw_orders_data:
            logger.info(f"Channel {channel_id}: No new orders fetched.")
            return 0
        
        validated_orders: List[OrderBase] = [OrderBase(**data) for data in raw_orders_data]
        saved_count = await self._save_orders_to_db(validated_orders)
        
        return saved_count
    
    async def _save_orders_to_db(self, orders: List[OrderBase]) -> int:
        order_count=0
        
        for order_data in orders:
            order_stmt = select(Order).where(Order.external_order_id == order_data.external_order_id)
            order_result = await self.db.execute(order_stmt)
            existing_order = order_result.scalar_one_or_none()
            
            order_params = Order.order_data.model_dump(exclude={"items"})
            
            if existing_order:
                update_stmt = update(Order).where(Order.id == existing_order.id).values(**order_params)
                await self.db.execute(update_stmt)
                db_order = existing_order
                logger.debug(f"Updated existing Order: {db_order.external_order_id}")
            else:
                db_order = Order(**order_params)
                self.db.add(db_order)
                await self.db.flush()
                logger.debug(f"Created new Order: {db_order.external_order_id}")
                
            for item_data in order_data.items:
                item_stmt = select(OrderItem).where(
                    OrderItem.external_item_id == item_data.external_item_id,
                    OrderItem.order_id == db_order.id
                )
                item_result = await self.db.execute(item_stmt)
                existing_item = item_result.scalar_one_or_none()
                
                item_params = item_data.model_dump()
                item_params["order_id"] = db_order.id

                if existing_item:
                    update_item_stmt = update(OrderItem).where(OrderItem.id == existing_item.id).values(**item_params)
                    await self.db.execute(update_item_stmt)
                    logger.debug(f"Updated existing OrderItem: {existing_item.external_item_id}")
                else:
                    db_item = OrderItem(**item_params)
                    self.db.add(db_item)
                    logger.debug(f"Created new OrderItem: {db_item.external_item_id}")
            
            order_count += 1
            
        await self.db.commit()
        return order_count