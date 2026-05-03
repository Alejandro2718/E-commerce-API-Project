import json
import sqlite3
from collections.abc import Generator
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "ecommerce.db"


def init_db() -> None:
	conn = sqlite3.connect(DB_PATH)
	conn.execute(
		"""
		CREATE TABLE IF NOT EXISTS products (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			kind TEXT NOT NULL,
			price REAL NOT NULL,
			quantity INTEGER NOT NULL
		)
		"""
	)
	conn.execute(
		"""
		CREATE TABLE IF NOT EXISTS orders (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			total_price REAL NOT NULL,
			customer TEXT NOT NULL,
			products TEXT NOT NULL
		)
		"""
	)
	cur = conn.cursor()
	cur.execute("SELECT COUNT(*) FROM products")
	if cur.fetchone()[0] == 0:
		cur.executemany(
			"INSERT INTO products (name, kind, price, quantity) VALUES (?, ?, ?, ?)",
			[
				("Auriculares BT", "audio", 49.99, 120),
				("Teclado mecánico", "periférico", 89.5, 45),
				("Monitor 24\"", "pantalla", 199.0, 30),
				("Ratón inalámbrico", "periférico", 24.99, 200),
			],
		)
	conn.commit()
	conn.close()


def get_db() -> Generator[sqlite3.Connection, None, None]:
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	try:
		yield conn
	finally:
		conn.close()


def row_to_order(row: sqlite3.Row) -> dict:
	return {
		"id": row["id"],
		"total_price": row["total_price"],
		"customer": json.loads(row["customer"]),
		"products": json.loads(row["products"]),
	}


def row_to_product(row: sqlite3.Row) -> dict:
	return {
		"id": row["id"],
		"name": row["name"],
		"kind": row["kind"],
		"price": row["price"],
		"quantity": row["quantity"],
	}
