import asyncio
import random
import aiohttp
import src.logger as logger

from typing import List, Union, Dict, Optional, Tuple
from fake_useragent import UserAgent

class RMHTTPClient:
    CHANGE_PROXY_TIME = 300
    BASE_URL = "https://readmanga.live"
    AUTH_PATH = "/internal/auth"
    AUTH_BODY_TEMPLATE = "targetUri={target_uri}&username={username}&password={password}&remember_me=true&_remember_me_yes=&remember_me_yes=on"

    def __init__(self, proxies: List[str] = None):
        self.proxies: List[str] = proxies or []
        self.current_proxy: Optional[str] = None
        self.user_informations: Dict[int, dict] = {}

    async def get(
        self, url: str, user_id: int,
        headers: dict = None, params: dict = None
    ) -> Union[dict, None]:
        user_information = self.get_user_information(user_id)
        response = {}
        async with aiohttp.ClientSession(cookie_jar=user_information.get("cookie_jar")) as client:
            async with client.get(
                url, headers=headers, params=params, proxy=self.current_proxy
            ) as resp:
                response["text"] = await resp.text()
                response["status"] = resp.status
                user_information["cookie_jar"] = client.cookie_jar
        self.save_user_information(user_id=user_id, user_information=user_information)
        return response

    async def post(
        self, url: str, user_id: int,
        headers: dict = None, data: dict = None
    ) -> Union[dict, None]:
        user_information = self.get_user_information(user_id)
        response = {}
        async with aiohttp.ClientSession(cookie_jar=user_information.get("cookie_jar")) as client:
            async with client.post(
                url, headers=headers, data=data, proxy=self.current_proxy
            ) as resp:
                response["text"] = await resp.text()
                response["status"] = resp.status
                user_information["cookie_jar"] = client.cookie_jar
        self.save_user_information(user_information=user_information, user_id=user_id)
        return response

    async def change_proxy(self, seconds: int = CHANGE_PROXY_TIME) -> None:
        if not self.proxies:
            return
        if self.current_proxy:
            await asyncio.sleep(seconds)
        self.current_proxy = random.choice(self.proxies)

    def get_user_information(self, user_id: int) -> dict:
        user_information = self.user_informations.get(user_id)
        if user_information is None:
            logger.logger.warning(f"Cookie for user_id: {user_id} not found")
        return user_information
    
    def check_if_user_information_exists(self, user_id: int):
        return True if self.user_informations.get(user_id) else False

    def check_if_user_session_exists(self, user_id: int):
        is_user_info_exists = self.check_if_user_information_exists(user_id)
        if is_user_info_exists:
            return True if self.user_informations.get(user_id).get("cookie_jar") else False
        return False

    def save_user_information(self, user_id: int, user_information: dict):
        self.user_informations[user_id] = user_information

    def create_user_information(self, user_id):
        user_agent = UserAgent()
        headers = {"User-Agent": user_agent.firefox}
        user_information = {"cookie_jar": None, "headers": headers}
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

    def get_auth_request_body(self, user_data: dict, parse_result: dict):
        data = self.AUTH_BODY_TEMPLATE.format(
            target_uri= parse_result.get("target_uri"),
            username=user_data.get("username"),
            password=user_data.get("password")
        )
        return data

async def main():
    client = HTTPClient()
    response = await client.get("https://google.com", return_text=True)
    print(response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
