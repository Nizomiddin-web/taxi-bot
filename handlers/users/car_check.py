from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

from data.config import SUPPORT_TEAM_GROUP_FACE, SUPPORT_TEAM_GROUP_CAR, MANUAL_FAQ_URL
from filters import IsPrivate
from keyboards.default.menuKeyboard import car_check_menu, mainMenu
from keyboards.inline.car_check_inline import ask_add_car_photo, end_ask_add_car_photo, admin_check_photo_btn
from loader import dp
from states.userState import CarCheckStates
from utils.api.service import MachineCheckService, FaceCheckService
from utils.misc.check_photo import get_image_taken_time, is_taken_within_last_30_minutes


@dp.message_handler(IsPrivate(), text="🔙Ortga")
async def car_check_start(message: types.Message):
    # Namuna rasmni yuborish
    await message.answer("Asosiy bo'lim", reply_markup=mainMenu)
    # Holatni belgilaymiz


@dp.message_handler(IsPrivate(), text="📖 Manual/FAQ")
async def car_check_start(message: types.Message):
    # Namuna rasmni yuborish
    await message.answer(f'<a href="{MANUAL_FAQ_URL}">Qoidalar va Eng ko\'p beriladigan savollarga javoblar</a>')
    # Holatni belgilaymiz


@dp.message_handler(IsPrivate(), text="📊 Status")
async def car_check_start(message: types.Message):
    try:
        result_machine = MachineCheckService.get(telegram_id=message.from_user.id)
        result_face = FaceCheckService.get(telegram_id=message.from_user.id)
        if result_machine.status_code == 200 and result_face.status_code == 200:
            result_machine = result_machine.json()
            result_face = result_face.json()
            status_machine_text = "Tasdiqlangan✅" if result_machine['status'] == 'approved' else "Rad etilgan❌"
            status_face_text = "Tasdiqlangan✅" if result_machine['status'] == 'approved' else "Rad etilgan❌"
            text = f"<b>Tekshiruv: 🚕 Moshina Tekshiruvi\nStatus: {status_machine_text}\nSababi: {result_machine['rejection_reason'] or ''}\n\nTekshiruv: 👤 Ko'rinish Tekshiruvi\nStatus: {status_face_text}\nSababi: {result_face['rejection_reason'] or ''}</b>"
            await message.reply(text=text)
        else:
            await message.answer("Xatolik yuz berdi.\nIltimos keyinroq urinib ko'ring!")
    except:
        await message.answer("Xatolik yuz berdi.\nIltimos keyinroq urinib ko'ring!")


@dp.message_handler(IsPrivate(), text="📅 Kunlik Tekshiruv")
async def car_check_start(message: types.Message):
    # Namuna rasmni yuborish
    await message.answer("Tekshiruvni tanlang 👇", reply_markup=car_check_menu)
    # Holatni belgilaymiz


@dp.message_handler(IsPrivate(), text="🚕 Moshina Tekshiruvi")
async def car_check_start(message: types.Message, state: FSMContext):
    result = MachineCheckService.get(telegram_id=message.from_user.id)
    if result.status_code != 200:
        await message.answer("Siz ro'yhatdan o'tmagansiz!!!\n\nQayta \start bosing!!!")
        return
    else:
        result = result.json()
        if result['status'] == 'pending':
            await message.answer("Siz <b>🚕 Moshina Tekshiruvi</b>ga Rasm yuborgansiz\n\nRasmlaringiz Tekshiruv "
                                 "Jarayonida...")
            return
        elif result['status'] == 'approved':
            await message.answer("Siz Kunlik<b>🚕 Moshina Tekshiruvi</b>dan O'tgansiz!\n\nOq yo'l!!!")
            return
    # Namuna rasmni yuborish
    photo = "https://media.istockphoto.com/id/1296515357/vector/compact-city-car-four-angle-set-car-side-back-and-front-view-vector-flat-illustration.jpg?s=612x612&w=0&k=20&c=uhHEE3_ISpLRPliyfg0_35T50P-wf1eDhIV4HollnQs="
    await message.answer_photo(photo=photo,
                               caption="<b>Iltimos, moshina rasmlarini yuboring (5 tagacha).\n\nNamuna sifatida quyidagi rasmga qarang☝️\n\n❗️Eslatma: Rasmlarni 1 tadan yuboring!</b>")
    # Holatni belgilaymiz
    await CarCheckStates.waiting_for_images.set()
    await state.update_data(images=[])


@dp.message_handler(IsPrivate(), content_types=['document'], state=CarCheckStates.waiting_for_images)
async def car_check_start(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    file_name = f"photos/{message.from_user.id}.jpg"
    await message.document.download(destination_file=file_name)
    result = is_taken_within_last_30_minutes(image_path=f"{file_name}")
    if result:
        images = user_data.get('images', [])
        if len(images) >= 5:
            await message.answer(f"{len(images)}/5 rasmlar yuklandi.\nBoshqa rasm qabul qilinmaydi!",
                                 reply_markup=end_ask_add_car_photo)
        else:
            # Add the new image file_id to the list
            images.append(message.document.file_id)
            # Update the state with the new list
            await state.update_data(images=images)
            await message.answer(f"{len(images)}/5 rasmlar yuklandi.", reply_markup=ask_add_car_photo)
    else:
        await message.answer("Rasm qabul qilinmadi\n\nRasm olingan vaqt 30 daqiqadan oshmasligi shart!\n\nBoshqa rasm "
                             "yuboring!")


@dp.message_handler(IsPrivate(), content_types=['photo'], state=CarCheckStates.waiting_for_images)
async def car_check_start(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    file_name = f"photos/{message.from_user.id}.jpg"
    await message.photo[-1].download(destination_file=file_name)
    result = is_taken_within_last_30_minutes(image_path=f"{file_name}")
    if result:
        images = user_data.get('images', [])
        if len(images) >= 5:
            await message.answer(f"{len(images)}/5 rasmlar yuklandi.\nBoshqa rasm qabul qilinmaydi!",
                                 reply_markup=end_ask_add_car_photo)
        else:
            # Add the new image file_id to the list
            images.append(message.photo[-1].file_id)
            # Update the state with the new list
            await state.update_data(images=images)
            await message.answer(f"{len(images)}/5 rasmlar yuklandi.", reply_markup=ask_add_car_photo)
    else:
        await message.answer("Rasm qabul qilinmadi\n\nRasm olingan vaqt 30 daqiqadan oshmasligi shart!\n\nBoshqa rasm "
                             "yuboring!")


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=CarCheckStates.waiting_for_images)
async def car_check_start(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    if data == "add":
        await call.message.edit_text("Yana Rasm yuboring!")
    elif data == "end":
        await call.message.edit_text("Rasmlar tekshiruvga yuborildi!")
        MachineCheckService.update(telegram_id=call.from_user.id, status="pending")
        user_data = await state.get_data()
        images = user_data.get('images')
        # Create media group
        media = types.MediaGroup()
        for i in images:
            media.attach_document(i)
        text = f"<b>User ID: <code>{call.from_user.id}</code> \nTekshiruv: 🚕 Moshina Tekshiruvi</b>"
        await call.message.bot.send_media_group(chat_id=SUPPORT_TEAM_GROUP_CAR, media=media)
        await call.message.bot.send_message(chat_id=SUPPORT_TEAM_GROUP_CAR, text=text,
                                            reply_markup=admin_check_photo_btn)
        await state.finish()
    elif data == "destroy":
        await call.message.edit_text("<b>Tekshiruvga yuborishni bekor qildingiz</b>")
        await state.finish()
