from fastapi import APIRouter, Depends

from auth_dependencies import require_basic_auth
from database import get_db
from schemas import UserRegister
from services.auth_service import register_user

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=201)
def register_endpoint(user: UserRegister, db=Depends(get_db)):
	user_id = register_user(db, user.name, user.email, user.password)
	return {"id": user_id, "name": user.name, "email": user.email}


@router.get("/me")
def me_endpoint(current_user: str = Depends(require_basic_auth)):
	return {"logged_in_as": current_user}
