import asyncio

from ...entity.parser_protocol import MangaParser
from ..client import HTTPClient
from ...repository import UserRepository


class RMService:
    def __init__(self, parser: MangaParser, client: HTTPClient):
        self.parser: MangaParser = parser
        self.client: HTTPClient = client
        self.user_repository = UserRepository

    def auth(self):
        response = self.client.get("https://grouple.co/internal/auth/login", return_text=True) 
        auth_parse_result = self.parser.parse_auth_page(response)


async def main():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
