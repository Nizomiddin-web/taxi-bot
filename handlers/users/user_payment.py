
import json
from datetime import datetime

import aiogram
from aiogram import types
from aiogram.types import ContentTypes

from data.config import PAYME_PROVIDER_TOKEN
from filters import IsPrivate
from keyboards.inline.payment_inline import payment_keyboard
from loader import dp, bot, i18n
from utils.api.service import AmountService, PaymentService
from utils.db_api.Service.user import UserBotService

_ = i18n.gettext
#PAYME_PROVIDER_TOKEN = "371317599:TEST:1726730149774"
CLICK_PROVIDER_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"


@dp.message_handler(IsPrivate(), text=["💳 Abonent To'lovlari", "💳Оплата подписки", "💳 Subscription Payments"])
async def user_payment(message: types.Message):
    user_bot = UserBotService.find_or_create(message.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    await message.reply(_("To'lov bo'limi"), reply_markup=payment_keyboard())


@dp.callback_query_handler(text="payment_history")
async def user_payment(call: types.CallbackQuery):
    user_bot = UserBotService.find_or_create(call.from_user.id)
    i18n.ctx_locale.set(user_bot.lang)
    result = PaymentService.get_history(telegram_id=call.from_user.id)
    if result.status_code == 200:
        text = _("<b>Ohirgi 10 kunlik to'lovlar\n\n👤User ID:</b>{user_id}\n").format(user_id=call.from_user.id)

        for i in result.json():
            datetime_object = datetime.fromisoformat(i['payment_date'])

            # Sana va vaqtni ajratib olish
            date_part = datetime_object.strftime("%Y-%m-%d")  # Sana qismi
            time_part = datetime_object.strftime("%H:%M:%S")  # Vaqt qismi

            # Dinamik qismni lokalizatsiya qiling
            text += _(
                "<b>💲To'lov turi:</b> {payment_type}\n<b>💵 Miqdori:</b> {amount_value}\n<b>📅 To'lov sanasi:</b> {"
                "date} {time}\n\n").format(
                payment_type=i['payment_type'],
                amount_value=i['amount_value'],
                date=date_part,
                time=time_part
            )
        await call.message.edit_text(text)


@dp.callback_query_handler(text="daily_payment")
async def user_payment(call: types.CallbackQuery):
    try:
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

        prices = [types.LabeledPrice(label=_("Kunlik Obuna"), amount=int(float(amount)) * 100)]  # 100 so'm = 1 UZS

        await call.message.edit_text(
            _("Quyidagi test karta orqali to'lovni amalga oshirishingiz mumkin: `8600 0000 0000 0000`\n\nMana sizning "
              "hisob-fakturangiz:"),
            parse_mode='Markdown'
        )

        await bot.send_invoice(
            call.from_user.id,
            title=_("Kunlik Obuna"),
            description=_("Kunlik obuna uchun to'lovni amalga oshiring."),
            provider_token=PAYME_PROVIDER_TOKEN,
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

    except aiogram.utils.exceptions.PaymentProviderInvalid as e:
        # Agar to'lov provayderi noto'g'ri bo'lsa, foydalanuvchiga xabar bering
        await call.message.answer(_("To'lov provayderida muammo mavjud: {}").format(e))
    except Exception as e:
        # Har qanday boshqa xatoliklar uchun umumiy xabar
        await call.message.answer(_("To'lovni amalga oshirishda muammo yuz berdi: {}").format(str(e)))


@dp.callback_query_handler(text="monthly_payment")
async def user_payment(call: types.CallbackQuery):
    try:
        user_id = call.from_user.id
        amounts = AmountService.get_amount(payment_type="monthly")
        if not amounts:
            await call.message.answer(_("Server xatoligi!!!"))
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

        prices = [types.LabeledPrice(label=_("Oylik Obuna"), amount=int(float(amount)) * 100)]  # 100 so'm = 1 UZS

        await call.message.edit_text(
            _("Quyidagi test karta orqali to'lovni amalga oshirishingiz mumkin: `8600 0000 0000 0000`\n\nMana sizning "
              "hisob-fakturangiz:"),
            parse_mode='Markdown'
        )

        await bot.send_invoice(
            call.from_user.id,
            title=_("Oylik Obuna"),
            description=_("Oylik obuna uchun to'lovni amalga oshiring."),
            provider_token=PAYME_PROVIDER_TOKEN,
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

    except aiogram.utils.exceptions.PaymentProviderInvalid as e:
        # Agar to'lov provayderi noto'g'ri bo'lsa, foydalanuvchiga xabar bering
        await call.message.answer(_("To'lov provayderida muammo mavjud: {}").format(e))
    except Exception as e:
        # Har qanday boshqa xatoliklar uchun umumiy xabar
        await call.message.answer(_("To'lovni amalga oshirishda muammo yuz berdi: {}").format(str(e)))


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    try:
        payload_data = json.loads(message.successful_payment.invoice_payload)
        user_id = payload_data.get('user_id')
        payment_type = payload_data.get('payment_type')
        result = PaymentService.create(telegram_id=user_id, amount_id=payment_type)
        if result.status_code == 201:
            await bot.send_message(
                message.chat.id,
                _("To'lovingiz muvaffaqiyatli amalga oshirildi! Miqdor: {amount} {currency}.").format(
                    amount=message.successful_payment.total_amount / 100,
                    currency=message.successful_payment.currency
                ),
                parse_mode='Markdown'
            )
        else:
            await message.answer(_("Ma'lumotlar serverga saqlanmadi\nTo'lov haqida adminlarga murojat qiling!!"))
    except Exception as e:
        # Har qanday boshqa xatoliklar uchun umumiy xabar
        await message.answer(_("To'lovni amalga oshirishda muammo yuz berdi: {}").format(str(e)))


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as e:
        # Pre-checkoutda xatolikni qo'lga olish
        await bot.send_message(pre_checkout_query.from_user.id,
                               _("Pre-checkout jarayonida xatolik yuz berdi: {}").format(str(e)))

