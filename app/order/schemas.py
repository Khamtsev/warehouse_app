from typing import List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from app.product.schemas import Product


class OrderStatus(str, Enum):
    IN_PROCESS = "в процессе"
    SENT = "отправлен"
    DELIVERED = "доставлен"


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    status: OrderStatus


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True
