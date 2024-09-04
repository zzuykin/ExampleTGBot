from aiogram import Bot, Dispatcher
import asyncio
import logging
import os
from dotenv import load_dotenv
from app.hendlers.main_hendler import main_router
from app.hendlers.reg_hendler import reg_router
from app.hendlers.menu_hendler import menu_router
from app.hendlers.order_hendler import order_router
from app.database.models import async_main


async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.include_router(reg_router)
    dp.include_router(menu_router)
    dp.include_router(order_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот завершил работу")
