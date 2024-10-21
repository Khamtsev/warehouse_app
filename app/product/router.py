from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import dao
from app.database import get_db
from .schemas import Product, ProductCreate, ProductUpdate

router = APIRouter(
    prefix='/products',
    tags=['Товары']
)


@router.post('', response_model=Product, summary="Добавить товар")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return dao.create_product(db, product)


@router.get('', response_model=list[Product], summary="Все товары")
def get_products(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    return dao.get_products(db, skip=skip, limit=limit)


@router.get('/{product_id}', response_model=Product,
            summary="Информация о товаре по id")
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = dao.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Продукт {db_product} не найден."
        )
    return db_product


@router.put('/{product_id}', response_model=Product,
            summary="Обновить товар по id")
def update_product(
    product_id: int, product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return dao.update_product(db, product_id, product)


@router.delete('/{product_id}', response_model=Product,
               summary="Удалить товар по id")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return dao.delete_product(db, product_id)
