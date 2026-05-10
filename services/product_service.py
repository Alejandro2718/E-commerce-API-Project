from fastapi import HTTPException

from schemas import ProductCreate, ProductUpdate


def list_products(db):
	cur = db.cursor()
	cur.execute("SELECT * FROM products ORDER BY id")
	return [dict(r) for r in cur.fetchall()]


def get_product(db, product_id):
	cur = db.cursor()
	cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
	row = cur.fetchone()
	if row is None:
		raise HTTPException(status_code=404, detail="Product not found")
	return dict(row)


def create_product(db, product: ProductCreate):
	cur = db.cursor()
	cur.execute(
		"INSERT INTO products (name, kind, price, quantity) VALUES (?, ?, ?, ?)",
		(product.name, product.kind, product.price, product.quantity),
	)
	db.commit()
	return get_product(db, cur.lastrowid)


def update_product(db, product_id, product: ProductUpdate):
	existing = get_product(db, product_id)
	name = product.name if product.name is not None else existing["name"]
	kind = product.kind if product.kind is not None else existing["kind"]
	price = product.price if product.price is not None else existing["price"]
	quantity = product.quantity if product.quantity is not None else existing["quantity"]

	cur = db.cursor()
	cur.execute(
		"UPDATE products SET name = ?, kind = ?, price = ?, quantity = ? WHERE id = ?",
		(name, kind, price, quantity, product_id),
	)
	db.commit()
	return get_product(db, product_id)


def delete_product(db, product_id):
	cur = db.cursor()
	cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
	db.commit()
	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="Product not found")
