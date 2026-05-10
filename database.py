import sqlite3
from collections.abc import Generator
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "ecommerce.db"


def init_db() -> None:
	conn = sqlite3.connect(DB_PATH)
	try:
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				email TEXT NOT NULL,
				password TEXT NOT NULL
			)
			"""
		)
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
				user_id INTEGER NOT NULL,
				product_id INTEGER NOT NULL,
				quantity INTEGER NOT NULL,
				total_price REAL NOT NULL,
				customer_name TEXT NOT NULL,
				customer_email TEXT NOT NULL,
				customer_phone TEXT NOT NULL,
				customer_address TEXT NOT NULL,
				FOREIGN KEY (user_id) REFERENCES users (id),
				FOREIGN KEY (product_id) REFERENCES products (id)
			)
			"""
		)
		cur = conn.cursor()
		cur.execute("PRAGMA table_info(orders)")
		order_columns = [row[1] for row in cur.fetchall()]
		if "product_id" not in order_columns:
			conn.execute("DROP TABLE IF EXISTS orders")
			conn.execute(
				"""
				CREATE TABLE orders (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					user_id INTEGER NOT NULL,
					product_id INTEGER NOT NULL,
					quantity INTEGER NOT NULL,
					total_price REAL NOT NULL,
					customer_name TEXT NOT NULL,
					customer_email TEXT NOT NULL,
					customer_phone TEXT NOT NULL,
					customer_address TEXT NOT NULL,
					FOREIGN KEY (user_id) REFERENCES users (id),
					FOREIGN KEY (product_id) REFERENCES products (id)
				)
				"""
			)
		conn.execute("DROP TABLE IF EXISTS order_items")
		cur.execute("SELECT COUNT(*) FROM products")
		if cur.fetchone()[0] == 0:
			cur.executemany(
				"INSERT INTO products (name, kind, price, quantity) VALUES (?, ?, ?, ?)",
				[
					("Wireless Mouse", "device", 24.99, 200),
				],
			)
		conn.commit()
	finally:
		conn.close()


def get_db() -> Generator[sqlite3.Connection, None, None]:
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	try:
		yield conn
	finally:
		conn.close()


def row_to_product(row: sqlite3.Row) -> dict:
	return {
		"id": row["id"],
		"name": row["name"],
		"kind": row["kind"],
		"price": row["price"],
		"quantity": row["quantity"],
	}
