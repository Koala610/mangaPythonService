import aiohttp

from typing import Union

class HTTPClient:

    def __init__(self):
        pass

    async def get(self, url: str,headers: dict = None, params: dict = None) -> Union[dict, None]:
        headers = headers or {}
        params = params or {}
        response = {}
        async with aiohttp.ClientSession() as client:
            try:
                async with client.get(url, headers=headers, params=params) as resp:
                    response["text"] = await resp.text()
                    response["status"] = resp.status
            except aiohttp.ClientConnectionError:
                return response
        return response

    async def post(self, url: str, headers: dict = None, data: dict = None, pack_data: bool = False) -> Union[dict, None]:
        headers = headers or {}
        data = data or {}
        response = {}
        if pack_data:
            data = {"data": data}
        async with aiohttp.ClientSession() as client:
            async with client.post(url, headers=headers, json=data) as resp:
                response["text"] = await resp.text()
                response["status"] = resp.status
        return response