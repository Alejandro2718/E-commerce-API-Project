from sqlite3 import Connection

from fastapi import APIRouter, Depends

from database import get_db
from services.product_service import list_products

router = APIRouter(tags=["products"])


@router.get("/products")
def list_products_endpoint(db: Connection = Depends(get_db)):
	return list_products(db)
