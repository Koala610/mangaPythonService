import asyncio

import aiohttp
import src.logger as logger

from fake_useragent import UserAgent
from ...entity.protocol.parser_protocol import MangaParser
from ..http_client.client import HTTPClient


class RMService:
    BASE_URL = "https://readmanga.live"
    def __init__(self, parser: MangaParser, client: HTTPClient):
        self.parser: MangaParser = parser
        self.client: HTTPClient = client

    async def auth(self, user_id: int) -> dict:
        is_session_exists = self.client.check_if_user_information_exists(user_id=user_id)
        if not is_session_exists:
            await self.create_user_information(user_id=user_id)
        user_information = self.client.get_user_information(user_id)
        response = await self.client.get(self.BASE_URL+"/internal/auth", user_id=user_id, headers=user_information["headers"]) 
        return response

    async def create_user_information(self, user_id):
        user_agent = UserAgent()
        headers = {"User-Agent" : user_agent.firefox}
        user_information = {"cookie_jar" : None, "headers": headers}
        self.client.save_user_information(user_id=user_id, user_information=user_information)
        await self.client.get(self.BASE_URL, user_id, headers=headers)


async def main():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
