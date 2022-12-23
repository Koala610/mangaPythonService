import unittest
import asyncio
import src.logger as logger

from src.entity.protocol.parser_protocol import MangaParser
from src.entity.manga import RMManga
from src.service.rm_service.main import MangaService
from src.entity.readmanga_parser import ReadmangaParser
from src.service.http_client.client import RMHTTPClient
from src.config import TEST_USERNAME, TEST_PASSWORD

class TestMangaService(unittest.TestCase):
    def setUp(self) -> None:
        parser: MangaParser = ReadmangaParser()
        client = RMHTTPClient()
        self.rm_service = MangaService(parser=parser, client=client, Manga=RMManga)

    def _auth(self):
        loop = asyncio.get_event_loop()
        user_data = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
        response =  loop.run_until_complete(asyncio.gather(self.rm_service.auth(1, user_data)))
        self.assertEqual(len(self.rm_service.client.user_informations), 1)
        self.assertTrue("Вход произведен" in response[0].get("text"))

    def test_obtaining_bookmarks(self):
        loop = asyncio.get_event_loop()
        user_data = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
        loop.run_until_complete(asyncio.gather(self.rm_service.auth(335271283, user_data)))
        response = loop.run_until_complete(asyncio.gather(self.rm_service.get_bookmarks(335271283)))
        self.assertTrue(response)

def main():
    unittest.main()
if __name__ == "__main__":
    main()