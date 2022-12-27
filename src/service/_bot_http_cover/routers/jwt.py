from typing import Optional
from fastapi import HTTPException
from fastapi import Body
from fastapi import APIRouter
from ..utils.jwt import generate_token, verify_jwt, get_admin
from src.logger import logger

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    user = get_admin(username, password)
    logger.info(user)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": generate_token(user)}

@router.post("/refresh")
def refresh(authorization: Optional[str]):
    old_payload = verify_jwt(authorization)
    logger.info(old_payload)
    if old_payload is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = get_admin(old_payload.get("username"), old_payload.get("password"), True)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"access_token": generate_token(user)}