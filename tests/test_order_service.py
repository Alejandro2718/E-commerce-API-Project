import pytest
from fastapi import HTTPException

from schemas import Customer, OrderCreate, ProductCreate
from services.auth_service import register_user
from services.order_service import create_order, delete_order, get_order, update_order
from services.product_service import create_product


@pytest.fixture
def setup(db):
	register_user(db, "alice", "alice@example.com", "secret")
	create_product(db, ProductCreate(name="Pen", kind="office", price=2.0, quantity=10))
	return db


def _customer() -> Customer:
	return Customer(
		name="Bob",
		email="bob@example.com",
		phone="1234567890",
		address="1 Main St",
	)


def test_create_order_calculates_total(setup):
	order = create_order(
		setup,
		OrderCreate(product_id=1, quantity=3, customer=_customer()),
		"alice",
	)
	assert order["total_price"] == 6.0
	assert order["customer"]["name"] == "Bob"
	assert order["product"]["product_id"] == 1


def test_create_order_unknown_product(setup):
	with pytest.raises(HTTPException) as exc:
		create_order(
			setup,
			OrderCreate(product_id=999, quantity=1, customer=_customer()),
			"alice",
		)
	assert exc.value.status_code == 404


def test_create_order_insufficient_stock(setup):
	with pytest.raises(HTTPException) as exc:
		create_order(
			setup,
			OrderCreate(product_id=1, quantity=999, customer=_customer()),
			"alice",
		)
	assert exc.value.status_code == 400


def test_create_order_unknown_user(setup):
	with pytest.raises(HTTPException) as exc:
		create_order(
			setup,
			OrderCreate(product_id=1, quantity=1, customer=_customer()),
			"ghost",
		)
	assert exc.value.status_code == 401


def test_update_order(setup):
	order = create_order(
		setup,
		OrderCreate(product_id=1, quantity=1, customer=_customer()),
		"alice",
	)
	updated = update_order(
		setup,
		order["id"],
		OrderCreate(product_id=1, quantity=2, customer=_customer()),
	)
	assert updated["total_price"] == 4.0


def test_delete_order(setup):
	order = create_order(
		setup,
		OrderCreate(product_id=1, quantity=1, customer=_customer()),
		"alice",
	)
	delete_order(setup, order["id"])
	with pytest.raises(HTTPException) as exc:
		get_order(setup, order["id"])
	assert exc.value.status_code == 404


def test_delete_order_not_found(setup):
	with pytest.raises(HTTPException) as exc:
		delete_order(setup, 999)
	assert exc.value.status_code == 404
