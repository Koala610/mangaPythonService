import aiohttp
import datetime

from src.config import REQUEST_WAITING_TIME
from src.entity import RMManga
from src.repository import user_repository
from src.service.rm_service import rm_service
from src.service.http_client.exceptions import NotAuthorized
from src import logger
from typing import Optional


async def get_bookmarks(user_id: int, dp, limit: int = 0, offset: int = 0, return_dict: bool = False) -> Optional[list]:
    storage_data = await dp.storage.get_data(user=user_id)
    timestamp = storage_data.get("timestamp")
    bookmarks = storage_data.get("bookmarks")
    if timestamp is None or bookmarks is None or datetime.datetime.now() - storage_data.get("timestamp") > datetime.timedelta(minutes=REQUEST_WAITING_TIME):
        try:
            bookmarks = await rm_service.get_bookmarks(user_id, limit, offset)
        except NotAuthorized:
            return None
        if bookmarks is None:
            return None
        h = RMManga.hash_from_list(bookmarks)
        user_repository.update(user_id, bookmarks_hash=h)
        await save_bookmarks_in_storage(user_id, bookmarks, dp)
        if return_dict:
            bookmarks = get_boomarks_dict(bookmarks)
        return bookmarks
    if return_dict:
        bookmarks = get_boomarks_dict(bookmarks)
    return bookmarks

async def save_bookmarks_in_storage(user_id, bookmarks, dp):
        storage_data = {
            "timestamp": datetime.datetime.now(),
            "bookmarks": bookmarks,
        }
        await dp.storage.set_data(user=user_id, data=storage_data)

def get_boomarks_dict(bookmarks):
    bookmarks_dict = {}
    for bookmark in bookmarks:
        letter = bookmark.title[0]
        if bookmarks_dict.get(letter) is None:
            bookmarks_dict[letter] = []
        bookmarks_dict[letter].append(bookmark)
    return bookmarks_dict