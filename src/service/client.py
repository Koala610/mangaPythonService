from typing import List, Union

import asyncio
import random

import aiohttp


class HTTPClient:
    CHANGE_PROXY_TIME = 30

    def __init__(self, proxies: List[str] = None):
        self.proxies = proxies or []
        self.current_proxy = None
        self.cookies = {}
        self.session = aiohttp.ClientSession()

    async def get(self, url: str, headers: dict = None, params: dict = None, return_text: bool = False) -> Union[aiohttp.ClientResponse, None]:
        async with self.session as client:
            async with client.get(
                url, headers=headers, params=params, proxy=self.current_proxy
            ) as resp:
                if return_text:
                    text = await resp.text()
                    return text
                return resp

    async def post(self, url: str, headers: dict = None, data: dict = None, return_text: bool = False) -> Union[aiohttp.ClientResponse, None]:
        async with self.session as client:
            async with client.post(
                url, headers=headers, data=data, proxy=self.current_proxy
            ) as resp:
                if return_text:
                    text = await resp.text()
                    return text
                return resp

    async def change_proxy(self, seconds: int = CHANGE_PROXY_TIME):
        if not self.proxies:
            return

        if self.current_proxy:
            await asyncio.sleep(seconds)
        self.current_proxy = random.choice(self.proxies)




async def main():
    client = HTTPClient()
    response = await client.get("https://google.com", return_text=True)
    print(response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
