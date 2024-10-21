from sqlalchemy.orm import Session
from fastapi import HTTPException

from .schemas import OrderCreate
from .models import Order, OrderItem
from app.product.dao import get_product


def create_order(db: Session, order: OrderCreate):
    """Создает новый заказ в базе данных."""
    db_order = Order(status="в процессе")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        product = get_product(db, item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f'Продукт {item.product_id} не найден'
            )
        if product.in_stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f'На складе недостаточно продукта. '
                    f'Доступно: {product.in_stock}. '
                    f'Запрошено: {item.quantity}.'
                )
            )
        product.in_stock -= item.quantity
        db.commit()
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)

    db.commit()
    return db_order


def get_order(db: Session, order_id: int):
    """Получает заказ по его ID из базы данных."""
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    """Получает список заказов с учетом пагинации."""
    return db.query(Order).offset(skip).limit(limit).all()


def update_order_status(db: Session, order_id: int, status: str):
    """Обновляет статус заказа по его ID."""
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order
