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