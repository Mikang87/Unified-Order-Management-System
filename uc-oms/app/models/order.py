from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, ForeignKey, Text, func
from sqlalchemy.orm import relationship, Mapped
from app.core.database import Base
from typing import List

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channel_configs.id"), nullable=False)
    external_order_id = Column(String(100), unique=True, index=True, nullable=False)
    channel_type = Column(String(50), nullable=False)
    
    order_date = Column(DateTime, nullable=False)
    total_amount = Column(Numeric(10,2), nullable=False)
    
    recipient_name = Column(String(100), nullable=False)
    recipient_phone = Column(String(50), nullable=False)
    shipping_address = Column(Text, nullable=False)
    
    umos_status = Column(String(50), index=True, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key= True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    external_item_id = Column(String(100), index=True, nullable=False)
    
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_price = Column(Numeric(10,2), nullable=False)
    
    courier_name = Column(String(50), nullable=False)
    tracking_number = Column(String(100), nullable=False)
    
    umos_status = Column(String(50), index=True, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    order: Mapped["Order"] = relationship(back_populates="items")