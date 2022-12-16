import asyncio
import random
import src.service.http_client.exceptions as exceptions
import aiohttp
import src.logger as logger

from typing import List, Union, Dict, Optional


class HTTPClient:
    CHANGE_PROXY_TIME = 300

    def __init__(self, proxies: List[str] = None):
        self.proxies: List[str] = proxies or []
        self.current_proxy: Optional[str] = None
        self.sessions: Dict[int, aiohttp.ClientSession] = {}

    async def get(
        self, url: str, user_id: int,
        headers: dict = None, params: dict = None
    ) -> Union[dict, None]:
        session = self.get_session(user_id)
        response = {}
        async with aiohttp.ClientSession(cookie_jar=session.cookie_jar) as client:
            async with client.get(
                url, headers=headers, params=params, proxy=self.current_proxy
            ) as resp:
                response["text"] = await resp.text()
                response["status"] = resp.status
        await self.save_session(session=session, user_id=user_id)
        return response

    async def post(
        self, url: str, user_id: int,
        headers: dict = None, data: dict = None
    ) -> Union[dict, None]:
        session = self.get_session(user_id)
        response = {}
        async with session as client:
            async with client.post(
                url, headers=headers, data=data, proxy=self.current_proxy
            ) as resp:
                response["text"] = await resp.text()
                response["status"] = resp.status
        await self.save_session(session=session, user_id=user_id)
        return response

    async def change_proxy(self, seconds: int = CHANGE_PROXY_TIME) -> None:
        if not self.proxies:
            return
        if self.current_proxy:
            await asyncio.sleep(seconds)
        self.current_proxy = random.choice(self.proxies)

    def create_session(self, user_id: int, headers: Optional[Dict[str, str]] = None) -> None:
        if headers is None:
            headers = {}
        session = aiohttp.ClientSession(headers=headers)
        self.sessions[user_id] = session
    
    def get_session(self, user_id: int) -> aiohttp.ClientSession:
        session = self.sessions.get(user_id)
        if session is None:
            logger.logger.warn(f"Session for user_id: {user_id} not found")
        return session
    
    def check_if_user_session_exists(self, user_id: int):
        return True if self.sessions.get(user_id) else False

    async def save_session(self, session: aiohttp.ClientSession, user_id: int):
        await session.close()
        self.sessions[user_id] = session

async def main():
    client = HTTPClient()
    response = await client.get("https://google.com", return_text=True)
    print(response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
