from sqlite3 import Connection

from fastapi import APIRouter, Depends

from database import get_db
from schemas import ProductCreate, ProductOut, ProductUpdate
from services.product_service import (
	create_product,
	delete_product,
	get_product,
	list_products,
	update_product,
)

router = APIRouter(tags=["products"])


@router.get("/products")
def list_products_endpoint(db: Connection = Depends(get_db)):
	return list_products(db)


@router.get("/products/{product_id}")
def get_product_endpoint(product_id: int, db: Connection = Depends(get_db)) -> ProductOut:
	return get_product(db, product_id)


@router.post("/products", status_code=201)
def create_product_endpoint(
	product: ProductCreate,
	db: Connection = Depends(get_db),
) -> ProductOut:
	return create_product(db, product)


@router.put("/products/{product_id}")
def update_product_endpoint(
	product_id: int,
	product: ProductUpdate,
	db: Connection = Depends(get_db),
) -> ProductOut:
	return update_product(db, product_id, product)


@router.delete("/products/{product_id}", status_code=204)
def delete_product_endpoint(product_id: int, db: Connection = Depends(get_db)):
	delete_product(db, product_id)
