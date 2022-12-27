from fastapi import APIRouter, HTTPException
from src.logger import logger
from ..models.notification_request import NotificationRequest
from ..utils.jwt import verify_jwt
from ..services.user_service import get_users
from src.service._bot.bot import telegram_bot

router = APIRouter()

@router.post("/notify/all/")
async def nofity_all(request: NotificationRequest):
    payload = verify_jwt(request.access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    users = get_users()
    for user in users:
        await telegram_bot.send_message(user.id, request.message)

