from typing import Tuple
from dataclasses import dataclass

@dataclass
class RmParsedManga:
    title: str
    description: str


class ReadmangaParser:
    def parse_manga_page(self, html: str) -> RmParsedManga:
        pass

    def parse_bookmarks(self, html: str) -> Tuple[RmParsedManga]:
        pass
