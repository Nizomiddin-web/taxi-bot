from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import i18n

_ = i18n.gettext

def admin_support_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton(text=_("Ha Istayman✅"), callback_data='support_yes'))
    keyboard.insert(InlineKeyboardButton(text=_("Yo'q, Rahmat❌"), callback_data='support_no'))
    return keyboard


def muloqot_btn(chat_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton(text="Muloqotni boshlash",callback_data=f'muloqot_{chat_id}'))
    return keyboard
