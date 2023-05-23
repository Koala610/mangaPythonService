import bs4

from typing import Dict
from src.core_entity.protocol.manga_protocol import Manga
from src.core_logger import logger

class ReadmangaParser:
    def parse_manga_page(self, html: str) -> dict:
        soup = bs4.BeautifulSoup(html, "html.parser")
        progress_bar = soup.find("b", class_="progress-bar-text")
        progress_bar = progress_bar.get_text() if progress_bar else ""
        progress_bar = progress_bar.split("/")
        unread_chapters = int(progress_bar[1]) - int(progress_bar[0]) if len(progress_bar) == 2 else -1
        return {
            "unread_chapters": unread_chapters
        }

    def parse_bookmarks(self, html: str) -> Dict[int, Manga]:
        soup = bs4.BeautifulSoup(html, features="html.parser")
        items = soup.find("tr", class_="bookmark-row")
        return (self.parse_bookmark_row(item) for item in items)

    def parse_auth_page(self, html: str) -> dict:
        soup = bs4.BeautifulSoup(html, features="html.parser")
        form = soup.find("form")
        url = form.attrs["action"]
        pre_targer_uri = form.find("input", {"name": "targetUri"})
        if (pre_targer_uri is None):
            return None
        targer_uri = pre_targer_uri["value"]
        logger.info("Auth page successfully parsed...")
        return {
            "url": url,
            "target_uri": targer_uri
        }
