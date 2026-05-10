# Cloud-based E-commerce REST API

A small FastAPI service that exposes a product catalogue and an orders system on top of SQLite. Users register, log in with HTTP Basic, and only authenticated users can place or manage orders.

## Stack

- Python 3.11+
- FastAPI + Uvicorn
- SQLite (standard library `sqlite3`)
- Pydantic v2 for input validation
- pytest for unit tests

## Project structure

```
.
├── main.py                 # FastAPI app, router wiring, global error handler
├── database.py             # SQLite connection and schema bootstrap
├── schemas.py              # Pydantic request/response models
├── auth_dependencies.py    # HTTP Basic auth dependency
├── routers/                # HTTP layer (controllers)
│   ├── auth_router.py
│   ├── products_router.py
│   └── orders_router.py
├── services/               # Business logic
│   ├── auth_service.py
│   ├── product_service.py
│   └── order_service.py
└── tests/                  # Unit tests for the service layer
```

## Setup

1. Clone the repo and create a virtual environment.

   ```bash
   python -m venv .venv
   .venv\Scripts\activate     # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Optional: copy the environment template (defaults work out of the box).

   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env      # macOS/Linux
   ```

4. Run the API.

   ```bash
   uvicorn main:app --reload
   ```

The interactive Swagger UI is available at <http://127.0.0.1:8000/docs>.

## Tests

```bash
pytest
```

## Endpoints

| Method | Path             | Auth  | Description                     |
| ------ | ---------------- | ----- | ------------------------------- |
| POST   | `/register`      | none  | Register a new user             |
| GET    | `/me`            | basic | Show current authenticated user |
| GET    | `/products`      | none  | List all products               |
| GET    | `/products/{id}` | none  | Get a product by id             |
| POST   | `/products`      | none  | Create a product                |
| PUT    | `/products/{id}` | none  | Update a product                |
| DELETE | `/products/{id}` | none  | Delete a product                |
| GET    | `/orders`        | basic | List orders                     |
| GET    | `/orders/{id}`   | basic | Get an order by id              |
| POST   | `/orders`        | basic | Place a new order               |
| PUT    | `/orders/{id}`   | basic | Update an order                 |
| DELETE | `/orders/{id}`   | basic | Delete an order                 |

## Example requests

### Register a user

```http
POST /register
Content-Type: application/json

{
  "name": "alice",
  "email": "alice@example.com",
  "password": "secret"
}
```

### Create a product

```http
POST /products
Content-Type: application/json

{
  "name": "Wireless Mouse",
  "kind": "device",
  "price": 24.99,
  "quantity": 200
}
```

### Place an order (authenticated)

```http
POST /orders
Authorization: Basic <base64(alice:secret)>
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2,
  "customer": {
    "name": "Alice",
    "email": "alice@example.com",
    "phone": "1234567890",
    "address": "1 Main St"
  }
}
```

## Error handling

| Status | Cause                                            |
| ------ | ------------------------------------------------ |
| 400    | Business rule violation (e.g. not enough stock)  |
| 401    | Missing or invalid HTTP Basic credentials        |
| 404    | Resource not found                               |
| 422    | Request body fails Pydantic validation           |
| 500    | Caught by the global handler in `main.py`        |
