import asyncio

from src.entity.protocol.parser_protocol import MangaParser
from src.entity.protocol.client_protocol import HTTPClient
from src.entity.protocol.manga_protocol import Manga
from src.logger import logger


class MangaService:
    BASE_URL = "https://readmanga.live"

    def __init__(self, parser: MangaParser, client: HTTPClient, Manga: Manga):
        self.parser: MangaParser = parser
        self.client: HTTPClient = client
        self.Manga = Manga
        logger.info("Manga service initalized...")

    async def auth(self, user_id: int, user_data: dict) -> dict:
        headers = {}

        auth_page_html = await self.client.get_auth_page_html(user_id, headers)
        params = self.parser.parse_auth_page(auth_page_html)

        response = await self.client.auth(user_id, headers, user_data, params) 
        if "Вход произведен" in response.get("text"):
            logger.info(
                f"Auth completed for user: {user_data.get('username')}")
        else:
            logger.warning(
                f"Auth failed for user: {user_data.get('username')}")
        return response

    async def get_bookmarks(self, user_id: int, limit: int = 0, offset: int = 0) -> list:
        bookmarks = await self.client.get_bookmarks_data(user_id, limit=limit, offset=offset)
        if bookmarks is None:
            return None
        bookmarks = [self.Manga.from_json(book) for book in bookmarks]
        logger.debug(bookmarks)
        return bookmarks

async def main():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
