from pydantic import BaseModel, Field

class Product(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	kind: str = Field(min_length=1, max_length=100)
	price: float = Field(gt=0)
	quantity: int = Field(gt=0)


class Customer(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	email: str = Field(min_length=1, max_length=100)
	phone: str = Field(min_length=1, max_length=10)
	address: str = Field(min_length=1, max_length=200)


class OrderCreate(BaseModel):
	products: list[Product] = Field(min_items=1)
	customer: Customer