import datetime
from enum import Enum

from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, String
)
from sqlalchemy.orm import relationship

from app.database import Base


class OrderStatus(str, Enum):
    IN_PROCESS = "в процессе"
    SENT = "отправлен"
    DELIVERED = "доставлен"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now()
    )
    status = Column(String, default=OrderStatus.IN_PROCESS)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
