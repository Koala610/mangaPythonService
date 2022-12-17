import unittest
import asyncio
from src.service.rm_service.main import MangaService
from src.entity.readmanga_parser import ReadmangaParser
from src.service.http_client.client import HTTPClient
from config import TEST_USERNAME, TEST_PASSWORD

class TestMangaService(unittest.TestCase):
    def setUp(self) -> None:
        parser = ReadmangaParser()
        client = HTTPClient()
        self.rm_service = MangaService(parser=parser, client=client)

    def test_auth(self):
        loop = asyncio.get_event_loop()
        user_data = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
        response =  loop.run_until_complete(asyncio.gather(self.rm_service.auth(1, user_data)))
        self.assertEqual(len(self.rm_service.client.user_informations), 1)
        self.assertTrue("Вход произведен" in response[0].get("text"))