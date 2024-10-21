from fastapi import FastAPI

from app.product.router import router as product_router
from app.order.router import router as order_router

app = FastAPI()

app.include_router(product_router)
app.include_router(order_router)
