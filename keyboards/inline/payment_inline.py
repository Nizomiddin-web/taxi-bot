from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton(text="📅Kunlik To'lov", callback_data='daily_payment'))
    keyboard.insert(InlineKeyboardButton(text="📆Oylik To'lov", callback_data='monthly_payment'))
    keyboard.insert(InlineKeyboardButton(text="📁To'lovlar Tarixi", callback_data='payment_history'))
    delete = InlineKeyboardButton(text="❌", callback_data="delete")
    keyboard.add(delete)
    return keyboard