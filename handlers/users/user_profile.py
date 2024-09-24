from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivate
from keyboards.inline.car_check_inline import user_update_profile_btn
from loader import dp, i18n
from states.userState import UpdateProfileState
from utils.api.service import UserService
from utils.db_api.Service.user import UserBotService

_ = i18n.gettext


@dp.message_handler(IsPrivate(), text=["👤 Mening Profilim", "👤 Мой Профиль", "👤 My Profile"])
async def user_profile(message: types.Message):
    # Profil ma'lumotlarini shakllantirish
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    try:
        user_info = UserService.get_user(tg_id=message.from_user.id)
        profile_info = f"<b>Ism:</b> {user_info['first_name'] or 'Kiritilmagan!'}\n" \
                       f"<b>Familiya:</b> {user_info['last_name'] or 'Kiritilmagan!'}\n" \
                       f"<b>📱Telefon:</b> {user_info['country_code'] or ''}{user_info['phone_number']}\n" \
                       f"<b>💰Balance:</b> {user_info['balance']} so'm\n"
        await message.reply(profile_info, reply_markup=user_update_profile_btn())
    except:
        await message.answer(_("Xatolik yuz berdi,Iltimos keyinroq urinib ko'ring!"))


# delete
@dp.callback_query_handler(lambda c: c.data.startswith('delete'))
async def update_first_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data.startswith('update_phone'))
async def update_phone_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_bot = UserBotService.find_or_create(callback_query.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    # Foydalanuvchidan yangi telefon raqamini so'rash
    await callback_query.answer(cache_time=1)
    await callback_query.message.edit_text(_("<b>Yangi 📱telefon raqamingizni kiriting:</b>"))
    # State ga o'tish
    await UpdateProfileState.update_phone.set()


@dp.message_handler(content_types=['text'], state=UpdateProfileState.update_phone)
async def process_phone_update(message: types.Message, state: FSMContext):
    new_phone = message.text
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    # Telefon raqamining validatsiyasi
    if not new_phone.startswith('+') or len(new_phone) < 10:
        await message.answer(_("Iltimos, to'g'ri telefon raqamini kiriting.\nMasalan: +998901234567"))
        return

    # Telefon raqamini bazada yangilash
    is_true = UserService.update_user_info(tg_id=message.from_user.id, phone=new_phone)
    # user.phone_number = new_phone  # Ma'lumotlar bazasida yangilang
    if is_true:
        await message.answer(_("Telefon raqamingiz muvaffaqiyatli yangilandi: {new_phone}").format(new_phone=new_phone))
    else:
        await message.answer(_("Xatolik yuz berdi iltimos keyinroq urinib ko'ring!\n\nEslatma:Siz Boshqa shahsga "
                               "tegishli raqamni kiritgan bo'lishingiz mumkin!"))
    # State tugatish
    await state.finish()


# Ismni yangilash
@dp.callback_query_handler(lambda c: c.data.startswith('update_first_name'))
async def update_first_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer(cache_time=1)
    user_bot = UserBotService.find_or_create(callback_query.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    # Foydalanuvchidan yangi ismni so'rash
    await callback_query.message.edit_text(_("Yangi ismingizni kiriting:"))

    # State ga o'tish
    await UpdateProfileState.update_first_name.set()


@dp.message_handler(IsPrivate(), state=UpdateProfileState.update_first_name)
async def process_first_name_update(message: types.Message, state: FSMContext):
    new_first_name = message.text
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    # Ismni bazada yangilash
    user_id = message.from_user.id
    is_true = UserService.update_user_info(tg_id=user_id, first_name=new_first_name)
    if is_true:
        await message.answer(
            _("Ismingiz muvaffaqiyatli yangilandi: {new_first_name}").format(new_first_name=new_first_name))
    else:
        await message.answer(_("Xatolik yuz berdi iltimos keyinroq urinib ko'ring!"))
    # State tugatish
    await state.finish()


# Familiyani yangilash
@dp.callback_query_handler(lambda c: c.data.startswith('update_last_name'))
async def update_last_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer(cache_time=1)
    user_bot = UserBotService.find_or_create(callback_query.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    # Foydalanuvchidan yangi familiyani so'rash
    await callback_query.message.edit_text(_("Yangi familiyangizni kiriting:"))
    # State ga o'tish
    await UpdateProfileState.update_last_name.set()


@dp.message_handler(IsPrivate(), state=UpdateProfileState.update_last_name)
async def process_last_name_update(message: types.Message, state: FSMContext):
    new_last_name = message.text
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    # Familiyani bazada yangilash
    user_id = message.from_user.id
    is_true = UserService.update_user_info(tg_id=user_id, last_name=new_last_name)
    if is_true:
        await message.answer(
            _("Familiyangiz muvaffaqiyatli yangilandi: {new_last_name}").format(new_last_name=new_last_name))
    else:
        await message.answer(_("Xatolik yuz berdi iltimos keyinroq urinib ko'ring!"))
    # State tugatish
    await state.finish()
