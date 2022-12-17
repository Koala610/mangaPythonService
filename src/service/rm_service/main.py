import asyncio

import src.logger as logger

from fake_useragent import UserAgent
from ...entity.protocol.parser_protocol import MangaParser
from ..http_client.client import HTTPClient
from typing import Tuple

class MangaService:
    BASE_URL = "https://readmanga.live"
    AUTH_BASE_URL = "https://grouple.co"
    AUTH_BODY_TEMPLATE = "targetUri={target_uri}&username={username}&password={password}&remember_me=true&_remember_me_yes=&remember_me_yes=on"

    def __init__(self, parser: MangaParser, client: HTTPClient):
        self.parser: MangaParser = parser
        self.client: HTTPClient = client
        logger.logger.info("Manga service initalized...")

    async def verify_user_session(self, user_id: int) -> None:
        is_session_exists = self.client.check_if_user_session(
            user_id=user_id)
        if not is_session_exists:
            await self.create_user_information(user_id=user_id)

    async def get_basic_cookies(self, user_id: int) -> Tuple[dict, dict]:
        user_information = self.client.get_user_information(user_id)
        response = await self.client.get(
            self.BASE_URL+"/internal/auth",
            user_id=user_id, headers=user_information.get("headers")
        )
        return user_information.get("headers"), response

    async def auth(self, user_id: int, user_data: dict) -> dict:
        await self.verify_user_session(user_id)
        headers, response = await self.get_basic_cookies(user_id)

        parse_result = self.parser.parse_auth_page(response.get("text"))
        url = self.AUTH_BASE_URL+parse_result.get("url")
        headers["Referer"] = url
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.set_default_headers(headers)

        target_uri = parse_result.get("target_uri")
        data = self.AUTH_BODY_TEMPLATE.format(
            target_uri=target_uri,
            username=user_data.get("username"),
            password=user_data.get("password")
        )
        response = await self.client.post(
            url, user_id=user_id, headers=headers, data=data
        )
        if "Вход произведен" in response.get("text"):
            logger.logger.info(f"Auth completed for user: {user_data.get('username')}")
        else:
            logger.logger.warning(f"Auth failed for user: {user_data.get('username')}")
        return response

    async def create_user_information(self, user_id):
        user_agent = UserAgent()
        headers = {"User-Agent": user_agent.firefox}
        user_information = {"cookie_jar": None, "headers": headers}
        self.client.save_user_information(
            user_id=user_id, user_information=user_information)
        await self.client.get(self.BASE_URL, user_id, headers=headers)

    def set_default_headers(self, headers: dict):
        headers["DNT"] = "1"


async def main():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
