from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from . import dao
from .schemas import Order, OrderCreate

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.post('', response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return dao.create_order(db, order)


@router.get('', response_model=list[Order])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return dao.get_orders(db, skip=skip, limit=limit)


@router.get('/{order_id}', response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = dao.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(
            status_code=404,
            detail="Заказ {db_order} не найден."
        )
    return db_order


@router.patch('/{order_id}/status', response_model=Order)
def update_order_status(
    order_id: int, status: str,
    db: Session = Depends(get_db)
):
    return dao.update_order_status(db, order_id, status)
