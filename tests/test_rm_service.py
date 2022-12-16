import unittest
import asyncio
from src.service.rm_service.main import RMService
from src.entity.readmanga_parser import ReadmangaParser
from src.service.http_client.client import HTTPClient

class TestRMService(unittest.TestCase):
    def setUp(self) -> None:
        parser = ReadmangaParser()
        client = HTTPClient()
        self.rm_service = RMService(parser=parser, client=client)

    def test_auth(self):
        loop = asyncio.get_event_loop()
        response =  loop.run_until_complete(asyncio.gather(self.rm_service.auth(1)))
        self.assertEqual(len(self.rm_service.client.user_informations), 1)
        self.assertEqual(response[0]["status"], 200)