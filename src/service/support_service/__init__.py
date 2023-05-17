from .main import SupportService
from src.service.http_client import simple_client

support_service = SupportService(simple_client)