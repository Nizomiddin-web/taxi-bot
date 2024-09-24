from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_selection_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='set_lang_uz'))
    keyboard.add(InlineKeyboardButton(text="🇷🇺 Русский", callback_data='set_lang_ru'))
    keyboard.add(InlineKeyboardButton(text="🇬🇧 English", callback_data='set_lang_en'))
    return keyboard