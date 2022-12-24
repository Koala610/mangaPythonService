import aiohttp
import datetime

from src.config import REQUEST_WAITING_TIME
from src.repository import user_repository
from src.service.rm_service import rm_service
from src.service.http_client.exceptions import NotAuthorized
from src import logger
from typing import Optional


async def get_bookmarks(user_id: int, storage_data, limit: int = 50, offset: int = 0) -> Optional[list]:

    timestamp = storage_data.get("timestamp")
    bookmarks = storage_data.get("bookmarks")
    if timestamp is None or bookmarks is None or datetime.datetime.now() - storage_data.get("timestamp") > datetime.timedelta(minutes=REQUEST_WAITING_TIME):
        try:
            bookmarks = await rm_service.get_bookmarks(user_id, limit, offset)
        except NotAuthorized:
            return None, None
        if bookmarks is None:
            return None, None
        user_repository.update(user_id, bookmarks_hash=hash(tuple(bookmarks)))
        return bookmarks, True
    return bookmarks, False
