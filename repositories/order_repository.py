import json
from sqlite3 import Connection

from fastapi import HTTPException

from database import row_to_order
from schemas import OrderCreate, OrderOut, OrderUpdate


def list_orders(db: Connection) -> list[OrderOut]:
	cur = db.cursor()
	cur.execute("SELECT * FROM orders ORDER BY id")
	return [row_to_order(r) for r in cur.fetchall()]

def get_order_by_id(db: Connection, order_id: int) -> OrderOut:
	cur = db.cursor()
	cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
	row = cur.fetchone()
	if row is None:
		raise HTTPException(status_code=404, detail="Order not found")
	return row_to_order(row)

def insert_order(db: Connection, order: OrderCreate, total_price: float, user_id: int = 1):
	cur = db.cursor()
	cur.execute(
		"INSERT INTO orders (user_id, total_price, customer, products) VALUES (?, ?, ?, ?)",
		(
			user_id,
			total_price,
			json.dumps(order.customer.model_dump()),
			json.dumps([p.model_dump() for p in order.products]),
		),
	)
	db.commit()
	return cur.lastrowid

def delete_order(db: Connection, order_id: int):
	cur = db.cursor()
	cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
	db.commit()
	return cur.rowcount


def update_order(db: Connection, order_id: int, order: OrderUpdate, total_price: float):
	cur = db.cursor()
	cur.execute(
		"UPDATE orders SET total_price = ?, customer = ?, products = ? WHERE id = ?",
		(
			total_price,
			json.dumps(order.customer.model_dump()),
			json.dumps([p.model_dump() for p in order.products]),
			order_id,
		),
	)
	db.commit()
	return cur.rowcount
