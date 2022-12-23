import aiohttp

from src.repository import user_repository
from src.service.rm_service import rm_service
from src.service.http_client.exceptions import NotAuthorized
from src import logger
from typing import Optional


async def get_bookmarks(user_id: int, limit: int = 50, offset: int = 0) -> Optional[list]:
    try:
        bookmarks = await rm_service.get_bookmarks(user_id, limit, offset)
    except NotAuthorized:
        return None
    user_repository.update(user_id, bookmarks_hash=hash(tuple(bookmarks)))
    return bookmarks
