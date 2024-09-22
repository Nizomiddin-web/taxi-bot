from aiogram import types

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), )
async def admin_group(message: types.Message):
    pass


@dp.callback_query_handler(lambda c: c.data.startswith('muloqot'))
async def admin_group(call: types.CallbackQuery):
    bot_info =await call.message.bot.get_me()
    text = f"{call.message.text}\n<a href='https://t.me/{bot_info.username}?start={call.data}'>Havolani bosing</a>"
    await call.message.edit_text(text=text)
