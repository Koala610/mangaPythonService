from fastapi import APIRouter, Header
from typing import Annotated, Optional
from ..services.admin_service import check_if_user_admin, get_admin_by_jwt, update_user_id
from ..services. user_service import get_users_in_range, check_whether_user_is_support, get_user_by_id
from ..models.admin import AdminInfo
from src.entity.user import Admin
from src.logger import logger

router = APIRouter()

@router.get("/echo")
@check_if_user_admin
async def echo(authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    return {"status": "ok"}

@router.post("/admin/user_id")
@check_if_user_admin
async def update_admin_user_id(adminInfo: AdminInfo, authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    update_user_id(adminInfo.id, adminInfo.user_id)
    return {"status": "ok"}

@router.get("/user")
@check_if_user_admin
async def get_all_users(offset: Optional[int], limit: Optional[int], authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    if offset is not None and limit is not None:
        return get_users_in_range(offset=offset, limit=limit)
    return get_all_users()

@router.get("/user/{user_id}")
@check_if_user_admin
async def get_user_by_its_id(user_id: int, authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    return get_user_by_id(user_id)

@router.get("/user/{user_id}/is_support")
@check_if_user_admin
async def check_if_user_is_support(user_id: str, authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    return check_whether_user_is_support(user_id)

@router.get("/admin")
@check_if_user_admin
async def get_admin_from_jwt(authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    try:
        admin: Admin = get_admin_by_jwt(authorization.split(" ")[1])

        return {
            "user_id" : admin.user_id if admin is not None else None,
            "username": admin.username,
            "id": admin.id
        }
    except Exception as e:
        logger.error(e)
        return {
            "user_id" : None,
            "username": None,
            "id": None
        }