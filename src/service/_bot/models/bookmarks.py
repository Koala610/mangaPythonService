import aiohttp

from src.repository import user_repository
from src.service.rm_service import rm_service
from src import logger
from typing import Optional

async def get_bookmarks(user_id: int, limit, offset) -> Optional[list]:
    try:
        bookmarks = await rm_service.get_bookmarks(user_id)
    except AttributeError:
        try:
            with open(f"./src/etc/{user_id}", "r") as f:
                cookie_jar = aiohttp.CookieJar()
                cookie_jar.load(f.name)
                rm_service.client.create_user_information(user_id, cookie_jar)
                bookmarks = await rm_service.get_bookmarks(user_id)
                logger.info(f"Cookies successfully loaded for user {user_id}")
                return bookmarks
        except FileNotFoundError:
            pass
            
        logger.warning(f"Can not get bookmarks for user {user_id}")
        return None
    user_repository.update(user_id, bookmarks_hash=hash(bookmarks))
    return bookmarks