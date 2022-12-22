from .main import MangaService
from src.entity import rm_parser, RMManga
from src.service.http_client import client

rm_service = MangaService(parser=rm_parser, client=client, Manga=RMManga)