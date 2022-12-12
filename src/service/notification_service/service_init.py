from fastapi import FastAPI
from ...bot import telegram_bot

app = FastAPI()

@app.get("/")
async def hello_world():
    await telegram_bot.send_message(335271283, "Hi")
    return {"message": "Hello, World!"}
