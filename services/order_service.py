from sqlite3 import Connection

from fastapi import HTTPException

from schemas import OrderCreate, OrderOut, OrderUpdate


def _get_user_by_name(db: Connection, name: str):
	cur = db.cursor()
	cur.execute("SELECT id, name, email, password FROM users WHERE name = ?", (name,))
	return cur.fetchone()


def _get_product_for_order(db: Connection, product_id: int):
	cur = db.cursor()
	cur.execute(
		"SELECT id, name, kind, price, quantity FROM products WHERE id = ?",
		(product_id,),
	)
	return cur.fetchone()


def _build_order_response(db: Connection, row) -> OrderOut:
	cur = db.cursor()
	cur.execute(
		"""
		SELECT p.id AS product_id, p.name, p.kind, p.price, o.quantity
		FROM orders o
		JOIN products p ON p.id = o.product_id
		WHERE o.id = ?
		""",
		(row["id"],),
	)
	product_row = cur.fetchone()
	if product_row is None:
		raise HTTPException(status_code=404, detail="Product not found")
	return {
		"id": row["id"],
		"total_price": row["total_price"],
		"customer": {
			"name": row["customer_name"],
			"email": row["customer_email"],
			"phone": row["customer_phone"],
			"address": row["customer_address"],
		},
		"product": {
			"product_id": product_row["product_id"],
			"name": product_row["name"],
			"kind": product_row["kind"],
			"price": product_row["price"],
			"quantity": product_row["quantity"],
		},
	}


def _get_order_by_id(db: Connection, order_id: int) -> OrderOut:
	cur = db.cursor()
	cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
	row = cur.fetchone()
	if row is None:
		raise HTTPException(status_code=404, detail="Order not found")
	return _build_order_response(db, row)


def _calculate_total_and_validate_stock(db: Connection, order: OrderCreate | OrderUpdate) -> float:
	product = _get_product_for_order(db, order.product_id)
	if product is None:
		raise HTTPException(status_code=404, detail=f"Product {order.product_id} not found")
	if order.quantity > product["quantity"]:
		raise HTTPException(
			status_code=400,
			detail=f"Not enough stock for product {order.product_id}",
		)
	return product["price"] * order.quantity


def create_order(db: Connection, order: OrderCreate, username: str) -> OrderOut:
	user = _get_user_by_name(db, username)
	if user is None:
		raise HTTPException(status_code=401, detail="Bad login or password")
	total_price = _calculate_total_and_validate_stock(db, order)
	cur = db.cursor()
	cur.execute(
		"""
		INSERT INTO orders (
			user_id, product_id, quantity, total_price,
			customer_name, customer_email, customer_phone, customer_address
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		""",
		(
			user["id"],
			order.product_id,
			order.quantity,
			total_price,
			order.customer.name,
			order.customer.email,
			order.customer.phone,
			order.customer.address,
		),
	)
	db.commit()
	return _get_order_by_id(db, cur.lastrowid)


def get_orders(db: Connection) -> list[OrderOut]:
	cur = db.cursor()
	cur.execute("SELECT * FROM orders ORDER BY id")
	return [_build_order_response(db, r) for r in cur.fetchall()]


def get_order(db: Connection, order_id: int) -> OrderOut:
	return _get_order_by_id(db, order_id)


def update_order(db: Connection, order_id: int, order: OrderUpdate) -> OrderOut:
	_get_order_by_id(db, order_id)
	total_price = _calculate_total_and_validate_stock(db, order)
	cur = db.cursor()
	cur.execute(
		"""
		UPDATE orders
		SET product_id = ?, quantity = ?, total_price = ?, customer_name = ?, customer_email = ?, customer_phone = ?, customer_address = ?
		WHERE id = ?
		""",
		(
			order.product_id,
			order.quantity,
			total_price,
			order.customer.name,
			order.customer.email,
			order.customer.phone,
			order.customer.address,
			order_id,
		),
	)
	db.commit()
	updated = cur.rowcount
	if not updated:
		raise HTTPException(status_code=404, detail="Order not found")
	return _get_order_by_id(db, order_id)


def delete_order(db: Connection, order_id: int):
	cur = db.cursor()
	cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
	db.commit()
	deleted_rows = cur.rowcount
	if deleted_rows == 0:
		raise HTTPException(status_code=404, detail="Order not found")