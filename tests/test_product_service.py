import pytest
from fastapi import HTTPException

from schemas import ProductCreate, ProductUpdate
from services.product_service import (
	create_product,
	delete_product,
	get_product,
	list_products,
	update_product,
)


def test_create_and_get_product(db):
	created = create_product(
		db, ProductCreate(name="Pen", kind="office", price=2.5, quantity=10)
	)
	assert created["id"] > 0
	assert created["name"] == "Pen"
	assert created["price"] == 2.5

	fetched = get_product(db, created["id"])
	assert fetched == created


def test_list_products_empty(db):
	assert list_products(db) == []


def test_list_products_returns_all(db):
	create_product(db, ProductCreate(name="A", kind="x", price=1.0, quantity=1))
	create_product(db, ProductCreate(name="B", kind="x", price=2.0, quantity=2))
	result = list_products(db)
	assert [p["name"] for p in result] == ["A", "B"]


def test_get_product_not_found(db):
	with pytest.raises(HTTPException) as exc:
		get_product(db, 999)
	assert exc.value.status_code == 404


def test_update_product_partial(db):
	created = create_product(
		db, ProductCreate(name="Pen", kind="office", price=2.5, quantity=10)
	)
	updated = update_product(db, created["id"], ProductUpdate(price=3.0))
	assert updated["price"] == 3.0
	assert updated["name"] == "Pen"
	assert updated["quantity"] == 10


def test_update_product_not_found(db):
	with pytest.raises(HTTPException) as exc:
		update_product(db, 999, ProductUpdate(price=3.0))
	assert exc.value.status_code == 404


def test_delete_product(db):
	created = create_product(
		db, ProductCreate(name="Pen", kind="office", price=2.5, quantity=10)
	)
	delete_product(db, created["id"])
	with pytest.raises(HTTPException) as exc:
		get_product(db, created["id"])
	assert exc.value.status_code == 404


def test_delete_product_not_found(db):
	with pytest.raises(HTTPException) as exc:
		delete_product(db, 999)
	assert exc.value.status_code == 404
