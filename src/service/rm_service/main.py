import asyncio
import src.logger as logger

from ...entity.protocol.parser_protocol import MangaParser
from ..http_client.client import HTTPClient


class RMService:
    BASE_URL = "https://readmanga.live"
    def __init__(self, parser: MangaParser, client: HTTPClient):
        self.parser: MangaParser = parser
        self.client: HTTPClient = client

    async def auth(self, user_id: int):
        is_session_exists = self.client.check_if_user_session_exists(user_id=user_id)
        if not is_session_exists:
            headers = {} #TODO: add user agent header
            self.client.create_session(user_id, headers) 
            logger.logger.debug(f"{len(self.client.sessions)} session")
            await self.client.get(self.BASE_URL, user_id)
        response = await self.client.get(self.BASE_URL+"/internal/auth/login", user_id=user_id) 
        return response
        # auth_parse_result = self.parser.parse_auth_page(response.get("text"))


async def main():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
