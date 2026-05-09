from sqlite3 import Connection

from database import row_to_product


def list_products(db: Connection):
	cur = db.cursor()
	cur.execute("SELECT * FROM products ORDER BY id")
	return [row_to_product(r) for r in cur.fetchall()]
