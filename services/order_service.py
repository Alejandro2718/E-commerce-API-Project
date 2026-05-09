from sqlite3 import Connection

from fastapi import HTTPException

from repositories.order_repository import (
	delete_order as delete_order_repository,
	update_order as update_order_repository,
	get_order_by_id,
	insert_order,
	list_orders,
)
from schemas import OrderCreate, OrderOut, OrderUpdate


def create_order(db: Connection, order: OrderCreate) -> int:
	total_price = sum(p.price * p.quantity for p in order.products)
	return insert_order(db, order, total_price)


def get_orders(db: Connection) -> list[OrderOut]:
	return list_orders(db)


def get_order(db: Connection, order_id: int) -> OrderOut:
	return get_order_by_id(db, order_id)


def update_order(db: Connection, order_id: int, order: OrderUpdate) -> OrderOut:
	existing_order = get_order_by_id(db, order_id)
	if not existing_order:
		raise HTTPException(status_code=404, detail="Order not found")

	total_price = sum(p.price * p.quantity for p in order.products)

	updated = update_order_repository(db, order_id, order, total_price)
	if not updated:
		raise HTTPException(status_code=404, detail="Order not found")
	return get_order_by_id(db, order_id)


def delete_order(db: Connection, order_id: int):
	deleted_rows = delete_order_repository(db, order_id)
	if deleted_rows == 0:
		raise HTTPException(status_code=404, detail="Order not found")
	return {"message": "Order deleted successfully"}