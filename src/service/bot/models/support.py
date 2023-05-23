from src.service.support_service import support_service
from src.service.bot.bot import telegram_bot

async def get_all_messages():
    return await support_service.get_all_messages()

async def get_processing_messages(support_id):
    return await support_service.get_support_message(support_id=support_id)

async def get_messages_in_range(offset, range):
    return await support_service.get_messages_in_range(offset, range)

async def answer_message(message_id: int, response: str, support_id: int):
        message_to_response = await support_service.get_message(message_id)
        await support_service.set_message_response(message_id=message_id, response=response, support_id=support_id)
        final_message = f"""
            Вам ответили
Сообщение: {message_to_response.get("message")}
ID члена поддержки: {support_id}
Ответ: {response}
        """
        await telegram_bot.send_message(message_to_response.get("user_id"), final_message)