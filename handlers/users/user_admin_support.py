from aiogram import types

from data.config import ADMIN_TEAM_GROUP
from filters import IsPrivate
from keyboards.default.menuKeyboard import bekor_qilish
from keyboards.inline.admin_support_inline import admin_support_keyboard, muloqot_btn
from loader import dp, i18n
from utils.api.service import SupportRequestService
from utils.db_api.Service.user import UserBotService

_ = i18n.gettext


@dp.message_handler(IsPrivate(), text=["💬 Admin bilan Muloqot", "💬 Contact Admin", "💬 Связь с администратором"])
async def user_admin_support(message: types.Message):
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    text = _("Assalomu alaykum {name}\n\nSizda savollar mavjudmi?\nAdminlarimiz bilan bog'lanishni istaysizmi?").format(
        name=message.from_user.first_name)
    await message.answer(text=text, reply_markup=admin_support_keyboard())


@dp.callback_query_handler(text="support_no")
async def user_admin_support(call: types.CallbackQuery):
    user_bot = UserBotService.find_or_create(call.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    await call.message.edit_text(_("Salomat bo'ling!"))


@dp.callback_query_handler(text="support_yes")
async def user_admin_support(call: types.CallbackQuery):
    await call.message.delete()
    user_bot = UserBotService.find_or_create(call.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    text = _("Sizning so'rovingiz qabul qilindi,\n\niltimos navbatni kuting.\n\nAdmin bog'lanishini kuting\n\nChatni "
             "to'xtatish uchun pastdagi tugmani bosing👇 ")
    result = SupportRequestService.create(telegram_id=call.from_user.id)
    if result.status_code == 201:
        result = result.json()
        await call.message.answer(text=text, reply_markup=bekor_qilish())
        text = _("Foydalanuvchi:<a href='tg://user?id={user_id}'>{name}</a>\ndan "
                 "Muloqot so'rovi keldi").format(user_id=call.from_user.id, name=call.from_user.full_name)
        await call.bot.send_message(chat_id=ADMIN_TEAM_GROUP, text=text,
                                    reply_markup=muloqot_btn(f"{call.from_user.id}_{result['id']}"))
    else:
        await call.message.answer(_("Xatolik yuz berdi iltimos keyinroq urinib ko'ring!"))
