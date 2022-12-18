import asyncio

import src.logger as logger

from ...entity.protocol.parser_protocol import MangaParser
from src.entity.protocol.client import HTTPClient


class MangaService:
    BASE_URL = "https://readmanga.live"
    AUTH_BASE_URL = "https://grouple.co"
    AUTH_PATH = "/internal/auth"
    AUTH_CONTENT_TYPE = "application/x-www-form-urlencoded"

    def __init__(self, parser: MangaParser, client: HTTPClient):
        self.parser: MangaParser = parser
        self.client: HTTPClient = client
        logger.logger.info("Manga service initalized...")

    async def auth(self, user_id: int, user_data: dict) -> dict:
        self.client.verify_user_session(user_id)

        user_information = self.client.get_user_information(user_id)
        headers = user_information.get("headers")
        auth_page_html = await self.client.get_auth_page_html(user_id, headers)

        parse_result = self.parser.parse_auth_page(auth_page_html)
        url = self.AUTH_BASE_URL+parse_result.get("url")
        self.set_auth_headers(headers)

        data = self.client.get_auth_request_body(
            user_data=user_data, parse_result=parse_result
        )
        response = await self.client.post(
            url, user_id=user_id, headers=headers, data=data
        )
        if "Вход произведен" in response.get("text"):
            logger.logger.info(
                f"Auth completed for user: {user_data.get('username')}")
        else:
            logger.logger.warning(
                f"Auth failed for user: {user_data.get('username')}")
        return response


    def set_auth_headers(self, headers: dict):
        headers["DNT"] = "1"
        headers["Content-Type"] = self.AUTH_CONTENT_TYPE


async def main():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
