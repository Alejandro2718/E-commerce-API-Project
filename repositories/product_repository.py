@app.get("/products")
def list_products(db: Connection = Depends(get_db)):
	cur = db.cursor()
	cur.execute("SELECT * FROM products ORDER BY id")
	return [row_to_product(r) for r in cur.fetchall()]
