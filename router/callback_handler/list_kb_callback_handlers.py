from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from database.crud import get_ongoings, create_remainder, get_users, get_remainder, delete_association
from database.models import async_session
from keyboards.inline_keyboards.list import (
    MainListCbData,
    MainListActions,
    build_main_kb,
    build_ongoings_kb,
    build_my_list_kb,
    OngoingCbData,
    OngoingsActions,
    FollowedCbData,
    FollowedActions,
    ongoings_details_kb,
    build_ongoing_link_kb, build_description_kb, my_list_link_kb, my_list_description_kb, my_list_details_kb,
)

router = Router(name=__name__)


@router.callback_query(
    MainListCbData.filter(F.action == MainListActions.ongoings),
)
async def send_ongoings_list(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        text="Select anime you are interested in:",
        reply_markup=await build_ongoings_kb(),
    )


# main_kb | build_main_kb
@router.callback_query(
    MainListCbData.filter(F.action == MainListActions.root),
)
async def handle_main_kb_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        text="Your actions:",
        reply_markup=build_main_kb(),
    )


@router.callback_query(
    MainListCbData.filter(F.action == MainListActions.followed),
)
async def handle_my_list_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        text='Your anime list:',
        reply_markup=await build_my_list_kb(call),
    )


@router.callback_query(
    OngoingCbData.filter(F.action == OngoingsActions.details),
)
async def handle_ongoings_details_button(
        call: CallbackQuery,
        callback_data: OngoingCbData,
):
    await call.answer()
    ongoings = await get_ongoings(async_session)
    message_text = markdown.text(
        markdown.hbold(f"Anime №{callback_data.id}"),
        markdown.text(
            markdown.hbold("Title:"),
            [i.anime_title for i in ongoings][int(callback_data.id) - 1],
        ),
        sep="\n",
    )
    await call.message.edit_text(
        text=message_text,
        reply_markup=ongoings_details_kb(callback_data),
    )


# skip for now
@router.callback_query(
    OngoingCbData.filter(F.action == OngoingsActions.remember),
)
async def handle_remember_button(
        call: CallbackQuery,
        callback_data: OngoingCbData,
):
    ongoings = await get_ongoings(async_session)
    idx_anime = [i.id for i in ongoings][int(callback_data.id) - 1]
    users = await get_users(async_session)
    idx_user = [i.id for i in users]
    telegram_user = [i.telegram_id for i in users]
    res = {telegram_user[i]: idx_user[i] for i in range(len(idx_user))}

    await create_remainder(res[call.from_user.id], idx_anime, async_session)
    await call.answer()


# do it next
@router.callback_query(
    OngoingCbData.filter(F.action == OngoingsActions.link),
)
async def handle_ongoing_link_button(
        call: CallbackQuery, callback_data: OngoingCbData,
):

    await call.message.edit_reply_markup(
        reply_markup=await build_ongoing_link_kb(callback_data),
    )


# create description
@router.callback_query(
    OngoingCbData.filter(F.action == OngoingsActions.description),
)
async def handle_ongoing_description_button(
        call: CallbackQuery, callback_data: OngoingCbData,
):
    ongoings = await get_ongoings(async_session)
    idx = call.data.split(':')[2]

    await call.message.edit_text(
        text=[i.anime_description for i in ongoings][int(idx) - 1],
        reply_markup=await build_description_kb(callback_data),
    )


@router.callback_query(
    FollowedCbData.filter(F.action == FollowedActions.delete),
)
async def handle_delete_button(
        call: CallbackQuery,
        callback_data: FollowedCbData,
):
    m2m_table = await get_remainder(async_session)
    ongoings = await get_ongoings(async_session)
    idx = 0
    for current in m2m_table:
        if current.id == callback_data.id:
            for ongoing in ongoings:
                if ongoing.id == current.right_id:
                    idx = ongoing.id

    await delete_association(idx, async_session)
    await call.answer()


@router.callback_query(
    FollowedCbData.filter(F.action == FollowedActions.details),
)
async def handle_my_list_details_button(
        call: CallbackQuery,
        callback_data: FollowedCbData,
):
    await call.answer()
    m2m_table = await get_remainder(async_session)
    ongoings = await get_ongoings(async_session)
    title = ''
    # print(f"CALL BACK ID: {callback_data.anime_id}")
    for current in m2m_table:
        if current.right_id == callback_data.anime_id:
            for ongoing in ongoings:
                if ongoing.id == current.right_id:
                    title = ongoing.anime_title

    message_text = markdown.text(
        markdown.hbold(f"Anime №{callback_data.id}"),
        markdown.text(
            markdown.hbold("Title:"),
            title,
        ),
        sep="\n",
    )
    await call.message.edit_text(
        text=message_text,
        reply_markup=my_list_details_kb(callback_data),
    )


# do it next
@router.callback_query(
    FollowedCbData.filter(F.action == FollowedActions.link),
)
async def handle_followed_link_button(
        call: CallbackQuery, callback_data: FollowedCbData,
):
    await call.message.edit_reply_markup(
        reply_markup=await my_list_link_kb(callback_data),
    )


# create description
@router.callback_query(
    FollowedCbData.filter(F.action == FollowedActions.description),
)
async def handle_followed_description_button(
        call: CallbackQuery, callback_data: FollowedCbData,
):
    m2m_table = await get_remainder(async_session)
    ongoings = await get_ongoings(async_session)
    description = ''
    for current in m2m_table:
        if current.right_id == callback_data.anime_id:
            for ongoing in ongoings:
                if ongoing.id == current.right_id:
                    description = ongoing.anime_description
    await call.message.edit_text(
        text=description,
        reply_markup=await my_list_description_kb(callback_data),
    )
