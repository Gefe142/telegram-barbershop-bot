import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import user

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не знайдено у змінних оточення!")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(user)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинений користувачем.")
