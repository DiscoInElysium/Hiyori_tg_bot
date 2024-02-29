import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot
from aiogram import Dispatcher

from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from anime_parser.anime_revision import message_release_day, check_new_ongoing, check_new_release_date
# from automaton.schedule_handler import wait_until
# import config
from config import settings
from database.models import async_main
# from database.crud import insert_ongoings
# from database.models import async_main, async_session

from router import router as main_router
# from automaton.schedule_handler import on_startup
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main():
    await async_main()
    # # await insert_ongoings(async_session)
    # await wait_until(dt)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    schedu = AsyncIOScheduler(timezone='Europe/Moscow')
    schedu.add_job(message_release_day,
                   trigger='cron',
                   hour='17-18',
                   minute='25',
                   start_date=datetime.now())
    schedu.add_job(check_new_ongoing,
                   trigger='cron',
                   hour='12-13',
                   minute='25',
                   start_date=datetime.now())
    schedu.add_job(check_new_release_date,
                   trigger='cron',
                   hour='20-21',
                   minute='25',
                   start_date=datetime.now())
    schedu.start()

    dp.include_router(main_router)
    bot = Bot(
        token=settings.bot_token,
        parse_mode=ParseMode.HTML,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bedge')
