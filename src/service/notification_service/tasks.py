import service_init
import config

@service_init.app.on_event("startup")
async def start_bot():
    config.asyncio.create_task(config.dp.start_polling())