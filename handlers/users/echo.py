from aiogram.dispatcher import filters
from aiogram import types

from filters import IsPrivate
from keyboards.default.menuKeyboard import mainMenu, bekor_qilish
from loader import dp, bot, i18n
from utils.api.service import ChatLogService, SupportRequestService
from utils.db_api.Service.user import UserBotService

_ = i18n.gettext


@dp.message_handler(IsPrivate(), text=["💬Chatni to'xtatish", "💬Stop Chat", "💬Остановить чат"])
async def echo(message: types.Message):
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    # Foydalanuvchining Telegram ID'sini oling
    telegram_id = message.from_user.id

    # Faol so'rovni olish
    active_request = SupportRequestService.get_active_request(telegram_id)
    if active_request:
        # Faol so'rovni yopish
        SupportRequestService.close_request(support_request_id=active_request['id'])
        if active_request['admin'] == message.from_user.id:
            await message.bot.send_message(chat_id=active_request['user'],
                                           text=_(
                                               "Sizning chatingiz to'xtatildi. Savollaringiz bo'lsa, yana yozishingiz mumkin."),
                                           reply_markup=mainMenu())
            await message.reply("Chat to'xtatildi!")
        else:
            # Adminga xabar yuborish
            admin_chat_id = active_request['admin']
            await message.reply(_("Chat to'xtatildi!"), reply_markup=mainMenu())
            await message.bot.send_message(chat_id=admin_chat_id, text="Foydalanuvchi chatni to'xtatdi.")
    else:
        await message.answer(_("Sizda hech qanday faol chat mavjud emas."))


@dp.message_handler(IsPrivate(), content_types=['text'])
async def echo(message: types.Message):
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    try:
        support_request = SupportRequestService.get_active_request(telegram_id=message.from_user.id)
        if support_request is None:
            await message.answer(_("Aktiv muloqot topilmadi."))
            return

        result = ChatLogService.create(telegram_id=message.from_user.id, support_request_id=support_request['id'],
                                       message=message.text)
        if result.status_code == 201:
            if message.from_user.id == support_request['admin']:
                user_telegram_id = support_request['user']
                await bot.send_message(chat_id=user_telegram_id,
                                       text=f"Admin:{message.from_user.full_name} \n\n{message.text}",
                                       reply_markup=bekor_qilish)
            else:
                # Foydalanuvchi admin bilan gaplashayotgan bo'lsa
                admin_telegram_id = support_request['admin']
                await bot.send_message(chat_id=admin_telegram_id,
                                       text=f"Foydalanuvchi:{message.from_user.full_name} \n\n{message.text}")
        else:
            await message.answer(_("Xatolik yuz berdi."))
    except:
        await message.answer(_("Xatolik yuz berdi!"))
