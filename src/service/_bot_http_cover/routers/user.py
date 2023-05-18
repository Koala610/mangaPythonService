from fastapi import APIRouter, Header
from typing import Annotated, Optional
from ..services.admin_service import check_if_user_admin
from ..services. user_service import get_users, get_users_in_range

router = APIRouter()

@router.get("/user")
@check_if_user_admin
async def get_all_users(offset: Optional[int], limit: Optional[int], authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    if offset is not None and limit is not None:
        return get_users_in_range(offset=offset, limit=limit)
    return get_all_users()
