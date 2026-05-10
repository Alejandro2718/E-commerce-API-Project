from fastapi import HTTPException

from schemas import OrderCreate


def _get_order(db, order_id):
	cur = db.cursor()
	cur.execute(
		"""
		SELECT o.id, o.total_price, o.quantity,
			o.customer_name, o.customer_email, o.customer_phone, o.customer_address,
			p.id AS product_id, p.name, p.kind, p.price
		FROM orders o
		JOIN products p ON p.id = o.product_id
		WHERE o.id = ?
		""",
		(order_id,),
	)
	row = cur.fetchone()
	if row is None:
		raise HTTPException(status_code=404, detail="Order not found")
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
			"product_id": row["product_id"],
			"name": row["name"],
			"kind": row["kind"],
			"price": row["price"],
			"quantity": row["quantity"],
		},
	}


def _check_product_and_total(db, product_id, quantity):
	cur = db.cursor()
	cur.execute("SELECT price, quantity FROM products WHERE id = ?", (product_id,))
	product = cur.fetchone()
	if product is None:
		raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
	if quantity > product["quantity"]:
		raise HTTPException(status_code=400, detail=f"Not enough stock for product {product_id}")
	return product["price"] * quantity


def create_order(db, order: OrderCreate, username):
	cur = db.cursor()
	cur.execute("SELECT id FROM users WHERE name = ?", (username,))
	user = cur.fetchone()
	if user is None:
		raise HTTPException(status_code=401, detail="Bad login or password")
	total = _check_product_and_total(db, order.product_id, order.quantity)
	cur.execute(
		"""
		INSERT INTO orders (
			user_id, product_id, quantity, total_price,
			customer_name, customer_email, customer_phone, customer_address
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		""",
		(
			user["id"], order.product_id, order.quantity, total,
			order.customer.name, order.customer.email,
			order.customer.phone, order.customer.address,
		),
	)
	db.commit()
	return _get_order(db, cur.lastrowid)


def get_orders(db):
	cur = db.cursor()
	cur.execute("SELECT id FROM orders ORDER BY id")
	return [_get_order(db, r["id"]) for r in cur.fetchall()]


def get_order(db, order_id):
	return _get_order(db, order_id)


def update_order(db, order_id, order: OrderCreate):
	_get_order(db, order_id)
	total = _check_product_and_total(db, order.product_id, order.quantity)
	cur = db.cursor()
	cur.execute(
		"""
		UPDATE orders
		SET product_id = ?, quantity = ?, total_price = ?,
			customer_name = ?, customer_email = ?, customer_phone = ?, customer_address = ?
		WHERE id = ?
		""",
		(
			order.product_id, order.quantity, total,
			order.customer.name, order.customer.email,
			order.customer.phone, order.customer.address, order_id,
		),
	)
	db.commit()
	return _get_order(db, order_id)


def delete_order(db, order_id):
	cur = db.cursor()
	cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
	db.commit()
	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="Order not found")
