from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import i18n

_ = i18n.gettext


def mainMenu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("📅 Kunlik Tekshiruv")),
                KeyboardButton(text=_("💳 Abonent To'lovlari")),
            ],
            [
                KeyboardButton(text=_("💬 Admin bilan Muloqot"))
            ],
            [
                KeyboardButton(text=_("👤 Mening Profilim")),
                KeyboardButton(text="📖 Manual/FAQ")
            ]
        ],
        resize_keyboard=True
    )


def car_check_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🚕 Moshina Tekshiruvi")),
                KeyboardButton(text=_("👤 Ko'rinish Tekshiruvi")),
            ],
            [
                KeyboardButton(text="📊 Status")
            ],
            [
                KeyboardButton(text=_("🔙Ortga"))
            ]
        ],
        resize_keyboard=True)


def bekor_qilish():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("💬Chatni to'xtatish"))
            ]
        ],
        resize_keyboard=True
    )


def send_contact():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("📱Telefon raqamni yuborish"), request_contact=True)
            ]
        ],
        resize_keyboard=True,
    )
