from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, inline_keyboard
from loader import bot

inK = InlineKeyboardButton
signInSignUp = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Savol berish", callback_data="question"),
         InlineKeyboardButton(text="Ro'yxatdan o'tish", callback_data="signup")
         ],
        [InlineKeyboardButton(text="🔍 Izlash hizmati", callback_data="search")],
    ]
)

vil_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [inK(text="🕌 Farg'ona", callback_data="Farg'ona"), inK(text="🕌 Xiva", callback_data="Xiva")],
        [inK(text="🕌 Toshkent", callback_data="Toshkent"), inK(text="🕌 Namangan", callback_data="Namangan")],
        [inK(text="🕌 Buxoro", callback_data="Buxoro"), inK(text="🕌 Guliston", callback_data="Guliston")],
        [inK(text="🕌 Jizzax", callback_data="Jizzax"), inK(text="🕌 Zarafshon", callback_data="Zarafshon")],
        [inK(text="🕌 Qarshi", callback_data="Qarshi"), inK(text="🕌 Navoiy", callback_data="Navoiy")],
        [inK(text="🕌 Nukus", callback_data="Nukus"), inK(text="🕌 Samarqand", callback_data="Samarqand")],
        [inK(text="🕌 Termiz", callback_data="Termiz"), inK(text="🕌 Urganch", callback_data="Urganch")],
        [inK(text="🕌 Andijon", callback_data="Andijon")]
    ]
)


def update_data(vil):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [inK(text="♻️ Yangilash", callback_data=f"update_{vil}")],
            [inK(text="🔙Orqaga", callback_data="back")]
        ]
    )
    return btn


add_group = InlineKeyboardMarkup(
    inline_keyboard=[
        [inK(text="➕Botni guruhda ishlatish", url="https://t.me/Abusolimbot?startgroup=new")]
    ]
)
