from typing import Protocol, Tuple
from src.entity.protocol.manga_protocol import Manga

class MangaParser(Protocol):

    def parse_manga_page(self, html: str) -> dict: ...

    def parse_bookmarks(self, html: str) -> Tuple[Manga]: ...

    def parse_auth_page(self, html: str) -> dict: ...
