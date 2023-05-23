from .main import MangaService
from src.core_entity.manga import RMManga
from src.service.http_client import client
from src.parser import rm_parser

rm_service = MangaService(parser=rm_parser, client=client, Manga=RMManga)