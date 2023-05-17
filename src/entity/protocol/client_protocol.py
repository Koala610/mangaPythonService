from typing import Union, Tuple, Protocol
from fake_useragent import UserAgent


class HTTPClient(Protocol):
    BASE_URL: str
    BOOKMARKS_PATH: str
    AUTH_BASE_URL: str
    AUTH_PATH: str
    AUTH_CONTENT_TYPE: str
    AUTH_BODY_TEMPLATE: str

    async def auth(self, user_id: int, headers: dict,
                   data: dict, params: dict) -> dict: ...

    async def get(
        self, url: str, user_id: int,
        headers: dict = None, params: dict = None
    ) -> Union[dict, None]: ...

    async def post(
        self, url: str, user_id: int,
        headers: dict = None, data: dict = None
    ) -> Union[dict, None]: ...

    def get_user_information(self, user_id: int) -> dict: ...

    def get_gwt(self, user_id: int) -> str: ...

    def check_if_user_information_exists(self, user_id: int): ...

    def check_if_user_session(self, user_id: int): ...

    def save_user_information(self, user_id: int, user_information: dict): ...

    def create_user_information(self, user_id): ...

    def verify_user_session(self, user_id: int) -> None: ...

    async def get_auth_page_html(
        self, user_id: int, headers: dict) -> Tuple[dict, dict]: ...

    def get_auth_request_body(self, user_data: dict, target_uri: str): ...

    def set_auth_headers(self, headers: dict): ...

    async def get_bookmarks_data(
        self, user_id: int, limit: int, offset: int) -> list: ...

    def delete_cookie(self, user_id: int): ...
