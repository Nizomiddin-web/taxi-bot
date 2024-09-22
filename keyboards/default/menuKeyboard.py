from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📅 Kunlik Tekshiruv"),
            KeyboardButton(text="💳 Abonent To'lovlari"),
        ],
        [
            KeyboardButton(text="💬 Admin bilan Muloqot")
        ],
        [
            KeyboardButton(text="👤 Mening Profilim"),
            KeyboardButton(text="📖 Manual/FAQ")
        ]
    ],
    resize_keyboard=True
)

car_check_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚕 Moshina Tekshiruvi"),
            KeyboardButton(text="👤 Ko'rinish Tekshiruvi"),
        ],
        [
            KeyboardButton(text="📊 Status")
        ],
        [
            KeyboardButton(text="🔙Ortga")
        ]
    ],
    resize_keyboard=True
)

bekor_qilish = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬Chatni to'xtatish")
        ]
    ],
    resize_keyboard=True
)