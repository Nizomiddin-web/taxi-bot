
import json
from datetime import datetime

from aiogram import types
from aiogram.types import ContentTypes

from filters import IsPrivate
from keyboards.inline.payment_inline import payment_keyboard
from loader import dp, bot
from utils.api.service import AmountService, PaymentService

PAYME_PROVIDER_TOKEN = "371317599:TEST:1726730149774"
CLICK_PROVIDER_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"


@dp.message_handler(IsPrivate(), text="💳 Abonent To'lovlari")
async def user_payment(message: types.Message):
    await message.reply("To'lov bo'limi", reply_markup=payment_keyboard())


@dp.callback_query_handler(text="payment_history")
async def user_payment(call: types.CallbackQuery):
    result = PaymentService.get_history(telegram_id=call.from_user.id)
    if result.status_code == 200:
        text = f"<b>Ohirgi 10 kunlik to'lovlar\n\n👤User ID:{call.from_user.id}</b>\n"
        for i in result.json():
            datetime_object = datetime.fromisoformat(i['payment_date'])

            # Sana va vaqtni ajratib olish
            date_part = datetime_object.strftime("%Y-%m-%d")  # Sana qismi
            time_part = datetime_object.strftime("%H:%M:%S")  # Vaqt qismi
            text += f"<b>💲To'lov turi:</b>{i['payment_type']}\n<b>💵Miqdori:</b>{i['amount_value']}\n<b>📅To'lov sanasi:</b>{date_part} {time_part}\n\n"
        await call.message.edit_text(text)


@dp.callback_query_handler(text="daily_payment")
async def user_payment(call: types.CallbackQuery):
    user_id = call.from_user.id
    amounts = AmountService.get_amount(payment_type="daily")
    if not amounts:
        await call.message.answer("Server xatoligi!!!")
        return
    amount = amounts[0]['amount']
    payment_type = amounts[0]['id']

    # Create payload with user_id, amount, and payment_type
    payload_data = {
        'user_id': user_id,
        'amount': str(amount),  # Convert Decimal to string for JSON serialization
        'payment_type': payment_type
    }
    payload = json.dumps(payload_data)  # Convert dictionary to JSON string

    prices = [types.LabeledPrice(label="Kunlik Obuna", amount=int(float(amount)) * 100)]  # 100 so'm = 1 UZS

    await call.message.edit_text(
        "Quyidagi test karta orqali to'lovni amalga oshirishingiz mumkin: `8600 0000 0000 0000`\n\nMana sizning "
        "hisob-fakturangiz:",
        parse_mode='Markdown'
    )

    await bot.send_invoice(
        call.from_user.id,
        title="Kunlik Obuna",
        description="Kunlik obuna uchun to'lovni amalga oshiring.",
        provider_token=CLICK_PROVIDER_TOKEN,
        currency='UZS',  # Payme API uses UZS for Uzbek sums
        photo_url="https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg",  # example image
        photo_width=512,
        photo_height=512,
        photo_size=512,
        is_flexible=False,  # Shipping is not required for virtual services
        prices=prices,
        start_parameter="daily-subscription",
        payload=payload  # Use dynamically generated payload
    )


@dp.callback_query_handler(text="monthly_payment")
async def user_payment(call: types.CallbackQuery):
    user_id = call.from_user.id
    amounts = AmountService.get_amount(payment_type="monthly")
    if not amounts:
        await call.message.answer("Server xatoligi!!!")
        return
    amount = amounts[0]['amount']
    payment_type = amounts[0]['id']

    # Create payload with user_id, amount, and payment_type
    payload_data = {
        'user_id': user_id,
        'amount': str(amount),  # Convert Decimal to string for JSON serialization
        'payment_type': payment_type
    }
    payload = json.dumps(payload_data)  # Convert dictionary to JSON string

    prices = [types.LabeledPrice(label="Oylik Obuna", amount=int(float(amount)) * 100)]  # 100 so'm = 1 UZS

    await call.message.edit_text(
        "Quyidagi test karta orqali to'lovni amalga oshirishingiz mumkin: `8600 0000 0000 0000`\n\nMana sizning "
        "hisob-fakturangiz:",
        parse_mode='Markdown'
    )

    await bot.send_invoice(
        call.from_user.id,
        title="Oylik Obuna",
        description="Oylik obuna uchun to'lovni amalga oshiring.",
        provider_token=CLICK_PROVIDER_TOKEN,
        currency='UZS',  # Payme API uses UZS for Uzbek sums
        photo_url="https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg",  # example image
        photo_width=512,
        photo_height=512,
        photo_size=512,
        is_flexible=False,  # Shipping is not required for virtual services
        prices=prices,
        start_parameter="monthly-subscription",
        payload=payload  # Use dynamically generated payload
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payload_data = json.loads(message.successful_payment.invoice_payload)
    user_id = payload_data.get('user_id')
    payment_type = payload_data.get('payment_type')
    result = PaymentService.create(telegram_id=user_id, amount_id=payment_type)
    if result.status_code == 201:
        await bot.send_message(
            message.chat.id,
            f"To'lovingiz muvaffaqiyatli amalga oshirildi! Miqdor: {message.successful_payment.total_amount / 100} {message.successful_payment.currency}.",
            parse_mode='Markdown'
        )
    else:
        await message.answer("Ma'lumotlar serverga saqlanmadi\nTo'lov haqida adminlarga murojat qiling!!")
