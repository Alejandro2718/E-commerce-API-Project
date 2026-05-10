from fastapi import FastAPI

from database import init_db
from routers import auth_router, orders_router, products_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
	init_db()

app.include_router(products_router.router)
app.include_router(orders_router.router)
app.include_router(auth_router.router)