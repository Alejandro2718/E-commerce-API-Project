import pytest
from fastapi import HTTPException

from services.auth_service import authenticate_user, register_user


def test_register_and_authenticate(db):
	user_id = register_user(db, "alice", "alice@example.com", "secret")
	assert user_id > 0
	assert authenticate_user(db, "alice", "secret") is True


def test_authenticate_wrong_password(db):
	register_user(db, "alice", "alice@example.com", "secret")
	assert authenticate_user(db, "alice", "wrong") is False


def test_authenticate_unknown_user(db):
	assert authenticate_user(db, "ghost", "any") is False


def test_register_duplicate_username(db):
	register_user(db, "alice", "alice@example.com", "secret")
	with pytest.raises(HTTPException) as exc:
		register_user(db, "alice", "other@example.com", "secret")
	assert exc.value.status_code == 400


def test_register_duplicate_email(db):
	register_user(db, "alice", "alice@example.com", "secret")
	with pytest.raises(HTTPException) as exc:
		register_user(db, "bob", "alice@example.com", "secret")
	assert exc.value.status_code == 400
