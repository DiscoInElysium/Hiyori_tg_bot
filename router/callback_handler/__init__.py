from aiogram import Router

from .list_kb_callback_handlers import router as catalog_kb_callback_router

router = Router(name=__name__)

router.include_routers(
    catalog_kb_callback_router,
)