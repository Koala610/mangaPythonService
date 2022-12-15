import asyncio

from ...entity.parser_protocol import MangaParser
from ..client import HTTPClient


class RMService:
    def __init__(self, parser: MangaParser, client: HTTPClient):
        self.parser: MangaParser = parser
        self.client: HTTPClient = client
        self.user_repository = None
    
    def auth():
        pass


async def main():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()