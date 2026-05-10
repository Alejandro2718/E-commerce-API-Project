from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database import init_db
from routers import auth_router, orders_router, products_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
	init_db()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
	return JSONResponse(status_code=500, content={"error": "Something went wrong"})


app.include_router(products_router.router)
app.include_router(orders_router.router)
app.include_router(auth_router.router)
