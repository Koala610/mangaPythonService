import aiohttp
import asyncio
import random
import aiohttp

from typing import Any, List, Coroutine, Optional


class HTTPClient:
    def __init__(self, proxies: Optional[List[str]] = None) -> None:
        if proxies is None:
            proxies = []
        self.proxies: List[str] = proxies
        self.cookies: dict = {}
        self.current_proxy: str = ""

    async def get(self, url: str) -> Coroutine[Any, Any, str]:
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(url, proxy=self.current_proxy) as response:
                return await response.text()

    async def post(self, url: str, data: dict) -> Coroutine[Any, Any, str]:
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.post(url, data=data, proxy=self.current_proxy) as response:
                return await response.text()

    def add_proxy(self, proxy: str) -> None:
        self.proxies.append(proxy)

    def switch_proxy(self) -> None:
        if len(self.proxies) == 0:
            return
        self.current_proxy = (random.randint(
            0, len(self.proxies))) % len(self.proxies)


async def main():
    client = HTTPClient()
    response = await client.get("https://google.com")
    print(response)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
