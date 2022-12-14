import aiohttp
import asyncio
import random
import aiohttp

class HTTPClient:
    def __init__(self, proxies = None):
        if proxies is None:
            proxies = []
        self.cookies = {}
        self.proxies = proxies
        self.current_proxy = ""
        
    async def get(self, url):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(url, proxy=self.current_proxy) as response:
                return await response.text()
    
    async def post(self, url, data):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.post(url, data=data, proxy=self.current_proxy) as response:
                return await response.text()
    
    def add_proxy(self, proxy):
        self.proxies.append(proxy)
        
    def switch_proxy(self):
        if len(self.proxies) == 0:
            return
        self.current_proxy = (random.randint(0, len(self.proxies))) % len(self.proxies)

async def main():
    client = HTTPClient()
    response = await client.get("https://google.com")
    print(response)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()