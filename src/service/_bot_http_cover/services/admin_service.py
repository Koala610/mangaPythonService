from src.repository.mysql import admin_repository
from src.entity.user import Admin
from src.service._bot_http_cover.utils.jwt import verify_jwt
from fastapi import HTTPException
from functools import wraps

def get_admin(username: str, password: str, is_password_hashed: bool = False) -> Admin:
    return admin_repository.find_by_username_and_password(username, password, is_password_hashed=is_password_hashed)

def update_jwt(id: int, jwt: str, refresh_token: str) -> None:
    admin_repository.update(id, actual_jwt=jwt, refresh_token=refresh_token)

def check_if_user_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get("authorization").split(" ")[1]
        payload = verify_jwt(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Incorrect token")
        admin = get_admin(payload.get("username"), payload.get("password"), True)
        if admin is None:
            raise HTTPException(status_code=401, detail="No such user")
        if admin.actual_jwt != token:
            raise HTTPException(status_code=401, detail="Incorrect token")
        return await func(*args, **kwargs)
    return wrapper