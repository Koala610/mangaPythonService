from fastapi import HTTPException
from fastapi import APIRouter
from ..utils.jwt import generate_token, verify_jwt, generate_refresh_token
from ..services.admin_service import get_admin, update_jwt
from ..models.credentials import Credentials
from ..models.refresh_token import TokenRequest
from src.core_logger import logger

router = APIRouter()

@router.post("/login")
def login(credentials: Credentials):
    user = get_admin(credentials.username, credentials.password)
    logger.debug(f"Got user: {user}")
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = generate_token(user)
    refresh_token = generate_refresh_token(user)
    update_jwt(user.id, jwt=token, refresh_token=refresh_token) 
    return {"access_token": token, "refresh_token": refresh_token}

@router.post("/refresh")
def refresh(refresh_token: TokenRequest):
    old_payload = verify_jwt(refresh_token.refresh_token)
    if old_payload is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = get_admin(old_payload.get("username"), old_payload.get("password"), True)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if user.refresh_token != refresh_token.refresh_token:
        raise HTTPException(status_code=401, detail="Wrong refresh token")
    
    token = generate_token(user)
    refresh_token = generate_refresh_token(user)
    update_jwt(user.id, jwt=token, refresh_token=refresh_token) 
    return {"access_token": token, "refresh_token": refresh_token}

@router.post("/verify-jwt")
def jwt_verification(access_token: TokenRequest):
    payload = verify_jwt(access_token.access_token)
    return {"result": False if payload is None else True}