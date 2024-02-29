from aiogram import Router, types
from aiogram.filters import CommandStart, Command


from database.crud import insert_users
from database.models import async_session

router = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"'Hi {message.from_user.full_name} (´• ω •`).\n"
                         f"You can use /help to learn more about my capabilities (◡‿◡ *).'")
    await insert_users(message.from_user.id, async_session)


@router.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    await message.answer("I can remind you about the release of new episodes of the anime you selected from the list.\n"
                         "(use command list and make chose (￢‿￢ ))")
