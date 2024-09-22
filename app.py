from aiogram import executor

from keyboards.inline.Zikr_inlien_button import vil_btn
from loader import dp, bot
import middlewares, filters, handlers
# from utils.db_api.model import getUserList
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands







async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)
    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
