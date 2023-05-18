from src.service.support_service import support_service
from src.repository import user_repository
from aiogram.types import Message
from src.service._bot.bot import telegram_bot, dp

async def get_all_messages():
    messages = await support_service.get_all_messages()

async def get_processing_messages(support_id):
    return await support_service.get_support_message(support_id=support_id)

async def get_messages_in_range(offset, range):
    return await support_service.get_messages_in_range(offset, range)