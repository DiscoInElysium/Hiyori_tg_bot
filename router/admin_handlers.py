from aiogram import Router, F, types
from config import settings

router = Router(name=__name__)


@router.message(F.from_user.id == settings.admin_ids, F.text == "Hi")
async def secret_admin_message(message: types.Message):
    await message.reply("Hi, Boss!")

