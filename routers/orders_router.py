from sqlite3 import Connection

from fastapi import APIRouter, Depends

from auth_dependencies import require_basic_auth
from database import get_db
from schemas import OrderCreate, OrderOut, OrderUpdate
from services.order_service import (
	create_order,
	delete_order,
	get_order,
	get_orders,
	update_order,
)

router = APIRouter(tags=["orders"])


@router.post("/orders", status_code=201)
def create_order_endpoint(
	order: OrderCreate,
	db: Connection = Depends(get_db),
	current_user: str = Depends(require_basic_auth),
) -> OrderOut:
	return create_order(db, order, current_user)


@router.get("/orders")
def get_orders_endpoint(
	db: Connection = Depends(get_db),
	current_user: str = Depends(require_basic_auth),
) -> list[OrderOut]:
	return get_orders(db)


@router.get("/orders/{order_id}")
def get_order_endpoint(
	order_id: int,
	db: Connection = Depends(get_db),
	current_user: str = Depends(require_basic_auth),
) -> OrderOut:
	return get_order(db, order_id)


@router.put("/orders/{order_id}")
def update_order_endpoint(
	order_id: int,
	order: OrderUpdate,
	db: Connection = Depends(get_db),
	current_user: str = Depends(require_basic_auth),
) -> OrderOut:
	return update_order(db, order_id, order)


@router.delete("/orders/{order_id}", status_code=204)
def delete_order_endpoint(
	order_id: int,
	db: Connection = Depends(get_db),
	current_user: str = Depends(require_basic_auth),
):
	delete_order(db, order_id)