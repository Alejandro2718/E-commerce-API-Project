from sqlite3 import Connection

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials

from auth_dependencies import require_basic_auth, security
from database import get_db
from schemas import UserRegister
from services.auth_service import register_user

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=201)
def register_endpoint(user: UserRegister, db: Connection = Depends(get_db)):
	user_id = register_user(db, user.name, user.email, user.password)
	return {"id": user_id, "name": user.name, "email": user.email}


@router.get("/me")
def login_endpoint(
	credentials: HTTPBasicCredentials = Depends(security),
	db: Connection = Depends(get_db),
):
	username = require_basic_auth(credentials, db)
	return {"logged_in_as": username}
