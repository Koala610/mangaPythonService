from config import asyncio, uvicorn
from src import dp, app

@app.on_event("startup")
def start_bot():
    dp.start_polling()

if __name__ == "__main__":
    asyncio.create_task(uvicorn.run(app=app, host="localhost", port=8080))