from fastapi import HTTPException
from passlib.hash import bcrypt


def register_user(db, name, email, password):
	cur = db.cursor()
	cur.execute("SELECT id FROM users WHERE name = ?", (name,))
	if cur.fetchone() is not None:
		raise HTTPException(status_code=400, detail="Username already exists")
	cur.execute("SELECT id FROM users WHERE email = ?", (email,))
	if cur.fetchone() is not None:
		raise HTTPException(status_code=400, detail="Email already exists")
	hashed = bcrypt.hash(password)
	cur.execute(
		"INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
		(name, email, hashed),
	)
	db.commit()
	return cur.lastrowid


def authenticate_user(db, username, password):
	cur = db.cursor()
	cur.execute("SELECT password FROM users WHERE name = ?", (username,))
	row = cur.fetchone()
	if row is None:
		return False
	return bcrypt.verify(password, row["password"])
