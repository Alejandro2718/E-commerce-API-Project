import json
from sqlite3 import Connection

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from database import get_db, init_db, row_to_order, row_to_product

app = FastAPI()


@app.on_event("startup")
def on_startup():
	init_db()


class Product(BaseModel):
	name: str
	kind: str
	price: float
	quantity: int


class Customer(BaseModel):
	name: str
	email: str
	phone: str
	address: str


class OrderCreate(BaseModel):
	products: list[Product]
	customer: Customer


@app.get("/products")
def list_products(db: Connection = Depends(get_db)):
	cur = db.cursor()
	cur.execute("SELECT * FROM products ORDER BY id")
	return [row_to_product(r) for r in cur.fetchall()]


@app.post("/create-order", status_code=201)
def create_order(order: OrderCreate, db: Connection = Depends(get_db)):
	total_price = sum(p.price * p.quantity for p in order.products)
	cur = db.cursor()
	cur.execute(
		"""
		INSERT INTO orders (total_price, customer, products)
		VALUES (?, ?, ?)
		""",
		(
			total_price,
			json.dumps(order.customer.model_dump()),
			json.dumps([p.model_dump() for p in order.products]),
		),
	)
	db.commit()
	new_id = cur.lastrowid
	cur.execute("SELECT * FROM orders WHERE id = ?", (new_id,))
	row = cur.fetchone()
	if row is None:
		raise HTTPException(
			status_code=500,
			detail="Order was created but could not be read back",
		)

	return {
		"message": "Order created successfully!",
		"total_price": round(total_price, 2),
		"details": row_to_order(row),
	}


@app.get("/orders")
def get_orders(db: Connection = Depends(get_db)):
	cur = db.cursor()
	cur.execute("SELECT * FROM orders ORDER BY id")
	return [row_to_order(r) for r in cur.fetchall()]


@app.get("/order/{order_id}")
def get_order(order_id: int, db: Connection = Depends(get_db)):
	cur = db.cursor()
	cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
	row = cur.fetchone()
	if row is None:
		raise HTTPException(status_code=404, detail="Order not found")
	return row_to_order(row)
