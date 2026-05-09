from sqlite3 import Connection

from repositories.product_repository import list_products as list_products_repository


def list_products(db: Connection):
	return list_products_repository(db)

