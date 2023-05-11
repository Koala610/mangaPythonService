from typing import Optional
from fastapi import HTTPException
from fastapi import Body
from fastapi import APIRouter
from ..utils.jwt import generate_token, verify_jwt
from ..services.admin_service import get_admin, update_jwt
from ..models.credentials import Credentials
from src.logger import logger

router = APIRouter()

@router.post("/login")
def login(credentials: Credentials):
    user = get_admin(credentials.username, credentials.password)
    logger.debug(f"Got user: {user}")
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = generate_token(user)
    update_jwt(user.id, jwt=token) 
    return {"access_token": token}

@router.post("/refresh")
def refresh(authorization: Optional[str]):
    old_payload = verify_jwt(authorization)
    if old_payload is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = get_admin(old_payload.get("username"), old_payload.get("password"), True)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = generate_token(user)
    update_jwt(user.id, jwt=token) 
    return {"access_token": token}