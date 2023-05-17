from src.service.http_client import simple_client, HTTPClient
from src.config import SUPPORT_SERVICE_ADDRESS

class SupportService:
    MESSAGE_PATH = "/message"
    SUPPORT_PATH = "/support"
    USER_PATH = "/user"
    
    def __init__(self, client: HTTPClient) -> None:
        self.client = client

    async def get_all_messages(self) -> dict:
        return await self.client.get(f"{SUPPORT_SERVICE_ADDRESS}/message").get("text") or ""

    async def get_support_message(self, support_id):
        final_path = f"{SUPPORT_SERVICE_ADDRESS}/{support_id}/message"
        return await self.client.get(final_path).get("text")

    async def set_message_response(self, message_id, response):
        final_path = f"{SUPPORT_SERVICE_ADDRESS}{self.MESSAGE_PATH}"
        data = {"message_id": message_id, "response": response}
        return await self.client.post(final_path, data=data).get("text")

    async def create_support_message(self, user_id, message) -> None:
        final_path = f"{SUPPORT_SERVICE_ADDRESS}{self.USER_PATH}/{user_id}/message"
        data = {"message": message}
        await self.client.post(final_path, data=data)