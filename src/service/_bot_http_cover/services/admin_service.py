from src.repository.mysql import admin_repository
from src.entity.user import Admin
from src.service._bot_http_cover.utils.jwt import verify_jwt
from ..models.notification_request import NotificationRequest
from fastapi import APIRouter, HTTPException


def get_admin(username: str, password: str, is_password_hashed: bool = False) -> Admin:
    return admin_repository.find_by_username_and_password(username, password, is_password_hashed=is_password_hashed)

def update_jwt(id: int, jwt: str) -> None:
    admin_repository.update(id, actual_jwt=jwt)

def check_if_user_admin(func):
    def wrapper(request: NotificationRequest):
        payload = verify_jwt(request.access_token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        admin = get_admin(payload.get("username"), payload.get("password"), True)
        if admin is None:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        if admin.actual_jwt != request.access_token:
            raise HTTPException(status_code=401, detail="Incorrect token")
        return func(request)
    return wrapper