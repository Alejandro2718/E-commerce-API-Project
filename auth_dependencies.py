from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from database import get_db
from services.auth_service import authenticate_user

security = HTTPBasic()


def require_basic_auth(credentials: HTTPBasicCredentials = Depends(security), db=Depends(get_db)):
	if not authenticate_user(db, credentials.username, credentials.password):
		raise HTTPException(status_code=401, detail="Bad login or password")
	return credentials.username
