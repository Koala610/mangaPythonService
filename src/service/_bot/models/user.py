import os

from src.repository import user_repository
from src.service.rm_service import rm_service
from src import logger


def create_user(user_id: int, name: str) -> None:
    user = user_repository.find_by_id(user_id)
    if user is None:
        user_repository.create(id=user_id, name=name)
        logger.info(f"User {user_id} create")


async def auth(user_id: int, data: dict):
    path = "./src/etc"
    await rm_service.auth(id=user_id, user_data=data)
    rm_service.client.save_cookie(user_id)
    logger.info(f"Cookies successfully save for user {user_id}")

def subscribe_on_updates(user_id: int):
    is_subscribed = check_if_subscribed(user_id)
    user_repository.update(user_id, is_subscribed=not is_subscribed)

def check_if_subscribed(user_id: int):
    return user_repository.check_if_subscribed(user_id)