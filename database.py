import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "ecommerce.db"))


def create_schema(conn):
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


def init_db():
	conn = sqlite3.connect(DB_PATH)
	try:
		create_schema(conn)
		cur = conn.cursor()
		cur.execute("SELECT COUNT(*) FROM products")
		if cur.fetchone()[0] == 0:
			cur.execute(
				"INSERT INTO products (name, kind, price, quantity) VALUES (?, ?, ?, ?)",
				("Wireless Mouse", "device", 24.99, 200),
			)
		conn.commit()
	finally:
		conn.close()


def get_db():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	try:
		yield conn
	finally:
		conn.close()
