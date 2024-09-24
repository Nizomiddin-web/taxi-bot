import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

from data.config import SUPPORT_TEAM_GROUP_FACE
from filters import IsPrivate
from keyboards.inline.car_check_inline import ask_add_car_photo, end_ask_add_car_photo, admin_check_photo_btn
from loader import dp, i18n
from states.userState import FaceCheckStates
from utils.api.service import FaceCheckService
from utils.db_api.Service.user import UserBotService
from utils.misc.check_photo import is_taken_within_last_30_minutes

_ = i18n.gettext


@dp.message_handler(IsPrivate(), text=["👤 Ko'rinish Tekshiruvi", "👤 Face Check", "👤 Проверка внешности"])
async def car_check_start(message: types.Message, state: FSMContext):
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    result = FaceCheckService.get(telegram_id=message.from_user.id)
    if result.status_code != 200:
        await message.answer(_("Siz ro'yhatdan o'tmagansiz!!!\n\nQayta \start bosing!!!"))
        return
    else:
        result = result.json()
        if result['status'] == 'pending':
            await message.answer(_("Siz <b>👤 Ko'rinish Tekshiruvi</b>ga Rasm yuborgansiz\n\nRasmlaringiz Tekshiruv "
                                   "Jarayonida..."))
            return
        elif result['status'] == 'approved':
            await message.answer(_("Siz Kunlik<b>👤 Ko'rinish Tekshiruvi</b>dan O'tgansiz!\n\nOq yo'l!!!"))
            return

            # Namuna rasmni yuborish
    photo = "https://i.pinimg.com/474x/a8/45/f1/a845f11e10d890b2926202b895658d20.jpg"
    await message.answer_photo(photo=photo,
                               caption=_("<b>Iltimos, Ko'rinishingiz rasmlarini yuboring (5 tagacha).\n\nNamuna "
                                         "sifatida quyidagi rasmga qarang☝️\n\n❗️Eslatma: Rasmlarni 1 tadan "
                                         "yuboring!</b>"))
    # Holatni belgilaymiz
    await FaceCheckStates.waiting_for_images.set()
    await state.update_data(images=[])


@dp.message_handler(IsPrivate(), content_types=['document'], state=FaceCheckStates.waiting_for_images)
async def car_check_start(message: types.Message, state: FSMContext):
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    user_data = await state.get_data()
    images = user_data.get('images', [])
    if len(images) >= 5:
        await message.answer(
            _("{img_len}/5 rasmlar yuklandi.\nBoshqa rasm qabul qilinmaydi!").format(img_len=len(images)),
            reply_markup=end_ask_add_car_photo)
        return
    file_name = f"photos/{message.from_user.id}.jpg"
    await message.document.download(destination_file=file_name)
    result = is_taken_within_last_30_minutes(image_path=f"{file_name}")
    if result:
        # Add the new image file_id to the list
        images.append(message.document.file_id)
        # Update the state with the new list
        await state.update_data(images=images)
        await message.answer(_("{img_len}/5 rasmlar yuklandi.").format(img_len=len(images)),
                             reply_markup=ask_add_car_photo)
    else:
        await message.answer(
            _("Rasm qabul qilinmadi\n\nRasm olingan vaqt 30 daqiqadan oshmasligi shart!\n\nBoshqa rasm "
              "yuboring!"))
    try:
        os.remove(file_name)
    except:
        pass


@dp.message_handler(IsPrivate(), content_types=['photo'], state=FaceCheckStates.waiting_for_images)
async def car_check_start(message: types.Message, state: FSMContext):
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    await message.answer(_("Rasmlarni document(file) shaklida yuboring!"))
    # user_data = await state.get_data()
    # images = user_data.get('images', [])
    # if len(images) >= 5:
    #     await message.answer(f"{len(images)}/5 rasmlar yuklandi.\nBoshqa rasm qabul qilinmaydi!",
    #                          reply_markup=end_ask_add_car_photo)
    # else:
    #     # Add the new image file_id to the list
    #     images.append(message.photo[-1].file_id)
    #     # Update the state with the new list
    #     await state.update_data(images=images)
    #     await message.answer(f"{len(images)}/5 rasmlar yuklandi.", reply_markup=ask_add_car_photo)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=FaceCheckStates.waiting_for_images)
async def car_check_start(call: types.CallbackQuery, state: FSMContext):
    user_bot = UserBotService.find_or_create(call.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    data = call.data.split("_")[1]
    if data == "add":
        await call.message.edit_text(_("Yana Rasm yuboring!"))
    elif data == "end":
        await call.message.edit_text(_("Rasmlar tekshiruvga yuborildi!"))
        status = FaceCheckService.update(telegram_id=call.from_user.id, status="pending")
        print(status)
        user_data = await state.get_data()
        images = user_data.get('images')
        # Create media group
        media = types.MediaGroup()
        for i in images[:-1]:
            media.attach_photo(i)
        text = f"<b>User ID: <code>{call.from_user.id}</code>\nTekshiruv: 👤 Ko'rinish Tekshiruvi</b>"
        media.attach_photo(images[-1])
        await call.message.bot.send_media_group(chat_id=SUPPORT_TEAM_GROUP_FACE, media=media)
        await call.message.bot.send_message(chat_id=SUPPORT_TEAM_GROUP_FACE, text=text,
                                            reply_markup=admin_check_photo_btn)
        await state.finish()
    elif data == "destroy":
        await call.message.edit_text(_("<b>Tekshiruvga yuborishni bekor qildingiz</b>"))
        await state.finish()
