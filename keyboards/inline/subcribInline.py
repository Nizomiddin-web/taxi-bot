from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def subsButton(channels, values):
    btnInl = InlineKeyboardMarkup(row_width=1)
    i = 0
    for channel in channels:
        btnKeyboard = InlineKeyboardButton(text=channel, url=values[i])
        btnInl.insert(btnKeyboard)
        i += 1
    azoCheck = InlineKeyboardButton("Obunani tekshirish", callback_data="check_subs")
    btnInl.insert(azoCheck)
    return btnInl
