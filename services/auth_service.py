from sqlite3 import Connection

from fastapi import HTTPException

def _get_user_by_name(db: Connection, name: str):
	cur = db.cursor()
	cur.execute("SELECT id, name, email, password FROM users WHERE name = ?", (name,))
	return cur.fetchone()


def _get_user_by_email(db: Connection, email: str):
	cur = db.cursor()
	cur.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
	return cur.fetchone()


def register_user(db: Connection, name: str, email: str, password: str) -> int:
	if _get_user_by_name(db, name) is not None:
		raise HTTPException(status_code=400, detail="Username already exists")
	if _get_user_by_email(db, email) is not None:
		raise HTTPException(status_code=400, detail="Email already exists")
	cur = db.cursor()
	cur.execute(
		"INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
		(name, email, password),
	)
	db.commit()
	return cur.lastrowid


def authenticate_user(db: Connection, username: str, password: str) -> bool:
	user = _get_user_by_name(db, username)
	if user is None:
		return False
	return user["password"] == password
