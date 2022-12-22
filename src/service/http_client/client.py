import asyncio
import aiohttp
import json
import src.logger as logger
import random

from typing import List, Union, Dict, Optional, Tuple
from fake_useragent import UserAgent
from src.entity.protocol.manga_protocol import Manga


class RMHTTPClient:
    AUTH_BASE_URL = "https://grouple.co"
    AUTH_PATH = "/internal/auth"
    AUTH_CONTENT_TYPE = "application/x-www-form-urlencoded"
    AUTH_BODY_TEMPLATE = "targetUri={target_uri}&username={username}&password={password}&remember_me=true&_remember_me_yes=&remember_me_yes=on"
    BASE_URL = "https://readmanga.live"
    BOOKMARKS_PATH = "/private/bookmarks"
    CHANGE_PROXY_TIME = 300
    BOOKMARKS_GETTTING_PARAMS = {
        "bookmarkSort":"NAME",
        "elementFilter":[],
        "statusFilter":["WATCHING"],
        "includeUpdates":True,
        "limit":50,
        "offset":0
    }
    def __init__(self, proxies: List[str] = None):
        self.proxies: List[str] = proxies or []
        self.current_proxy: Optional[str] = None
        self.user_informations: Dict[int, dict] = {}

    async def auth(self, user_id: int, headers: dict, data: dict, params: dict) -> dict:
        self.set_auth_headers(headers)
        data = self.get_auth_request_body(
            user_data=data, target_url=params.get("target_uri")
        )
        response = await self.post(
            self.AUTH_BASE_URL+params.get("url"), user_id=user_id, headers=headers, data=data
        )
        return response

    async def get(
        self, url: str, user_id: int,
        headers: dict = None, params: dict = None, use_gwt: bool = False
    ) -> Union[dict, None]:
        user_agent = UserAgent()
        headers["User-Agent"] = user_agent.firefox
        user_information = self.get_user_information(user_id)
        if use_gwt:
            gwt = self.get_gwt(user_id)
            headers["Authorization"] = f"Bearer {gwt}"
        response = {}
        async with aiohttp.ClientSession(cookie_jar=user_information.get("cookie_jar")) as client:
            async with client.get(
                url, headers=headers, params=params, proxy=self.current_proxy
            ) as resp:
                response["text"] = await resp.text()
                response["status"] = resp.status
                user_information["cookie_jar"] = client.cookie_jar
        self.save_user_information(
            user_id=user_id, user_information=user_information)
        return response

    async def post(
        self, url: str, user_id: int,
        headers: dict = None, data: dict = None
    ) -> Union[dict, None]:
        user_information = self.get_user_information(user_id)
        user_agent = UserAgent()
        headers["User-Agent"] = user_agent.firefox
        response = {}
        async with aiohttp.ClientSession(cookie_jar=user_information.get("cookie_jar")) as client:
            async with client.post(
                url, headers=headers, data=data, proxy=self.current_proxy
            ) as resp:
                response["text"] = await resp.text()
                response["status"] = resp.status
                user_information["cookie_jar"] = client.cookie_jar
        self.save_user_information(
            user_information=user_information, user_id=user_id)
        return response

    async def change_proxy(self, seconds: int = CHANGE_PROXY_TIME) -> None:
        if not self.proxies:
            return
        if self.current_proxy:
            await asyncio.sleep(seconds)
        self.current_proxy = random.choice(self.proxies)

    def get_user_information(self, user_id: int) -> Optional[dict]:
        self.verify_user_session(user_id)
        user_information = self.user_informations.get(user_id)
        if user_information is None:
            logger.logger.warning(
                f"Information for user_id: {user_id} not found")
            return None
        return user_information

    def check_if_user_information_exists(self, user_id: int) -> bool:
        return True if self.user_informations.get(user_id) else False

    def check_if_user_session_exists(self, user_id: int) -> bool:
        is_user_info_exists = self.check_if_user_information_exists(user_id)
        if is_user_info_exists:
            if self.user_informations.get(user_id).get("cookie_jar"):
                return True
            logger.warning(f"Cookie for user_id: {user_id} not found")
        return False

    def save_user_information(self, user_id: int, user_information: dict) -> None:
        self.user_informations[user_id] = user_information

    def create_user_information(self, user_id, cookie_jar = None) -> None:
        cookie_jar = cookie_jar or None
        user_information = {"cookie_jar": cookie_jar}
        self.save_user_information(
            user_id=user_id, user_information=user_information)

    def verify_user_session(self, user_id: int) -> None:
        is_session_exists = self.check_if_user_session_exists(
            user_id=user_id)
        if not is_session_exists:
            self.create_user_information(user_id=user_id)

    async def get_auth_page_html(self, user_id: int, headers: dict) -> Tuple[dict, dict]:
        response = await self.get(
            self.BASE_URL+self.AUTH_PATH,
            user_id=user_id, headers=headers
        )
        return response.get("text")

    def get_auth_request_body(self, user_data: dict, target_url: str) -> str:
        data = self.AUTH_BODY_TEMPLATE.format(
            target_uri=target_url,
            username=user_data.get("username"),
            password=user_data.get("password")
        )
        return data

    def set_auth_headers(self, headers: dict) -> None:
        headers["DNT"] = "1"
        headers["Content-Type"] = self.AUTH_CONTENT_TYPE

    async def get_bookmarks_data(self, user_id: int) -> list:
        headers = {}
        gwt = self.get_gwt(user_id)
        headers["Authorization"] = f"Bearer {gwt}"
        headers["Content-Type"] = "application/json"
        body = self.BOOKMARKS_GETTTING_PARAMS
        response = await self.post(self.AUTH_BASE_URL+"/api/bookmark/list", user_id, headers, json.dumps(body))
        result = json.loads(response.get("text"))
        result = result.get("list")
        return result

    def get_gwt(self, user_id: int) -> str:
        user_information = self.get_user_information(user_id)
        cookie_jar = user_information.get("cookie_jar")
        cookies = cookie_jar._cookies.get("grouple.co")
        gwt: str = cookies.get("gwt").OutputString().split(";")[0]
        gwt = gwt.split("=")[1]
        return gwt


async def main():
    cookieJar = aiohttp.CookieJar()
    cookieJar.save()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
