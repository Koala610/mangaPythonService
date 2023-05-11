from fastapi import APIRouter
from ..models.notification_request import NotificationRequest
from ..services.user_service import get_users
from src.service._bot.bot import telegram_bot
from src.service._bot_http_cover.services.admin_service import check_if_user_admin

router = APIRouter()

@router.post("/notify/all/")
@check_if_user_admin
async def nofity_all(request: NotificationRequest):
    users = get_users()
    for user in users:
        await telegram_bot.send_message(user.id, request.message)
