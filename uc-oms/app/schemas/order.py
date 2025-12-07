from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

class OrderItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    external_item_id: str = Field(..., max_length=100)
    product_name: str = Field(..., max_length=255)
    item_price: float = Field(..., ge=0)
    courier_code: Optional[str] = Field(None, max_length=50)
    tracking_number: Optional[str] = Field(None, max_length=100)
    
    umons_status: str = Field(..., max_length=50)
    
class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    channel_id: int
    channel_type: str = Field(..., max_length=50)
    external_order_id: str = Field(..., max_length=100)
    recipient_name: str = Field(..., max_length=100)
    recipient_phone: str = Field(..., max_length=50)
    shipping_address: str

    umos_status: str = Field(..., max_length=50)
    
    items: List[OrderItemBase] = Field(..., min_length=1)
    