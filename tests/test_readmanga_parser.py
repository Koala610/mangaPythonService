import unittest
import src.logger as logger
from src.entity.readmanga_parser import ReadmangaParser

class TestRMParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = ReadmangaParser()

    def test_parse_auth(self):
        test_content = ""
        with open("./tests/rm_auth.html", "r", encoding="utf8") as file:
            for line in file.readlines():
                test_content += line
        result = self.parser.parse_auth_page(test_content)
        targer_uri: str = result["target_uri"]
        url: str = result["url"]
        self.assertTrue("/login/" in targer_uri)
        self.assertTrue("/authenticate?" in url)

    def test_parse_manga_page(self):
        content = ""
        with open("./tests/rm_manga_page.html", "r", encoding="utf8") as file:
            content = file.read()
        result = self.parser.parse_manga_page(content)
        logger.debug(result)
        self.assertIsNotNone(result)
