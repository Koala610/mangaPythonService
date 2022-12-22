from typing import Protocol

class Chapter(Protocol):
    volume: str
    chapter: str
    url: str

class Manga(Protocol):
    title: str
    current_chapter: Chapter
    unread_chapters: int
    url: str

    def from_json(cls, data: dict) -> object: ...

    def set_attrs(self, **kwargs) -> None: ...