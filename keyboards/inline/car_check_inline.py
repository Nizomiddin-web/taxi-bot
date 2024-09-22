from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inK = InlineKeyboardButton

ask_add_car_photo = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            inK(text="🖼Rasm Qo'shish➕", callback_data="photo_add")
        ],
        [
            inK(text="Yakunlash✅", callback_data="photo_end")
        ],
        [
            inK(text="Bekor Qilish🪓", callback_data="photo_destroy")
        ]
    ]
)

end_ask_add_car_photo = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            inK(text="Yakunlash✅", callback_data="photo_end")
        ],
        [
            inK(text="Bekor Qilish🪓", callback_data="photo_destroy")
        ]
    ]
)

admin_check_photo_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            inK(text="Approved✅", callback_data="admin_yes"),
            inK(text="Rejected❌", callback_data="admin_no")
        ]
    ]
)


def admin_review_photo(user_id, check_type):
    btnInl = InlineKeyboardMarkup(row_width=1)
    btnInl.insert(inK(text="Rasmlar aniq emas", callback_data=f"Rasmlar_aniq_emas_{check_type}_{user_id}"))
    btnInl.insert(inK(text="Rasmlar to'liq emas", callback_data=f"Rasmlar_to'liq_emas_{check_type}_{user_id}"))
    btnInl.insert(
        inK(text="Rasmlar noto'g'ri formatda", callback_data=f"Rasmlar_noto'g'ri_formatda_{check_type}_{user_id}"))
    btnInl.insert(inK(text="Rasmlar sifatli emas", callback_data=f"Rasmlar_sifatli_emas_{check_type}_{user_id}"))
    btnInl.insert(inK(text="Boshqa sabablar", callback_data=f"Rasmlar_other_{check_type}_{user_id}"))
    return btnInl


def user_update_profile_btn():
    btnInl = InlineKeyboardMarkup(row_width=2)
    update_phone_button = InlineKeyboardButton("📱 Telefonni O'zgartirish", callback_data=f"update_phone")
    update_first_name_button = InlineKeyboardButton("📝 Ismni O'zgartirish", callback_data=f"update_first_name")
    update_last_name_button = InlineKeyboardButton("📝 Familiyani O'zgartirish",
                                                   callback_data=f"update_last_name")
    delete = inK(text="❌", callback_data="delete")
    btnInl.insert(update_phone_button)
    btnInl.insert(update_first_name_button)
    btnInl.insert(update_last_name_button)
    btnInl.add(delete)

    return btnInl
