

import time
from datetime import datetime

from aiogram import Bot
from config import settings

from anime_parser.anime_methods import anime_description, anime_stats, final_episode_release_date
from anime_parser.ongoing_anime import anime_ongoing_list

from database.crud import get_ongoings, delete_ongoing, get_remainder, get_users
from database.models import async_session


# from handler import anime_release


# add new anime
async def check_new_ongoing():
    ongoing_dic = anime_ongoing_list()
    temporary_list = []
    check_new = []
    check_old = []
    result = []

    for k in ongoing_dic.keys():
        check_new.append(k)

    ongoings = await get_ongoings(async_session)
    for ongoing in ongoings:
        check_old.append(ongoing.anime_title)

    for title in check_new:
        if title not in check_old:
            temporary_list.append(title)
            time.sleep(2)
            temporary_list.append(anime_description(ongoing_dic[title]))
            time.sleep(2)
            temporary_list.append(ongoing_dic[title])
            time.sleep(2)
            temporary_list.append(anime_stats(ongoing_dic[title])[0])
            time.sleep(2)
            temporary_list.append(final_episode_release_date(anime_stats(ongoing_dic[title])))
            time.sleep(2)
            result.append(tuple(temporary_list))
            temporary_list.clear()

    return result


# update
async def check_new_release_date():
    ongoing_dic = anime_ongoing_list()
    temporary_list = []
    check_new = {}
    check_old = {}
    result = []

    for k, v in ongoing_dic.items():
        check_new[k] = (final_episode_release_date(anime_stats(v)))

    ongoings = await get_ongoings(async_session)
    for ongoing in ongoings:
        check_old[ongoing.anime_title] = ongoing.release_date

    for key, value in check_new.items():
        if check_new[key] != check_old[key]:
            temporary_list.append(key)
            temporary_list.append(value)
            result.append(tuple(temporary_list))
            temporary_list.clear()

    return result


# problem can ber here
async def anime_release(user_id, anime_title):
    bot = Bot(token=settings.bot_token)
    await bot.send_message(user_id, f'Today is {anime_title} release day (*^‿^*)')
    await bot.session.close()


async def message_release_day():
    week = {'пн': 0, 'вт': 1, 'ср': 2, 'чт': 3, 'пт': 4, 'сб': 5, 'вс': 6}
    users = await get_users(async_session)
    ongoings = await get_ongoings(async_session)
    m2m_table = await get_remainder(async_session)
    for ongoing in ongoings:
        if ongoing.release_day in week.keys() and week[ongoing.release_day] == datetime.today().weekday():
            for m2m in m2m_table:
                if m2m.right_id == ongoing.id:
                    for user in users:
                        if user.id == m2m.left_id:
                            await anime_release(user.telegram_id, ongoing.anime_title)
