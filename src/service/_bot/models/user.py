import os

from src.repository import user_repository
from src.service.rm_service import rm_service
from src import logger

def create_user(user_id: int, name: str) -> None:
    user = user_repository.find_by_id(user_id)
    if user is None:
        user_repository.create(user_id=user_id, name=name)
        logger.info(f"User {user_id} create")

async def auth(user_id: int, data: dict):
    path = "./src/etc"
    await rm_service.auth(user_id=user_id, user_data=data)
    user_information = rm_service.client.get_user_information(user_id)
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path+f"/{user_id}", "w") as f:
        cookie_jar = user_information.get("cookie_jar")
        cookie_jar.save(f.name)
        logger.info(f"Cookies successfully save for user {user_id}")