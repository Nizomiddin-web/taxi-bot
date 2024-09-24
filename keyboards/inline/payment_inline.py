from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import i18n

_ = i18n.gettext

def payment_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton(text=_("📅Kunlik To'lov"), callback_data='daily_payment'))
    keyboard.insert(InlineKeyboardButton(text=_("📆Oylik To'lov"), callback_data='monthly_payment'))
    keyboard.insert(InlineKeyboardButton(text=_("📁To'lovlar Tarixi"), callback_data='payment_history'))
    delete = InlineKeyboardButton(text="❌", callback_data="delete")
    keyboard.add(delete)
    return keyboard