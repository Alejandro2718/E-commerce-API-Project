import json
from sqlite3 import Connection

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from database import get_db, init_db, row_to_order, row_to_product
from schemas import OrderCreate, Product, Customer

app = FastAPI()


@app.on_event("startup")
def on_startup():
	init_db()




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

@app.put("/order/{order_id}")
def update_order(order_id: int, order: OrderCreate, db: Connection = Depends(get_db)):
	cur = db.cursor()
	cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
	row = cur.fetchone()
	if row is None:
		raise HTTPException(status_code=404, detail="Order not found")
	return row_to_order(row)

@app.delete("/order/{order_id}", status_code=204)
def delete_order(order_id: int, db: Connection = Depends(get_db)):
	cur = db.cursor()
	cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
	db.commit()
	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="Order not found")
	return {"message": "Order deleted successfully"}