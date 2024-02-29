from aiogram import Router, types
from aiogram.filters import Command


from keyboards.inline_keyboards.list import build_main_kb


router = Router(name=__name__)


@router.message(Command("list", prefix="!/"))
async def send_shop_message_kb(message: types.Message):
    await message.answer(
        text="Your actions:",
        reply_markup=build_main_kb(),
    )
