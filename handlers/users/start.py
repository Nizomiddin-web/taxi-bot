from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentType, CallbackQuery

from filters import IsPrivate
from keyboards.default.menuKeyboard import mainMenu, bekor_qilish, send_contact
from keyboards.inline.set_lang_inline import language_selection_keyboard
from loader import dp, i18n
from states.userState import VerificationStates
from utils.api.service import UserService, MachineCheckService, FaceCheckService, SupportRequestService, DemoService
from utils.db_api.Service.user import UserBotService
import random

_ = i18n.gettext
from utils.misc.send_sms import send_sms


def generate_verification_code(length=4):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


@dp.message_handler(IsPrivate(), commands=['set_lang'])
async def start_handler(message: types.Message):
    await message.answer("Choose Language", reply_markup=language_selection_keyboard())


@dp.callback_query_handler(lambda call: call.data.startswith('set_lang_'))
async def set_language(call: CallbackQuery):
    await call.message.delete()
    lang_code = call.data.split('_')[2]  # 'uz', 'ru', 'en'

    if lang_code == 'uz':
        i18n.ctx_locale.set('uz')
        response_text = _("Til o'zgartirildi.")
    elif lang_code == 'ru':
        i18n.ctx_locale.set('ru')
        response_text = _("Язык изменен.")
    elif lang_code == 'en':
        i18n.ctx_locale.set('en')
        response_text = _("Language changed.")
    UserBotService.set_lang(tg_id=call.from_user.id, lang=lang_code)
    user = UserService.find_or_create(call.from_user.id)
    if user['is_admin']:
        await call.message.answer("Assalomu alaykum Admin!!!")
        await call.answer()
        return
    if user['verification_status']:
        await call.message.answer(_("Hush kelibsiz siz ro'yhatdan o'tgansiz"), reply_markup=mainMenu())
        await call.answer()
    else:
        await call.message.answer(_("Telefon raqamingizni yuborish tugmasini bosing👇"), reply_markup=send_contact())
        await call.answer()
        await VerificationStates.ask_phone.set()
    # Callbackni tasdiqlash


@dp.message_handler(IsPrivate(), commands=['start'])
async def start_handler(message: types.Message):
    user = UserBotService.find_or_create(message.from_user.id)
    if not user.lang:
        await message.answer("Choose Language", reply_markup=language_selection_keyboard())
        return
    i18n.ctx_locale.set(user.lang)
    deep_link_parameter = message.get_args()
    if deep_link_parameter:
        data = deep_link_parameter.split('_')
        user_id = data[1]
        support_id = data[-1]
        result = SupportRequestService.update(id=support_id, telegram_id=message.from_user.id)
        if result.status_code == 404:
            await message.answer(_("So'rov topilmadi!"))
            return
        await message.answer(_("Ulanish Hosil qilindi!"), reply_markup=bekor_qilish())
        await message.bot.send_message(chat_id=user_id, text=_("Admin siz bilan bog'landi❗️"))
        await message.bot.send_message(chat_id=user_id,
                                       text=_('Assalomu alaykum\nIsmim:{admin_name}\nQanday savollaringiz bor?').format(
                                           admin_name=message.from_user.first_name))
        return
    user = UserService.find_or_create(message.from_user.id)
    if user['is_admin']:
        await message.answer("Assalomu alaykum Admin!!!")
        return
    if user['verification_status']:
        await message.answer(_("Hush kelibsiz siz ro'yhatdan o'tgansiz"), reply_markup=mainMenu())
    else:
        await message.answer(_("Telefon raqamingizni yuborish tugmasini bosing👇"), reply_markup=send_contact())
        await VerificationStates.ask_phone.set()


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT,
                    state=VerificationStates.ask_phone)
async def phone_number_handler(message: types.Message, state: FSMContext):
    user = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user.lang)
    sms_code = generate_verification_code()
    try:
        is_have = DemoService.is_have_user(tg_id=message.from_user.id, phone_number=message.contact.phone_number,
                                           verification_code=sms_code)
        if is_have:
            try:
                text = f"🏰Saroylar Jangi⚔️ bot uchun tasdiqlash kodi Kod: {sms_code}"
                # res = send_sms(phone_number=998940660299, message=text)
                await message.answer(f"CODE:{sms_code}")
                await message.answer(_("Yuborilgan SMS CODE ni yozing!"))
                await VerificationStates.generate_code.set()
            except:
                await message.answer(_("Code yuborishda xatolik yuz berdi!"))
                await state.finish()
        else:
            await message.answer(_("Telefonr Raqam tizimda topilmadi"))
            await state.finish()
    except:
        await message.answer(_("Xatolik yuz berdi,Iltimos keyinroq urinib ko'ring!"))


# @dp.message_handler(IsPrivate(), lambda message: message.text and message.text.isdigit(),
#                     state=VerificationStates.ask_phone)
# async def phone_number_handler(message: types.Message, state: FSMContext):
#     sms_code = generate_verification_code()
#     is_have = DemoService.is_have_user(tg_id=message.from_user.id, phone_number=message.text,
#                                        verification_code=sms_code)
#     if is_have:
#         try:
#             text = f"🏰Saroylar Jangi⚔️ bot uchun tasdiqlash kodi Kod: {sms_code}"
#             res = send_sms(phone_number=998940660299, message=text)
#             await message.answer(f"Yuborilgan SMS CODE ni yozing!")
#             await VerificationStates.generate_code.set()
#         except:
#             await message.answer("Code yuborishda xatolik yuz berdi!")
#     else:
#         await message.answer("Phone number not found in the system.")
#         await state.finish()


@dp.message_handler(IsPrivate(), lambda message: message.text and len(message.text) == 4,
                    state=VerificationStates.generate_code)
async def otp_handler(message: types.Message, state: FSMContext):
    user = UserService.get_user(tg_id=message.from_user.id)
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    if user and str(user['verify_code']) == message.text:
        result = UserService.set_is_verified(telegram_id=message.from_user.id, is_verified=True)
        MachineCheckService.create(telegram_id=message.from_user.id)
        FaceCheckService.create(telegram_id=message.from_user.id)
        await message.answer(_("Ro'yhatdan o'tdingiz!"), reply_markup=mainMenu())
    else:
        await message.answer(_("SMS CODE noto'gri."))
    await state.finish()
