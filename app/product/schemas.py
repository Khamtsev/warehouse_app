from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    in_stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[int] = None


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
