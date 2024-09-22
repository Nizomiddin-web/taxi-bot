from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from filters import IsPrivate
from keyboards.default.menuKeyboard import mainMenu, bekor_qilish
from loader import dp
from states.userState import VerificationStates
from utils.api.service import UserService, MachineCheckService, FaceCheckService, SupportRequestService
from utils.db_api.Service.user import DemoService
import random


def generate_verification_code(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


@dp.message_handler(IsPrivate(), commands=['start'])
async def start_handler(message: types.Message):
    deep_link_parameter = message.get_args()
    if deep_link_parameter:
        data = deep_link_parameter.split('_')
        user_id = data[1]
        support_id = data[-1]
        result = SupportRequestService.update(id=support_id, telegram_id=message.from_user.id)
        if result.status_code == 404:
            await message.answer("So'rov topilmadi!")
            return
        await message.answer("Ulanish Hosil qilindi!", reply_markup=bekor_qilish)
        await message.bot.send_message(chat_id=user_id, text=f"Admin siz bilan bog'landi❗️")
        await message.bot.send_message(chat_id=user_id,
                                       text=f"Assalomu alaykum\nIsmim:{message.from_user.first_name}\nQanday savollaringiz bor?")
        return
    user = UserService.find_or_create(message.from_user.id)
    if user['is_admin']:
        await message.answer("Assalomu alaykum Admin!!!")
        return
    if user['verification_status']:
        await message.answer("Hush kelibsiz siz ro'yhatdan o'tgansiz", reply_markup=mainMenu)
    else:
        await message.answer("Ro'yhatdan o'tgan Telefon raqamingizni yuboring!")
        await VerificationStates.ask_phone.set()


@dp.message_handler(IsPrivate(), lambda message: message.text and message.text.isdigit(),
                    state=VerificationStates.ask_phone)
async def phone_number_handler(message: types.Message, state: FSMContext):
    sms_code = generate_verification_code()
    is_have = DemoService.is_have_user(tg_id=message.from_user.id, phone_number=message.text,
                                       verification_code=sms_code)
    if is_have:
        await message.answer(f"Verification code sent: {sms_code}")
        await VerificationStates.generate_code.set()
    else:
        await message.answer("Phone number not found in the system.")
        await state.finish()


@dp.message_handler(IsPrivate(), lambda message: message.text and len(message.text) == 6,
                    state=VerificationStates.generate_code)
async def otp_handler(message: types.Message, state: FSMContext):
    user = UserService.get_user(tg_id=message.from_user.id)
    if user and str(user['verify_code']) == message.text:
        result = UserService.set_is_verified(telegram_id=message.from_user.id, is_verified=True)
        MachineCheckService.create(telegram_id=message.from_user.id)
        FaceCheckService.create(telegram_id=message.from_user.id)
        await message.answer("Verification successful! You can now access other menus.", reply_markup=mainMenu)
    else:
        await message.answer("Invalid OTP.")
    await state.finish()
