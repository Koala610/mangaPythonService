from typing import Protocol, Tuple



class ParsedManga(Protocol):
    title: str
    description: str


class MangaParser(Protocol):

    def parse_manga_page(self, html: str) -> ParsedManga: ...

    def parse_bookmarks(self, html: str) -> Tuple[ParsedManga]: ...

    def parse_auth_page(self, html: str) -> dict: ...
