from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud import get_ongoings, get_remainder, get_users
from database.models import async_session


class MainListActions(IntEnum):
    ongoings = auto()
    followed = auto()
    root = auto()


class MainListCbData(CallbackData, prefix="main"):
    action: MainListActions


class OngoingsActions(IntEnum):
    details = auto()
    description = auto()
    remember = auto()
    link = auto()


class OngoingCbData(CallbackData, prefix="ongoing"):
    action: OngoingsActions
    id: int
    anime_id: int


class FollowedActions(IntEnum):
    details = auto()
    description = auto()
    delete = auto()
    link = auto()


class FollowedCbData(CallbackData, prefix="followed"):
    action: FollowedActions
    id: int
    anime_id: int


def build_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Show ongoings",
        callback_data=MainListCbData(action=MainListActions.ongoings).pack(),
    )
    builder.button(
        text="My followed",
        callback_data=MainListCbData(action=MainListActions.followed).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


async def build_ongoings_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Back to root",
        callback_data=MainListCbData(action=MainListActions.root).pack(),
    )

    ongoings = await get_ongoings(async_session)
    for idx, ongoing in enumerate(ongoings, start=1):
        builder.button(
            text=ongoing.anime_title,
            callback_data=OngoingCbData(
                action=OngoingsActions.details,
                id=idx,
                anime_id=ongoing.id,
            ),
        )
    builder.adjust(2)
    return builder.as_markup()


def ongoings_details_kb(
        ongoing_cb_data: OngoingCbData,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Back",
        callback_data=MainListCbData(action=MainListActions.ongoings).pack(),
    )
    for label, action in [
        ("Remember", OngoingsActions.remember),
        ("link", OngoingsActions.link),
        ("Description", OngoingsActions.description),
    ]:
        builder.button(
            text=label,
            callback_data=OngoingCbData(
                action=action,
                **ongoing_cb_data.model_dump(include={"id", 'anime_id'}),
            ),
        )
    builder.adjust(1, 2)
    return builder.as_markup()


async def build_ongoing_link_kb(
        product_cb_data: OngoingCbData,
) -> InlineKeyboardMarkup:
    ongoings = await get_ongoings(async_session)
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"⬅️ back to actions menu",
        callback_data=OngoingCbData(
            action=OngoingsActions.details,
            **product_cb_data.model_dump(include={"id", 'anime_id'}),
        ),
    )

    builder.button(
        text="↗️ Link",
        url=[i.link for i in ongoings][int(product_cb_data.id)-1],
    )
    return builder.as_markup()


async def build_description_kb(
        product_cb_data: OngoingCbData,
) -> InlineKeyboardMarkup:
    # ongoings = await get_ongoings(async_session)
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"⬅️ back to actions menu",
        callback_data=OngoingCbData(
            action=OngoingsActions.details,
            **product_cb_data.model_dump(include={"id", 'anime_id'}),
        ),
    )

    return builder.as_markup()


# FOLLOWINGS
async def build_my_list_kb(call: CallbackQuery) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Back to root",
        callback_data=MainListCbData(action=MainListActions.root).pack(),
    )
    ongoings = await get_ongoings(async_session)
    m2m_table = await get_remainder(async_session)
    users = await get_users(async_session)
    kb_buttons = []

    for user in users:
        if user.telegram_id == call.from_user.id:
            for m2m in m2m_table:
                if user.id == m2m.left_id:
                    for ongoing in ongoings:
                        if ongoing.id == m2m.right_id:

                            kb_buttons.append(ongoing.anime_title)

    for idx, ongoing in enumerate(kb_buttons, start=1):
        for ongoing_id in ongoings:
            if ongoing == ongoing_id.anime_title:
                builder.button(
                    text=ongoing,
                    callback_data=FollowedCbData(
                        action=FollowedActions.details,
                        id=idx,
                        anime_id=ongoing_id.id,
                    ),
                )

    builder.adjust(2)
    return builder.as_markup()


def my_list_details_kb(
        followed_cb_data: FollowedCbData,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Back",
        callback_data=MainListCbData(action=MainListActions.followed).pack(),
    )
    for label, action in [
        ("Delete", FollowedActions.delete),
        ("link", FollowedActions.link),
        ("Description", FollowedActions.description),
    ]:
        builder.button(
            text=label,
            callback_data=FollowedCbData(
                action=action,
                **followed_cb_data.model_dump(include={"id", 'anime_id'}),

            ),
        )
    builder.adjust(1, 2)
    return builder.as_markup()


async def my_list_link_kb(
        followed_cb_data: FollowedCbData,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"⬅️ back to actions menu",
        callback_data=FollowedCbData(
            action=FollowedActions.details,
            **followed_cb_data.model_dump(include={"id", 'anime_id'}),
        ),
    )
    m2m_table = await get_remainder(async_session)
    ongoings = await get_ongoings(async_session)
    link = ''
    for current in m2m_table:
        if current.right_id == followed_cb_data.anime_id:
            for ongoing in ongoings:
                if ongoing.id == current.right_id:
                    link = ongoing.link
    builder.button(
        text="↗️ Link",
        url=link,
    )
    return builder.as_markup()


async def my_list_description_kb(
        followed_cb_data: FollowedCbData,
) -> InlineKeyboardMarkup:
    # ongoings = await get_ongoings(async_session)
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"⬅️ back to actions menu",
        callback_data=FollowedCbData(
            action=FollowedActions.details,
            **followed_cb_data.model_dump(include={"id", 'anime_id'}),
        ),
    )

    return builder.as_markup()
