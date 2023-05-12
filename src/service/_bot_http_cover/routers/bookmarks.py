from fastapi import APIRouter
from ..models.request import Request
from src.entity.manga import RMManga
from src.service._bot_http_cover.services.admin_service import check_if_user_admin
from src.service.rm_service import rm_service

router = APIRouter()

@router.post("/bookmarks/hash")
@check_if_user_admin
async def get_bookmarks_hash(request: Request):
    bookmarks: list = await rm_service.get_bookmarks(request.data.get("user_id"))
    return RMManga.hash_from_list(bookmarks)
