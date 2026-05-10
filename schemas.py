from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	kind: str = Field(min_length=1, max_length=100)
	price: float = Field(gt=0)
	quantity: int = Field(gt=0)


class ProductUpdate(BaseModel):
	name: str | None = Field(default=None, min_length=1, max_length=100)
	kind: str | None = Field(default=None, min_length=1, max_length=100)
	price: float | None = Field(default=None, gt=0)
	quantity: int | None = Field(default=None, gt=0)


class Customer(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	email: str = Field(min_length=1, max_length=100)
	phone: str = Field(min_length=1, max_length=10)
	address: str = Field(min_length=1, max_length=200)


class OrderCreate(BaseModel):
	product_id: int = Field(gt=0)
	quantity: int = Field(gt=0)
	customer: Customer


class UserRegister(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	email: str = Field(min_length=1, max_length=100)
	password: str = Field(min_length=1, max_length=100)
