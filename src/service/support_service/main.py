import json
from src.service.http_client import simple_client, HTTPClient
from src.config import SUPPORT_SERVICE_ADDRESS

class SupportService:
    MESSAGE_PATH = "/message"
    SUPPORT_PATH = "/support"
    USER_PATH = "/user"
    
    def __init__(self, client: HTTPClient) -> None:
        self.client = client

    async def get_all_messages(self) -> dict:
        response = await self.client.get(f"{SUPPORT_SERVICE_ADDRESS}/message")
        return json.loads(response.get("text")) or {}

    async def get_message(self, id) -> dict:
        response = await self.client.get(f"{SUPPORT_SERVICE_ADDRESS}/message/{id}")
        return json.loads(response.get("text")) or {}

    async def get_unprocessed_message(self) -> dict:
        response = await self.client.get(f"{SUPPORT_SERVICE_ADDRESS}/message/unprocessed")
        return json.loads(response.get("text")) or {}

    async def get_messages_in_range(self, offset, limit) -> dict:
        response = await self.client.get(f"{SUPPORT_SERVICE_ADDRESS}/message?offset={offset}&limit={limit}")
        return json.loads(response.get("text")) or {}

    async def get_messages_count(self) -> dict:
        response = await self.client.get(f"{SUPPORT_SERVICE_ADDRESS}/message/count")
        return json.loads(response.get("text")) or {}

    async def get_support_message(self, support_id, processed = None):
        final_path = f"{SUPPORT_SERVICE_ADDRESS}{self.SUPPORT_PATH}/{support_id}/message"
        if processed is not None:
            final_path += f"?processed={int(processed)}"
        response = await self.client.get(final_path)
        return json.loads(response.get("text")) or {}

    async def set_message_response(self, support_id, message_id, response):
        final_path = f"{SUPPORT_SERVICE_ADDRESS}{self.MESSAGE_PATH}/answer"
        data = {"message_id": message_id, "response": response, "support_id": support_id}
        response = await self.client.post(final_path, data=data)
        return json.loads(response.get("text")) or {}

    async def create_support_message(self, user_id, message) -> None:
        final_path = f"{SUPPORT_SERVICE_ADDRESS}{self.USER_PATH}/{user_id}/message"
        data = {"message": message}
        response = await self.client.post(final_path, data=data)
        return json.loads(response.get("text")) or {}