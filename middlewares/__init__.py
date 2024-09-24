from aiogram import Dispatcher

from loader import dp, i18n
from .throttling import ThrottlingMiddleware
# from .checkedMiddleware import BigBrother

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(i18n)
    # dp.middleware.setup(BigBrother())