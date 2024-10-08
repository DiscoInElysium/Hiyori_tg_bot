__all__ = ("router",)

from aiogram import Router

from .admin_handlers import router as admin_router
from .callback_handler import router as callback_router
from .commands import router as commands_router
from .common import router as common_router


router = Router(name=__name__)

router.include_routers(
    callback_router,
    commands_router,
    admin_router,
)

# this one has to be the last!
router.include_router(common_router)