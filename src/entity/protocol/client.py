import asyncio

from typing import Union, Tuple, Protocol
from fake_useragent import UserAgent

class HTTPClient(Protocol):
    BASE_URL = ""
    AUTH_PATH = ""
    AUTH_BODY_TEMPLATE = ""

    async def get(
        self, url: str, user_id: int,
        headers: dict = None, params: dict = None
    ) -> Union[dict, None]: ...

    async def post(
        self, url: str, user_id: int,
        headers: dict = None, data: dict = None
    ) -> Union[dict, None]: ...

    def get_user_information(self, user_id: int) -> dict: ...
    
    def check_if_user_information_exists(self, user_id: int): ...

    def check_if_user_session(self, user_id: int): ...

    def save_user_information(self, user_id: int, user_information: dict): ...

    def create_user_information(self, user_id): ...

    def verify_user_session(self, user_id: int) -> None: ...

    async def get_auth_page_html(self, user_id: int, headers: dict) -> Tuple[dict, dict]: ...

    def get_auth_request_body(self, user_data: dict, parse_result: dict): ...