import asyncio
import time
from src import start_bot, telegram_bot 
from concurrent.futures import ProcessPoolExecutor

def start_second():
    async def test():
        while True:
            time.sleep(3)
            await telegram_bot.send_message(335271283, "11")
    asyncio.run(test())

async def main():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    tasks = []
    tasks.append(loop.run_in_executor(pool, start_bot))
    tasks.append(loop.run_in_executor(pool, start_second))
    await asyncio.gather(*tasks)
if __name__ == "__main__":
    asyncio.run(main())