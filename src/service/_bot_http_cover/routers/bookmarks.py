from fastapi import APIRouter, Header
from src.entity.manga import RMManga
from src.service._bot_http_cover.services.admin_service import check_if_user_admin
from src.service.rm_service import rm_service
from typing import Annotated
from ..models.request import Request

router = APIRouter()

@router.get("/{user_id}/bookmarks/hash")
@check_if_user_admin
async def get_bookmarks_hash(user_id: int, authorization: Annotated[str | None, Header()] = Header(title="Authorization")):
    bookmarks: list = await rm_service.get_bookmarks(user_id=user_id)
    return RMManga.hash_from_list(bookmarks)
