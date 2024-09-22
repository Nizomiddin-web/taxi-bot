from aiogram import types

from data.config import ADMIN_TEAM_GROUP
from filters import IsPrivate
from keyboards.default.menuKeyboard import bekor_qilish
from keyboards.inline.admin_support_inline import admin_support_keyboard, muloqot_btn
from loader import dp
from utils.api.service import SupportRequestService


@dp.message_handler(IsPrivate(), text="💬 Admin bilan Muloqot")
async def user_admin_support(message: types.Message):
    text = f"Assalomu alaykum {message.from_user.first_name}\n\nSizda savollar mavjudmi?\nAdminlarimiz bilan bog'lanishni istaysizmi?"
    await message.answer(text=text, reply_markup=admin_support_keyboard())


@dp.callback_query_handler(text="support_no")
async def user_admin_support(call: types.CallbackQuery):
    await call.message.edit_text("Salomat bo'ling!")


@dp.callback_query_handler(text="support_yes")
async def user_admin_support(call: types.CallbackQuery):
    await call.message.delete()
    text = "Sizning so'rovingiz qabul qilindi,\n\niltimos navbatni kuting.\n\nAdmin bog'lanishini kuting\n\nChatni " \
           "to'xtatish uchun pastdagi tugmani bosing👇 "
    result = SupportRequestService.create(telegram_id=call.from_user.id)
    if result.status_code == 201:
        result = result.json()
        await call.message.answer(text=text, reply_markup=bekor_qilish)
        text = f"Foydalanuvchi:<a href='tg://user?id={call.from_user.id}'>{call.from_user.full_name}</a>\ndan Muloqot so'rovi keldi"
        await call.bot.send_message(chat_id=ADMIN_TEAM_GROUP, text=text, reply_markup=muloqot_btn(f"{call.from_user.id}_{result['id']}"))
    else:
        await call.message.answer("Xatolik yuz berdi iltimos keyinroq urinib ko'ring!")
