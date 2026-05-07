import json
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
				total_price REAL NOT NULL,
				customer TEXT NOT NULL,
				products TEXT NOT NULL,
				FOREIGN KEY (user_id) REFERENCES users (id)
			)
			"""
		)
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS order_items (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				order_id INTEGER NOT NULL,
				product_id INTEGER NOT NULL,
				quantity INTEGER NOT NULL,
				FOREIGN KEY (order_id) REFERENCES orders (id),
				FOREIGN KEY (product_id) REFERENCES products (id)
			)
			"""
		)
		cur = conn.cursor()
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
