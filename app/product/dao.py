from sqlalchemy.orm import Session

from .schemas import ProductCreate, ProductUpdate
from .models import Product


def create_product(db: Session, product: ProductCreate):
    """Создает новый продукт в базе данных."""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    """Получает продукт по его ID из базы данных."""
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def get_products(db: Session, skip: int = 0, limit: int = 10):
    """Получает список продуктов с учетом пагинации."""
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(
    db: Session, product_id: int,
    product: ProductUpdate
):
    """Обновляет информацию о продукте по его ID."""
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    """Удаляет продукт из базы данных по его ID."""
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
