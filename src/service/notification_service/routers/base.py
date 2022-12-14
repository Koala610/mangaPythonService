from config import APIRouter
from ...bot import telegram_bot

router = APIRouter()
@router.get("/")
async def hello_world():
    await telegram_bot.send_message(335271283, "Hi")
    return {"message": "Hello, World!"}